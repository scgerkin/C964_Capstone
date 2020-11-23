from training.utils import IMG_DIR, DUMMY_IMG
from tensorflow.keras.preprocessing.image import img_to_array, load_img
from tensorflow.keras.models import load_model
import numpy as np

model = load_model("./models/20201122100101_dx-classifier.h5")
# %%
img = load_img(f"{IMG_DIR}/{DUMMY_IMG}", target_size=(256, 256), color_mode='grayscale')
img = img_to_array(img)
img = np.expand_dims(img, axis=0)
print(img.shape)
# %%
# TODO: Need to figure out the labels associated with each array index
preds = model.predict(img)

