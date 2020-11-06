from pathlib import PurePath
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import pandas as pd
from sklearn.model_selection import train_test_split

DUMMY_IMG = "00000001_000.png"
PROJECT_DIR = "W:/WGU/C964_Capstone/project/"
DATASET_DIR = PROJECT_DIR + "dataset/"
IMG_DIR = DATASET_DIR + "images/"
IMG_SIZE = 256
TRAINING_SIZE = 100
BATCH_SIZE = 32
RND_SEED = 8
IMG_CHANNEL = 1
TEST_SIZE = 0.2

DX_LABELS = None  # cache diagnostic labels


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
        resize_height_width = [IMG_SIZE, IMG_SIZE]
    img = tf.io.read_file(img_path)
    img = tf.image.decode_png(img, channels=IMG_CHANNEL)
    img = tf.image.convert_image_dtype(img, tf.float32)
    img = tf.image.resize(img, size=resize_height_width)
    return img


def convert_filepath_and_label_to_tensor_data(img_path, labels):
    img = png_to_tensor(img_path)
    return img, labels


def row_label(img_data):
    dx_labels = load_dx_labels()
    return img_data[dx_labels].to_numpy()


def load_dx_labels():
    if DX_LABELS is not None:
        return DX_LABELS
    path = PurePath(DATASET_DIR + "dx_labels.csv")
    with open(path, 'r') as f:
        lines = f.readlines()[1:]
        return [line.strip() for line in lines]


def get_training_and_validation_sets(img_data, num_images=TRAINING_SIZE):
    filenames = []
    for filename in img_data[:num_images]["img_filename"]:
        filenames.append(IMG_DIR + filename)

    dx_labels = load_dx_labels()
    labels = img_data[:num_images][dx_labels].to_numpy()

    x_train, x_val, y_train, y_val = train_test_split(filenames,
                                                      labels,
                                                      test_size=TEST_SIZE,
                                                      random_state=RND_SEED)

    training_data = create_data_batches(filepaths=x_train,
                                        labels=y_train,
                                        test_data=False,
                                        shuffle=False)
    validation_data = create_data_batches(filepaths=x_val,
                                          labels=y_val,
                                          test_data=False,
                                          shuffle=False)
    return training_data, validation_data


def create_data_batches(filepaths,
                        labels=None,
                        test_data=False,
                        shuffle=False):
    if test_data:
        return tf.data.Dataset \
            .from_tensor_slices((tf.constant(filepaths))) \
            .map(png_to_tensor) \
            .batch(BATCH_SIZE)
    else:
        data = tf.data.Dataset.from_tensor_slices((tf.constant(filepaths),
                                                   tf.constant(labels)))
        if shuffle:
            data.shuffle(buffer_size=len(filepaths))

        return data \
            .map(convert_filepath_and_label_to_tensor_data) \
            .batch(BATCH_SIZE)


MODEL_URL = "https://tfhub.dev/google/imagenet/inception_v3/classification/4"


def create_model(model_url=None):
    # TODO: in_shape is very rigid for this model, will need to find a different
    #  model that can take channel 1
    in_shape = (None, IMG_SIZE, IMG_SIZE, IMG_CHANNEL)
    out_shape = len(load_dx_labels())
    if model_url is None:
        model_url = MODEL_URL

    model = keras.Sequential(
            [
                layers.Dense(2, activation="relu", name="layer1"),
                layers.Dense(3, activation="relu", name="layer2"),
                layers.Dense(4, name="layer3"),
                ])

    model.compile(loss=tf.keras.losses.CategoricalCrossentropy(),
                  optimizer=tf.keras.optimizers.Adam(),
                  metrics=["accuracy"]
                  )

    # Build the model
    # model.build(input_shape=in_shape)

    return model
