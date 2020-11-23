#%%
from tensorflow.keras.preprocessing.image import img_to_array, load_img
from tensorflow.keras.models import load_model
import numpy as np
from training.utils import *

#%%
model = load_model("./models/20201123-115253_dx-classifier-withdroput-final.h5")

DUMMY_IMG = "00000001_001.png"
img = load_img(f"{IMG_DIR}/{DUMMY_IMG}", target_size=(256, 256), color_mode='grayscale')
img = img_to_array(img)
img = np.expand_dims(img, axis=0)
print(img.shape)

# TODO: Need to figure out the labels associated with each array index
preds = model.predict(img)

#%%
img_metadata = get_img_metadata()

filepaths = img_metadata['img_filename']
labels = img_metadata['no_finding']
#%%
combined = np.vstack((filepaths, labels))
#%%
import pandas as pd
df = pd.DataFrame()

df['filename'] = filepaths
df['no_finding'] = labels
#%%
print(len(df))