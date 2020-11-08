import tensorflow as tf
import tensorflow_hub as tf_hub
from training.utils import (get_dx_labels,
                            get_img_metadata,
                            get_training_and_validation_sets,
                            create_model,
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

training_data, validation_data = get_training_and_validation_sets(img_metadata)
# %% This seems to be working if I can get the labels correct
from tensorflow.keras import Sequential
from tensorflow.keras.layers import (Dropout,
                                     Dense,
                                     GlobalAveragePooling2D,
                                     )

model = Sequential()
model.add(GlobalAveragePooling2D())
model.add(Dropout(0.5))
model.add(Dense(512))
model.add(Dropout(0.5))

model.add(Dense(len(training_data.class_indices), activation='sigmoid'))

model.compile(optimizer="rmsprop",
              loss="categorical_crossentropy",
              metrics=["accuracy"])

train_generator = training_data
valid_generator = validation_data

STEP_SIZE_TRAIN = train_generator.n // train_generator.batch_size
STEP_SIZE_VALID = valid_generator.n // valid_generator.batch_size
model.fit_generator(generator=train_generator,
                    steps_per_epoch=STEP_SIZE_TRAIN,
                    validation_data=valid_generator,
                    validation_steps=STEP_SIZE_VALID,
                    epochs=10)

# %%
