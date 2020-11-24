# %%
from training.utils import (get_dx_labels,
                            get_img_metadata,
                            pickle_model,
                            create_binary_results_df,
                            print_metrics,
                            load_img_as_flat_array,
                            )
from sklearn.cluster import KMeans
from sklearn.model_selection import train_test_split
import numpy as np

RANDOM_SEED = 42

dx_labels = get_dx_labels()
print(f"Total diagnostic labels imported: {len(dx_labels)}")
img_metadata = get_img_metadata()
print(f"Total usable images: {len(img_metadata)}")
kmeans = KMeans(n_clusters=2, random_state=RANDOM_SEED)

train_df, test_df = train_test_split(img_metadata,
                                     test_size=0.2,
                                     random_state=RANDOM_SEED)

x_train_paths = train_df['img_filename']
y_train_labels = train_df['no_finding']
x_test_paths = test_df['img_filename']
y_test_labels = test_df['no_finding']


def load_imgs(filenames):
    print(f"Loading {len(filenames)} images.")
    arr = []
    for index, filename in enumerate(filenames):
        if index % 100 == 0:
            print(f"{round(float(index) / len(filenames) * 100., 2)}% complete")
        img = load_img_as_flat_array(filename)
        arr.append(img)
    print("Finished loading.")
    return np.array(arr)


num_samples = 100
x_train = load_imgs(x_train_paths[:num_samples])
print("Fitting model...")
kmeans_model = kmeans.fit(x_train)
print("Making predictions...")
preds = kmeans_model.predict(x_train)
results_df = create_binary_results_df(x=x_train_paths[:num_samples],
                                      y_expected=y_train_labels[:num_samples],
                                      y_prediction=preds)
pickle_model(model=kmeans_model,
             name='binary-kmeans',
             results_df=results_df)

print_metrics(results_df)
