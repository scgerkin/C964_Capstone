#%%
from training.utils import get_img_metadata, get_train_valid_test_split

img_metadata = get_img_metadata()

train, valid, test = get_train_valid_test_split(img_metadata)

print(train.image_shape)
