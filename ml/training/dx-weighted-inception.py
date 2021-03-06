# %%
from pathlib import PurePath
from tensorflow.keras.callbacks import ModelCheckpoint, CSVLogger
from datetime import datetime
from tensorflow.keras.models import load_model
from sklearn.model_selection import train_test_split
from tensorflow.keras.applications.inception_v3 import InceptionV3
from tensorflow.keras import Sequential
from training.utils import (get_dx_labels,
                            get_img_metadata,
                            PROJECT_DIR,
                            IMG_SIZE,
                            IMG_DIR,
                            Y_COL_NAME,
                            init_image_data_generator,
                            )
import pandas as pd
import tensorflow as tf
from tensorflow.keras.preprocessing.image import img_to_array, load_img
from numpy import expand_dims
from tensorflow.keras.layers import (Dense,
                                     GlobalAveragePooling2D,
                                     )

BATCH_SIZE = 32


def get_train_valid_test_split(img_data):
    train_df, test_df = train_test_split(img_data, test_size=0.10,
                                         random_state=42)

    training_data = get_data_batch(train_df, subset="training")
    validation_data = get_data_batch(train_df, subset="validation")
    test_gen = get_data_batch(test_df, subset=None)
    return training_data, validation_data, test_gen


def get_data_batch(img_metadata,
                   batch_size=None,
                   rnd_seed=None,
                   subset=None):
    if batch_size is None:
        batch_size = BATCH_SIZE

    valid_subset = subset == "training" or subset == "validation"
    if subset is not None and not valid_subset:
        raise ValueError(f"Invalid subset value: {subset}")

    shuffle = subset == "training"

    idg = init_image_data_generator(split=valid_subset)

    return idg.flow_from_dataframe(img_metadata,
                                   directory=str(PurePath(IMG_DIR)),
                                   x_col="img_filename",
                                   y_col=Y_COL_NAME,
                                   target_size=(IMG_SIZE, IMG_SIZE),
                                   color_mode="rgb",
                                   class_mode="categorical",
                                   batch_size=batch_size,
                                   shuffle=shuffle,
                                   seed=rnd_seed,
                                   subset=subset)


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


# Prepare for training
def print_gpu_status():
    print(f"TensorFlow version: {tf.__version__}")
    gpu_data = tf.config.list_physical_devices("GPU")
    if gpu_data:
        print(f"GPU is available for training.\nTotal GPUs: {len(gpu_data)}")
    else:
        print("WARNING: GPU is not available for training!")


print_gpu_status()
train_gen, valid_gen, test_gen = get_train_valid_test_split(target)


def map_set(row):
    fname = row["img_filename"]
    if fname in train_gen.filenames:
        return "training"
    elif fname in valid_gen.filenames:
        return "validation"
    return "testing"


target["split_set"] = target.apply(map_set, axis=1)
tpath = f"{PROJECT_DIR}training/train_data.csv"
target.drop(["findings_list"], axis=1).to_csv(tpath, index=False)


# %%
def init_model():
    base = Sequential()
    base.add(InceptionV3(input_shape=train_gen.image_shape,
                         include_top=False,
                         weights="imagenet"))
    base.add(GlobalAveragePooling2D())
    base.add(Dense(512))
    base.add(Dense(len(sample_labels), activation='sigmoid'))
    optimizer = tf.keras.optimizers.Nadam(learning_rate=0.001)
    base.compile(optimizer=optimizer,
                 loss="categorical_crossentropy",
                 metrics=["accuracy", "mae"])
    return base


def train_checkpoint_save(model,
                          train_gen,
                          valid_gen,
                          model_name,
                          monitor="val_loss",
                          num_epochs=10, version="01"):
    def get_date_time_str():
        return datetime.now().strftime("%Y%m%d-%H%M%S")

    def save_model(model, base_model_name):
        date_time = get_date_time_str()
        path = f"./models/{date_time}_{base_model_name}.h5"
        model.save(path)

    dt = get_date_time_str()
    checkpoint_fp = f"./checkpoints/{dt}-{model_name}.h5"
    checkpoint_cb = ModelCheckpoint(checkpoint_fp,
                                    save_freq="epoch",
                                    monitor=monitor,
                                    save_best_only=True)

    csv_fp = f"./logs/{dt}-{version}-{model_name}.csv"
    csv_cb = CSVLogger(csv_fp)

    callbacks = [checkpoint_cb, csv_cb]

    STEP_SIZE_TRAIN = train_gen.n // train_gen.batch_size
    STEP_SIZE_VALID = valid_gen.n // valid_gen.batch_size
    model.fit_generator(generator=train_gen,
                        steps_per_epoch=STEP_SIZE_TRAIN,
                        validation_data=valid_gen,
                        validation_steps=STEP_SIZE_VALID,
                        epochs=num_epochs,
                        callbacks=callbacks)

    # Save the final trained model and the checkpoint with the best monitor
    save_model(model, f'{model_name}-final')
    early_stop_model = tf.keras.models.load_model(checkpoint_fp)
    save_model(early_stop_model, f'{model_name}-bestcp')
    weights_path = f"{PROJECT_DIR}models/save/{model_name}/{version}"
    tf.saved_model.save(model, weights_path)
    return model


model = init_model()
# %%
num_epochs = 100
model_name = "dx-weighted-inception"
model = train_checkpoint_save(model, train_gen, valid_gen,
                              model_name, num_epochs=num_epochs, version="00")


# %% This cell and beyond requires reloading environment/model
# and refreshing generators to clear GPU memory from training.
# Then, all cells for initializing data must be run except training.
def load_and_do_test_predictions():
    mpath = PurePath(f"{PROJECT_DIR}models/save/wincep_train-overfit_s500/04")
    m = load_model(str(mpath))
    p = m.predict(test_gen)
    return m, p


def load_single_image(filename):
    img_path = PurePath(f"{IMG_DIR}/{filename}")
    img = load_img(str(img_path), target_size=(256, 256), color_mode="rgb")
    idg = init_image_data_generator()
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
    pdf.to_csv(f"{PROJECT_DIR}analysis/{name}.csv", index=False)


def load_model_make_and_save_preds():
    loaded_model, test_preds = load_and_do_test_predictions()

    train_preds = loaded_model.predict(train_gen)
    valid_preds = loaded_model.predict(valid_gen)
    save_preds_to_file("test_preds", test_preds, test_gen.filenames)
    save_preds_to_file("train_preds", train_preds, train_gen.filenames)
    save_preds_to_file("valid_preds", valid_preds, valid_gen.filenames)


load_model_make_and_save_preds()
