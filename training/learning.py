import tensorflow as tf
import tensorflow_hub as tf_hub
from training.utils import (get_dx_labels,
                            get_img_metadata,
                            get_training_and_validation_sets,
                            )

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
img_metadata.describe()


def create_model(in_shape, out_shape):
    from tensorflow.keras import Sequential
    from tensorflow.keras.applications.inception_v3 import InceptionV3
    from tensorflow.keras.layers import (Dropout,
                                         Dense,
                                         GlobalAveragePooling2D,
                                         )
    model = Sequential()
    model.add(InceptionV3(input_shape=in_shape,
                          include_top=False,
                          weights=None))
    model.add(GlobalAveragePooling2D())
    model.add(Dropout(0.5))
    model.add(Dense(512))
    model.add(Dropout(0.5))

    model.add(Dense(out_shape, activation='sigmoid'))

    model.compile(optimizer="rmsprop",
                  loss="categorical_crossentropy",
                  metrics=["accuracy"])
    return model


# %% Fit model
train_gen, valid_gen = get_training_and_validation_sets(img_metadata)

model = create_model(train_gen.image_shape, len(train_gen.class_indices))
STEP_SIZE_TRAIN = train_gen.n // train_gen.batch_size
STEP_SIZE_VALID = valid_gen.n // valid_gen.batch_size
model.fit_generator(generator=train_gen,
                    steps_per_epoch=STEP_SIZE_TRAIN,
                    validation_data=valid_gen,
                    validation_steps=STEP_SIZE_VALID,
                    epochs=10)

# %% Arbitrary test of prediction
preds = model.predict(valid_gen)
for pred in preds[:5]:
    print(pred)


# %%
def save_model(model, base_model_name="InceptionV3"):
    from datetime import datetime
    date_time = datetime.now().strftime("%Y%m%d%H%M%S")
    path = f"./models/{date_time}_{base_model_name}.h5"
    model.save(path)


save_model(model)
