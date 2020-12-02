# %%
from pathlib import PurePath

from keras_preprocessing.image import ImageDataGenerator
from tensorflow.keras.models import load_model
from tensorflow.keras.applications.inception_v3 import InceptionV3
from tensorflow.keras import Sequential
from training.utils import (get_dx_labels,
                            get_img_metadata,
                            print_gpu_status,
                            get_train_valid_test_split,
                            train_checkpoint_save, PROJECT_DIR, IMG_DIR,
                            )
import pandas as pd
import tensorflow as tf
from tensorflow.keras.preprocessing.image import img_to_array, load_img
from numpy import expand_dims
from tensorflow.keras.layers import (Dense,
                                     GlobalAveragePooling2D,
                                     Dropout,
                                     )

# Load only records with a single finding
img_metadata = get_img_metadata()
single_finding_records = img_metadata[
    img_metadata["findings_list"].apply(lambda val: len(val) == 1)]

df = single_finding_records
dx_labels = get_dx_labels()
# Get counts of images per label
pre_drop_counts = {}
for label in dx_labels:
    pre_drop_counts[label] = len(df[df[label] > 0.5].index)

pre_drop_rows = len(df.index)
print(f"Before:\n{df.describe()}")

SAMPLE_THRESHOLD = 500
# Remove any records with a finding below the threshold
# also remove the column for that label
removed_labels = set()
for label, count in pre_drop_counts.items():
    if count < SAMPLE_THRESHOLD:
        indices = df[df[label] > 0.5].index
        df = df.drop(indices)
        df = df.drop(labels=[label], axis=1)
        removed_labels.add(label)

post_drop_rows = len(df.index)
print(f"after:\n{df.describe()}")

# Get the counts per label again
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

# Get equal number of samples of each finding label
RANDOM_SEED = 42

target = pd.DataFrame()
sample_counts = {}
for label in sample_labels:
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

# TODO: consider saving this as an csv for data discussion
# Prepare for training
print_gpu_status()
train_gen, valid_gen, test_gen = get_train_valid_test_split(target)


# %%
def init_model():
    base = Sequential()
    base.add(InceptionV3(input_shape=train_gen.image_shape,
                         include_top=False,
                         weights="imagenet"))
    base.add(GlobalAveragePooling2D())
    base.add(Dense(512))
    # base.add(Dropout(0.3))
    base.add(Dense(len(sample_labels), activation='sigmoid'))
    optimizer = tf.keras.optimizers.Nadam(learning_rate=0.001)
    base.compile(optimizer=optimizer,
                 loss="categorical_crossentropy",
                 metrics=["accuracy", "mae"])
    return base


model = init_model()
# %%
num_epochs = 30
model_name = "dx-weighted-inception"
model = train_checkpoint_save(model, train_gen, valid_gen,
                              model_name, num_epochs=num_epochs, version="00")


# %%
def load_and_do_test_predictions():
    """
    Requires reloading environment/model and refreshing generators to
    clear GPU memory from training, run all cells except training.
    """
    mpath = PurePath(f"{PROJECT_DIR}models/save/wincep_train-overfit_s500/04")
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


def preds_to_df(preds, filenames):
    pdf = pd.DataFrame()
    pdf["filename"] = filenames
    lbls = list(sample_labels)
    lbls.sort()
    for i, lbl in enumerate(lbls):
        pdf[lbl] = preds[:, i]
    return pdf.round(4)


def save_preds_to_file(name, preds, filenames):
    pdf = preds_to_df(preds, filenames)
    pdf.to_csv(f"{name}.csv", index=False)


def load_model_make_and_save_preds():
    loaded_model, test_preds = load_and_do_test_predictions()

    train_preds = loaded_model.predict(train_gen)
    valid_preds = loaded_model.predict(valid_gen)
    save_preds_to_file("test_preds", test_preds, test_gen.filenames)
    save_preds_to_file("train_preds", train_preds, train_gen.filenames)
    save_preds_to_file("valid_preds", valid_preds, valid_gen.filenames)


# %%
load_model_make_and_save_preds()
