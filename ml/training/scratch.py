#%%
from tensorflow.keras.models import load_model
from training.utils import *
import tensorflow as tf

#%%
saved_model_path = "./models/20201123-120422_dx-classifier-final.h5"
model = load_model(saved_model_path)

img = load_img_as_tensor(DUMMY_IMG)

preds = model.predict(img)
#%%
model_version = "01"
model_name = "dx-classifier"
model_path = f"{PROJECT_DIR}models/save/{model_name}/{model_version}"

tf.saved_model.save(model, model_path)