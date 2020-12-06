from pathlib import PurePath
from keras_preprocessing.image import ImageDataGenerator
import pandas as pd
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from sklearn.model_selection import train_test_split
from tensorflow.keras.callbacks import ModelCheckpoint, CSVLogger
from datetime import datetime
from tensorflow.keras.applications.densenet import DenseNet201
from tensorflow.keras.layers import Input, Dense
from tensorflow.keras.models import Model

DUMMY_IMG = "00000001_000.png"
PROJECT_DIR = "/content/"
DATASET_DIR = PROJECT_DIR + "dataset/"
IMG_DIR = DATASET_DIR + "images"

Y_COL_NAME = "findings_list"
IMG_SIZE = 256
TRAINING_SIZE = 500
BATCH_SIZE = 32
RND_SEED = 8
IMG_CHANNELS = 1
TEST_SIZE = 0.2

SPLIT_VALUE = 0.15


def print_gpu_status():
    print(f"TensorFlow version: {tf.__version__}")
    gpu_data = tf.config.list_physical_devices("GPU")
    if gpu_data:
        print(f"GPU is available for training.\nTotal GPUs: {len(gpu_data)}")
    else:
        print("WARNING: GPU is not available for training!")


def get_img_metadata():
    path = PurePath(DATASET_DIR + "usable_img_metadata.csv")
    data = pd.read_csv(str(path))
    dx_labels = get_dx_labels()
    data[Y_COL_NAME] = data[dx_labels].apply(create_classification_list,
                                             axis=1)
    return data


def create_classification_list(row):
    findings = []
    for label, value in row.items():
        if value > 0.5:
            findings.append(label)
    return findings


def get_dx_labels():
    path = PurePath(DATASET_DIR + "dx_labels.csv")
    with open(path, 'r') as f:
        lines = f.readlines()[1:]
        return [line.strip() for line in lines]


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

    idg = init_image_data_generator(split=valid_subset, augment=shuffle)

    return idg.flow_from_dataframe(img_metadata,
                                   directory=str(PurePath(IMG_DIR)),
                                   x_col="img_filename",
                                   y_col=Y_COL_NAME,
                                   target_size=(IMG_SIZE, IMG_SIZE),
                                   color_mode="rgb",
                                   # classes=get_dx_labels(),
                                   class_mode="categorical",
                                   batch_size=batch_size,
                                   shuffle=shuffle,
                                   seed=rnd_seed,
                                   subset=subset)


def init_image_data_generator(split=False, augment=False):
    split_value = SPLIT_VALUE if split else 0.0
    if not augment:
        return ImageDataGenerator(
                samplewise_center=True,
                samplewise_std_normalization=True,
                fill_mode='constant',
                cval=1.0,
                validation_split=split_value)

    return ImageDataGenerator(
            samplewise_center=True,
            samplewise_std_normalization=True,
            horizontal_flip=True,
            vertical_flip=False,
            height_shift_range=0.05,
            width_shift_range=0.1,
            rotation_range=5,
            shear_range=0.1,
            fill_mode='constant',
            zoom_range=0.15,
            cval=1.0,
            validation_split=split_value)


def get_date_time_str():
    return datetime.now().strftime("%Y%m%d-%H%M%S")


def save_model(model, base_model_name):
    date_time = get_date_time_str()
    path = f"./models/{date_time}_{base_model_name}.h5"
    model.save(path)


def train_checkpoint_save(model,
                          train_gen,
                          valid_gen,
                          model_name,
                          monitor="val_loss",
                          num_epochs=10, version="01"):
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


def init_model():
    _input = Input(train_gen.image_shape)
    densenet = DenseNet201(include_top=False,
                           weights="imagenet",
                           input_tensor=_input,
                           input_shape=train_gen.image_shape,
                           pooling="avg")

    predictions = Dense(len(sample_labels), activation='sigmoid')(
            densenet.output)

    base = Model(inputs=_input, outputs=predictions)

    optimizer = tf.keras.optimizers.Nadam(learning_rate=0.001)
    base.compile(optimizer=optimizer,
                 loss="categorical_crossentropy",
                 metrics=["accuracy", "mae"])
    return base


model = init_model()
num_epochs = 100
model_name = "wdense201_s5000-allLabels"
model = train_checkpoint_save(model, train_gen, valid_gen,
                              model_name, num_epochs=num_epochs, version="00")
