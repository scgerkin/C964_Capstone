import os
import tensorflow as tf
from pathlib import PurePath
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from sklearn.model_selection import train_test_split
import pandas as pd
from tensorflow.keras.applications.inception_v3 import InceptionV3
from tensorflow.keras import Sequential
from tensorflow.keras.layers import (Dense,
                                     GlobalAveragePooling2D,
                                     )
from tensorflow.keras.callbacks import ModelCheckpoint, CSVLogger
from datetime import datetime
import pickle
from tensorflow.keras.preprocessing.image import img_to_array, load_img
from numpy import expand_dims
from sklearn.metrics import (confusion_matrix,
                             precision_score,
                             recall_score,
                             f1_score,
                             )

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
    model.add(Dense(512))
    model.add(Dense(out_shape, activation='sigmoid'))

    optimizer = tf.keras.optimizers.Nadam(learning_rate=0.01, )
    model.compile(optimizer=optimizer,
                  loss="categorical_crossentropy",
                  metrics=["accuracy", "mae"])
    return model


def get_date_time_str():
    return datetime.now().strftime("%Y%m%d-%H%M%S")


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


def create_binary_results_df(x, y_expected, y_prediction):
    df = pd.DataFrame()
    df["x"] = x
    df["y_expected"] = y_expected
    df["y_prediction"] = y_prediction
    df['confusion'] = df.apply(
            lambda s: determine_confusion(s['y_expected'], s['y_prediction']),
            axis=1)

    return df


def pickle_model(model, name, results_df):
    date_time = get_date_time_str()
    n_samp = len(results_df)

    base_filename = f"./models/{date_time}-{n_samp}-{name}"

    pkl_filename = base_filename + ".pkl"
    csv_filename = base_filename + ".csv"

    print(f"Saving model to {base_filename}")

    with open(pkl_filename, 'wb') as f:
        pickle.dump(model, f)

    results_df.to_csv(csv_filename, index=False)
    print("Model saved.")


def determine_confusion(expected, actual):
    if expected == 1:
        if expected == actual:
            return "TP"
        else:
            return "FN"
    else:
        if expected == actual:
            return "TN"
        else:
            return "FP"


def load_img_as_array(filename):
    filepath = os.path.join(IMG_DIR, filename)
    img = load_img(filepath, target_size=(256, 256), color_mode='grayscale')
    img = img_to_array(img)
    return img


def load_img_as_flat_array(filename):
    img = load_img_as_array(filename)
    img = img.flatten()
    return img


def load_img_as_tensor(filename):
    img = load_img_as_array(filename)
    img = expand_dims(img, axis=0)
    return img


def print_metrics(results):
    exp, act = results["y_expected"], results["y_prediction"]

    precision = round(precision_score(exp, act) * 100, 2)
    recall = round(recall_score(exp, act) * 100, 2)
    f1 = round(f1_score(exp, act) * 100, 2)
    cf = confusion_matrix(exp, act)

    print(f"Precision: {precision}\tRecall: {recall}\tF1: {f1}")
    print("Confusion Matrix:")
    print(f"TN: {cf[0][0]}\tFP: {cf[0][1]}")
    print(f"FN: {cf[1][0]}\tTP: {cf[1][1]}")


def load_imgs_for_kmeans():
    idg = init_image_data_generator()
    imgs = []
    with open("analysis/trainfiles.txt", "r") as f:
        for i, filename in enumerate(f.read().split("\n")):
            if i % 100 == 0:
                print(f"{i}")
            filepath = os.path.join(IMG_DIR, filename)
            img = load_img(filepath, target_size=(256, 256),
                           color_mode='grayscale')
            img = img_to_array(img)
            img = expand_dims(img, axis=0)
            img = idg.flow(img)
            img = next(img)
            img = img.flatten()
            imgs.append(img)
    return imgs