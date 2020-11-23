from training.utils import (get_dx_labels,
                            get_img_metadata,
                            print_gpu_status,
                            IMG_DIR, get_date_time_str,
                            )
from sklearn.cluster import KMeans
from sklearn.model_selection import train_test_split
from skimage.transform import resize
import os
import numpy as np
from skimage import io
import pickle

RANDOM_SEED = 42

print_gpu_status()

dx_labels = get_dx_labels()
print(f"Total diagnostic labels imported: {len(dx_labels)}")
img_metadata = get_img_metadata()
print(f"Total usable images: {len(img_metadata)}")
kmeans = KMeans(n_clusters=2, random_state=RANDOM_SEED)

train_df, test_df = train_test_split(img_metadata,
                                     test_size=0.2,
                                     random_state=RANDOM_SEED)

#
x_train_paths = train_df['img_filename']
y_train_labels = train_df['no_finding']
x_test_paths = test_df['img_filename']
y_test_labels = test_df['no_finding']


def load_imgs(filenames):
    print(f"Loading {len(filenames)} images.")
    arr = []
    for index, filename in enumerate(filenames):
        if index % 1000 == 0:
            print(f"{round(float(index) / len(filenames) * 100., 2)}% complete")
        path = os.path.join(IMG_DIR, filename)
        img = io.imread(path, as_gray=True)
        img = resize(img, output_shape=(256, 256))
        img = img.flatten()
        arr.append(img)
    print("Finished loading.")
    return np.array(arr)


# %%
x_train = load_imgs(x_train_paths)
print("Fitting model...")
kmeans_model = kmeans.fit(x_train)
print("Done fitting model.")
filename = f"./models/{get_date_time_str()}-binary-kmeans.pkl"
with open(filename, 'wb') as file:
    pickle.dump(kmeans_model, file)
print("Model saved.")
