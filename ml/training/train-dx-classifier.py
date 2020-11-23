from tensorflow.keras.models import load_model
from training.utils import (get_dx_labels,
                            get_img_metadata,
                            get_train_valid_test_split,
                            create_model,
                            print_gpu_status,
                            train_checkpoint_save,
                            )

print_gpu_status()

dx_labels = get_dx_labels()
print(f"Total diagnostic labels imported: {len(dx_labels)}")
img_metadata = get_img_metadata()
print(f"Total usable images: {len(img_metadata)}")

# %%
# only train on images with finding
train_df = img_metadata[img_metadata['no_finding'] < 1.]
train_gen, valid_gen, test_gen = get_train_valid_test_split(train_df)
# %%

# model = tf.keras.models.load_model("./models/20201121102739_dx-classifier.h5")

# %%
model = create_model(train_gen.image_shape, len(train_gen.class_indices))
model = train_checkpoint_save(model,
                              train_gen,
                              valid_gen,
                              model_name='dx-classifier',
                              num_epochs=100)

# %% Arbitrary test of prediction
preds = model.predict(test_gen)
for pred in preds[:5]:
    print(pred)
