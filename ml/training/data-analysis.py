# %%
import pandas as pd
from training.utils import get_img_metadata, get_dx_labels
import matplotlib.pyplot as plt

plt.style.use("seaborn-poster")

trimmed = pd.read_csv("training/train_data.csv")
original = get_img_metadata()
dx_labels = get_dx_labels()
dx_counts = {}
for label in dx_labels:
    dx_counts[label] = len(original[original[label] > 0.5])
# %%
plt.figure(figsize=(20, 10))
plt.barh(dx_labels, list(dx_counts.values()), align="center")
plt.show()
