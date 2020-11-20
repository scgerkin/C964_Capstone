from pathlib import PurePath
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from sklearn.model_selection import train_test_split
import pandas as pd
from tensorflow.keras.applications.inception_v3 import InceptionV3
from tensorflow.keras import Sequential
from tensorflow.keras.layers import (Dense,
                                     GlobalAveragePooling2D,
                                     )
from datetime import datetime

DUMMY_IMG = "00000001_000.png"
PROJECT_DIR = "W:/WGU/C964_Capstone/project/ml/"
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

DX_LABELS = None  # cache dx labels


def print_gpu_status():
    import tensorflow as tf
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
    global DX_LABELS
    if DX_LABELS is not None:
        return DX_LABELS
    path = PurePath(DATASET_DIR + "dx_labels.csv")
    with open(path, 'r') as f:
        lines = f.readlines()[1:]
        DX_LABELS = [line.strip() for line in lines]
        return DX_LABELS


def get_train_valid_test_split(img_data):
    train_df, test_df = train_test_split(img_data, test_size=0.10,
                                         random_state=42)

    training_data = get_data_batch(train_df, subset="training")
    validation_data = get_data_batch(train_df, subset="validation")
    test_gen = get_data_batch(test_df, batch_size=1024, subset=None)
    return training_data, validation_data, test_gen


def get_data_batch(img_metadata,
                   batch_size=None,
                   rnd_seed=None,
                   subset=None):
    """
    TODO: This will use the entire directory, but that's a ton of files
        Will need to send in a subset of the DF, but that won't perform
        a full shuffle on the entire dataset, just the given subset
        For now, with testing, this is fine, but will need to either
        shuffle the dataframe, pass a subset, then create a batch from
        that, or something...
    :param img_metadata:
    :param batch_size:
    :param rnd_seed:
    :param subset:
    :return:
    """

    if batch_size is None:
        batch_size = BATCH_SIZE

    valid_subset = subset == "training" or subset == "validation"
    if subset is not None and not valid_subset:
        raise ValueError(f"Invalid subset value: {subset}")

    idg = init_image_data_generator(split=valid_subset)

    shuffle = subset == "training"

    return idg.flow_from_dataframe(img_metadata,
                                   directory=str(PurePath(IMG_DIR)),
                                   x_col="img_filename",
                                   y_col=Y_COL_NAME,
                                   target_size=(IMG_SIZE, IMG_SIZE),
                                   color_mode="grayscale",
                                   # classes=get_dx_labels(),
                                   class_mode="categorical",
                                   batch_size=batch_size,
                                   shuffle=shuffle,
                                   seed=rnd_seed,
                                   subset=subset)


def init_image_data_generator(split=False):
    split_value = SPLIT_VALUE if split else 0.0

    return ImageDataGenerator(
            samplewise_center=True,
            samplewise_std_normalization=True,
            fill_mode='constant',
            cval=1.0,
            validation_split=split_value)


def create_model(in_shape, out_shape):
    model = Sequential()
    model.add(InceptionV3(input_shape=in_shape,
                          include_top=False,
                          weights=None))
    model.add(GlobalAveragePooling2D())

    model.add(Dense(out_shape, activation='relu'))

    model.compile(optimizer="nadam",
                  loss="categorical_crossentropy",
                  metrics=["accuracy"])
    return model


def get_date_time_str():
    return datetime.now().strftime("%Y%m%d%H%M%S")


def save_model(model, base_model_name):
    date_time = get_date_time_str()
    path = f"./models/{date_time}_{base_model_name}.h5"
    model.save(path)


def filter_on_matching(data, labels, value=1):
    """
    Filters image metadata based on binary 0 or 1 labels (diagnostic labels).

    Example:
        edema_or_mass = filter_on_matching(img_metadata, ["edema", "mass"])

        with_finding = filter_on_matching(img_metadata, ["no_finding"], value=0)

    :param data: a DataFrame containing the image metadata
    :param labels: a list of diagnostic labels to filter
    :param value: the value to filter for (0 or 1).
     Default is 1 (to include the image based on the presence
      of this diagnostic label)
    :return: a filtered DataFrame matching the given labels and value.
    """
    mask = data[labels[0]] == value
    for label in labels[1:]:
        mask = mask & (data[label] == value)
    return data[mask]


def save_to_json(dataframe, filepath, orient="index"):
    dataframe.to_json(filepath, orient=orient)
