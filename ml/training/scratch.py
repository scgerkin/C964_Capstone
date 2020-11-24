#%%
from tensorflow.keras.models import load_model

from training.utils import *

#%%
model_path = "./models/20201123-120422_dx-classifier-final.h5"
model = load_model(model_path)

img = load_img_as_tensor(DUMMY_IMG)

preds = model.predict(img)


