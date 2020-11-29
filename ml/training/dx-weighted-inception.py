# %%
from training.utils import *

img_metadata = get_img_metadata()
single_finding_records = img_metadata[
    img_metadata["findings_list"].apply(lambda val: len(val) == 1)]
#%%
print(single_finding_records.describe())
