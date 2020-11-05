import tensorflow as tf
import tensorflow_hub as tf_hub

import training.utils as utils

print(f"TensorFlow version: {tf.__version__}")
print(f"TensorFlow Hub version: {tf_hub.__version__}")
gpu_data = tf.config.list_physical_devices("GPU")
if gpu_data:
    print(f"GPU is available for training.\nTotal GPUs: {len(gpu_data)}")
else:
    print("WARNING: GPU is not available for training!")

#%% Load meta data, labels
dx_labels = utils.load_dx_labels()
print(f"Total diagnostic labels imported: {len(dx_labels)}")
img_metadata = utils.load_img_metadata()
print(f"Total usable images: {len(img_metadata)}")
img_metadata.describe()

#%% check data conversion
tensor, label = utils.get_tensor_and_label(img_metadata.loc[0])


