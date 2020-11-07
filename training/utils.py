from pathlib import PurePath
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import pandas as pd
import numpy as np

DUMMY_IMG = "00000001_000.png"
PROJECT_DIR = "W:/WGU/C964_Capstone/project/"
DATASET_DIR = PROJECT_DIR + "dataset/"
IMG_DIR = DATASET_DIR + "images"
IMG_SIZE = 256
TRAINING_SIZE = 100
BATCH_SIZE = 32
RND_SEED = 8
IMG_CHANNELS = 1
TEST_SIZE = 0.2

SPLIT_VALUE = 0.2
IMG_GEN_WITH_SPLIT = None

DX_LABELS = None    # cache dx labels


def get_img_metadata():
    path = PurePath(DATASET_DIR + "usable_img_metadata.csv")
    data = pd.read_csv(str(path))
    data["dx_labels"] = data["dx_labels"].map(
            lambda val: np.fromstring(val[1:-1], dtype=int, sep=" "))
    return data


def get_dx_labels():
    global DX_LABELS
    if DX_LABELS is not None:
        return DX_LABELS
    path = PurePath(DATASET_DIR + "dx_labels.csv")
    with open(path, 'r') as f:
        lines = f.readlines()[1:]
        DX_LABELS = [line.strip() for line in lines]
        return DX_LABELS


def get_training_and_validation_sets(img_data, num_images=TRAINING_SIZE):
    """
    TODO: Will need to shuffle DF before using methods below if I want to keep
        this signature the same and use it without thinking about it by only
        changing the global for training size
    :param img_data:
    :param num_images:
    :return:
    """
    training_data = get_data_batch(img_data[:num_images], subset="training")
    validation_data = get_data_batch(img_data[:num_images], subset="validation")
    return training_data, validation_data


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
    # TODO: Fix classes to have the actual labels instead of the raw input
    return idg.flow_from_dataframe(img_metadata,
                                   directory=str(PurePath(IMG_DIR)),
                                   x_col="img_filename",
                                   y_col="dx_labels",
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
            # samplewise_center=True,
            # samplewise_std_normalization=True,
            # horizontal_flip=True,
            # vertical_flip=False,
            # height_shift_range=0.05,
            # width_shift_range=0.1,
            # rotation_range=5,
            # shear_range=0.1,
            # fill_mode='reflect',
            # zoom_range=0.15,
            rescale=1. / 255,
            validation_split=split_value)


def create_model():
    pass
