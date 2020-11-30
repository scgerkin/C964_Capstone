# %%
from training.utils import *

img_metadata = get_img_metadata()
single_finding_records = img_metadata[
    img_metadata["findings_list"].apply(lambda val: len(val) == 1)]

df = single_finding_records
dx_labels = get_dx_labels()

pre_drop_counts = {}
for label in dx_labels:
    pre_drop_counts[label] = len(df[df[label] > 0.5].index)

pre_drop_rows = len(df.index)
print(f"Before:\n{df.describe()}")

SAMPLE_THRESHOLD = 500

removed_labels = set()
for label, count in pre_drop_counts.items():
    if count < SAMPLE_THRESHOLD:
        indices = df[df[label] > 0.5].index
        df = df.drop(indices)
        df = df.drop(labels=[label], axis=1)
        removed_labels.add(label)

post_drop_rows = len(df.index)
print(f"after:\n{df.describe()}")

post_drop_counts = {}
sample_labels = set()
for label in dx_labels:
    if label not in removed_labels:
        sample_labels.add(label)
        post_drop_counts[label] = len(df[df[label] > 0.5].index)


def print_vals(lbl, rows, counts):
    print(f"{lbl}---Rows: {rows}\tCounts:\n{counts}")


print_vals("Pre drop", pre_drop_rows, pre_drop_counts)
print_vals("Post drop", post_drop_rows, post_drop_counts)
print(f"Removed labels: {', '.join(removed_labels)}")

RANDOM_SEED = 42

only_finding_labels = sample_labels.copy()
only_finding_labels.remove("no_finding")

target = pd.DataFrame()
sample_counts = {}
for label in only_finding_labels:
    sample = df[df[label] > 0.5].sample(n=SAMPLE_THRESHOLD,
                                        replace=False,
                                        random_state=RANDOM_SEED,
                                        axis=0)
    sample_counts[label] = len(sample.index)
    target = pd.concat([target, sample])

# Shuffle the dataset
target = target.sample(frac=1, random_state=RANDOM_SEED)
print(target.describe())
print(f"Total labels: {len(sample_counts)}\n{sample_counts}")

print_gpu_status()
# %%
train_gen, valid_gen, test_gen = get_train_valid_test_split(target)


def init_model():
    m = Sequential()
    m.add(InceptionV3(input_shape=train_gen.image_shape,
                      include_top=False,
                      weights="imagenet"))
    m.add(GlobalAveragePooling2D())
    m.add(Dense(512))
    m.add(Dense(len(only_finding_labels), activation='sigmoid'))
    optimizer = tf.keras.optimizers.Nadam()
    m.compile(optimizer=optimizer,
              loss="categorical_crossentropy",
              metrics=["accuracy", "mae"])
    return m


model = init_model()
num_epochs = 10
model = train_checkpoint_save(model, train_gen, valid_gen,
                              "dx-weighted-inception", num_epochs=num_epochs)
