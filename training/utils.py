from pathlib import PurePath
import tensorflow as tf
import pandas as pd

DUMMY_IMG = "00000001_000.png"
DATASET_DIR = "../dataset/"
IMG_DIR = DATASET_DIR + "images/"


def load_img_metadata():
    path = PurePath(DATASET_DIR + "usable_img_metadata.csv")
    return pd.read_csv(str(path))


def get_tensor_and_label(img_data):
    path = PurePath(IMG_DIR + img_data["img_filename"])
    tensor = png_to_tensor(str(path))
    label = row_label(img_data)
    return tensor, label


def png_to_tensor(img_path: str, resize_height_width=None):
    if resize_height_width is None:
        resize_height_width = [256, 256]
    img = tf.io.read_file(img_path)
    img = tf.image.decode_png(img, channels=1)
    img = tf.image.convert_image_dtype(img, tf.float32)
    img = tf.image.resize(img, size=resize_height_width)
    return img


def row_label(img_data):
    dx_labels = load_dx_labels()
    return img_data[dx_labels].to_numpy()


def load_dx_labels():
    path = PurePath(DATASET_DIR + "dx_labels.csv")
    with open(path, 'r') as f:
        lines = f.readlines()[1:]
        return [line.strip() for line in lines]
