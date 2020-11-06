import tensorflow as tf
import tensorflow_hub as tf_hub
from training.utils import (load_dx_labels,
                            load_img_metadata,
                            get_training_and_validation_sets,
                            create_model
                            )

print(f"TensorFlow version: {tf.__version__}")
print(f"TensorFlow Hub version: {tf_hub.__version__}")
gpu_data = tf.config.list_physical_devices("GPU")
if gpu_data:
    print(f"GPU is available for training.\nTotal GPUs: {len(gpu_data)}")
else:
    print("WARNING: GPU is not available for training!")

# %% Load meta data, labels
dx_labels = load_dx_labels()
print(f"Total diagnostic labels imported: {len(dx_labels)}")
img_metadata = load_img_metadata()
print(f"Total usable images: {len(img_metadata)}")
img_metadata.describe()

#%% get training/validation data
training_data, validation_data = get_training_and_validation_sets(img_metadata)

#%% get model
model = create_model()
model.summary()
#%%
early_stop = tf.keras.callbacks.EarlyStopping(monitor="val_accuracy",
                                              patience=3)
EPOCHS = 100
model.fit(x=training_data,
          epochs=EPOCHS,
          validation_data=validation_data,
          validation_freq=1,
          callbacks=[early_stop])

