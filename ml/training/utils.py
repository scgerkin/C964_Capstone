import os
from copy import deepcopy
from pathlib import PurePath
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import pandas as pd
from tensorflow.keras.preprocessing.image import img_to_array, load_img
from numpy import expand_dims

DUMMY_IMG = "00000001_000.png"
PROJECT_DIR = "W:/WGU/C964_Capstone/project/ml/"
DATASET_DIR = PROJECT_DIR + "dataset/"
IMG_DIR = DATASET_DIR + "images"

Y_COL_NAME = "findings_list"
IMG_SIZE = 256
RND_SEED = 8
IMG_CHANNELS = 1

SPLIT_VALUE = 0.15


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


def init_image_data_generator(split=False):
    split_value = SPLIT_VALUE if split else 0.0
    return ImageDataGenerator(
            samplewise_center=True,
            samplewise_std_normalization=True,
            fill_mode='constant',
            cval=1.0,
            validation_split=split_value)


def load_imgs_for_kmeans():
    idg = init_image_data_generator()
    imgs = []
    img_data = pd.read_csv("training/train_data.csv")
    img_data = img_data[img_data["split_set"] == "training"]
    num_imgs = len(img_data.index)
    for i, filename in enumerate(img_data["img_filename"]):
        if i % 100 == 0:
            print(f"Loading {i} of {num_imgs}")
        filepath = os.path.join(IMG_DIR, filename)
        img = load_img(filepath, target_size=(256, 256),
                       color_mode='grayscale')
        img = img_to_array(img)
        img = expand_dims(img, axis=0)
        img = idg.flow(img)
        img = next(img)
        img = img.flatten()
        imgs.append(img)

    lbls = deepcopy(get_dx_labels())
    lbls.remove("hernia")
    lbls.remove("pneumonia")

    def lbl_index(row):
        for index, lbl in enumerate(lbls):
            if row[lbl] > 0.5:
                return index
        raise Exception(f"Could not determine row label index for {row}")

    return imgs, img_data.apply(lbl_index, axis=1).to_numpy(), lbls
