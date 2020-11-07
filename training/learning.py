import tensorflow as tf
import tensorflow_hub as tf_hub
from training.utils import (get_dx_labels,
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

dx_labels = get_dx_labels()
print(f"Total diagnostic labels imported: {len(dx_labels)}")
img_metadata = load_img_metadata()
print(f"Total usable images: {len(img_metadata)}")
img_metadata.describe()

training_data, validation_data = get_training_and_validation_sets(img_metadata)

# %%
import matplotlib.pyplot as plt

t_x, t_y = next(training_data)
fig, m_axs = plt.subplots(4, 4, figsize=(16, 16))
for (c_x, c_y, c_ax) in zip(t_x, t_y, m_axs.flatten()):
    c_ax.imshow(c_x[:, :, 0], cmap='bone', vmin=-1.5, vmax=1.5)
    c_ax.set_title(
            ', '.join([n_class for n_class, n_score in zip(dx_labels, c_y)
                       if n_score > 0.5]))
    c_ax.axis('off')

fig.show()