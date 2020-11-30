# %%
from tensorflow.keras.models import load_model
from pathlib import PurePath
from training.utils import *
from tensorflow.keras.preprocessing.image import img_to_array, load_img
from numpy import expand_dims

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

train_gen, valid_gen, test_gen = get_train_valid_test_split(target)


# %%
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
num_epochs = 30
model_name = "dx-weighted-inception"
model = train_checkpoint_save(model, train_gen, valid_gen,
                              model_name, num_epochs=num_epochs)


# %%
def load_and_do_test_predictions():
    """
    Requires reloading environment/model and refreshing generators to
    clear GPU memory from training, run all cells except training.
    """
    mpath = PurePath(f"{PROJECT_DIR}models/save/dx-weighted-inception/01")
    m = load_model(str(mpath))
    p = m.predict(test_gen)
    return m, p


def load_single_image(filename):
    img_path = PurePath(f"{IMG_DIR}/{filename}")
    img = load_img(str(img_path), target_size=(256, 256), color_mode="rgb")
    idg = ImageDataGenerator(
            samplewise_center=True,
            samplewise_std_normalization=True,
            fill_mode='constant',
            cval=1.0)
    img = img_to_array(img)
    img = expand_dims(img, axis=0)
    img = idg.flow(img)
    return img


def test_single_img_prediction(m, filename):
    img = load_single_image(filename)
    prediction = m.predict(img)
    return prediction


loaded_model, preds = load_and_do_test_predictions()
for i in range(10):
    print("From test gen:")
    print(preds[i])
    print("From single image:")
    print(test_single_img_prediction(loaded_model, test_gen.filenames[i]))
