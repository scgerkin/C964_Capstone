import tensorflow as tf
import tensorflow_hub as tf_hub
from training.utils import (load_dx_labels,
                            load_img_metadata,
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

# %% Load meta data, labels
dx_labels = load_dx_labels()
print(f"Total diagnostic labels imported: {len(dx_labels)}")
img_metadata = load_img_metadata()
print(f"Total usable images: {len(img_metadata)}")
img_metadata.describe()

# %% get training/validation data
training_data, validation_data = get_training_and_validation_sets(img_metadata)

## now what... I have no idea what I'm doing.
