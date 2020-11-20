import tensorflow as tf
import tensorflow_hub as tf_hub
from training.utils import (get_dx_labels,
                            get_img_metadata,
                            get_train_valid_test_split,
                            )
from tensorflow.keras import Sequential
from tensorflow.keras.applications.inception_v3 import InceptionV3
from tensorflow.keras.layers import (Dropout,
                                     Dense,
                                     GlobalAveragePooling2D,
                                     )
from tensorflow.keras.callbacks import ModelCheckpoint, CSVLogger, EarlyStopping

from datetime import datetime

print(f"TensorFlow version: {tf.__version__}")
print(f"TensorFlow Hub version: {tf_hub.__version__}")
gpu_data = tf.config.list_physical_devices("GPU")
if gpu_data:
    print(f"GPU is available for training.\nTotal GPUs: {len(gpu_data)}")
else:
    print("WARNING: GPU is not available for training!")

dx_labels = get_dx_labels()
print(f"Total diagnostic labels imported: {len(dx_labels)}")
img_metadata = get_img_metadata()
print(f"Total usable images: {len(img_metadata)}")


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


def save_model(model, base_model_name="InceptionV3"):
    date_time = get_date_time_str()
    path = f"./models/{date_time}_{base_model_name}.h5"
    model.save(path)


def train_checkpoint_save(model, train_gen, valid_gen, num_epochs=10):
    dt = get_date_time_str()
    checkpoint_fp = f"./checkpoints/{dt}.h5"
    checkpoint_cb = ModelCheckpoint(checkpoint_fp,
                                    save_freq="epoch",
                                    monitor="val_loss",
                                    save_best_only=True)

    csv_fp = f"./logs/{dt}.csv"
    csv_cb = CSVLogger(csv_fp)

    early_stop_cb = EarlyStopping(monitor="val_loss", patience=5, mode="min")

    callbacks = [checkpoint_cb, csv_cb, early_stop_cb]
    STEP_SIZE_TRAIN = train_gen.n // train_gen.batch_size
    STEP_SIZE_VALID = valid_gen.n // valid_gen.batch_size
    model.fit_generator(generator=train_gen,
                        steps_per_epoch=STEP_SIZE_TRAIN,
                        validation_data=valid_gen,
                        validation_steps=STEP_SIZE_VALID,
                        epochs=num_epochs,
                        callbacks=callbacks)

    model = tf.keras.models.load_model(checkpoint_fp)
    save_model(model)
    return model


# %%
train_gen, valid_gen, test_gen = get_train_valid_test_split(img_metadata)

# %%
model = create_model(train_gen.image_shape, len(train_gen.class_indices))
train_checkpoint_save(model, train_gen, valid_gen, num_epochs=100)

# %% Arbitrary test of prediction
preds = model.predict(test_gen)
for pred in preds[:5]:
    print(pred)