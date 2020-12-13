# %%
from training.utils import PROJECT_DIR
import matplotlib.pyplot as plt
import pandas as pd

plt.style.use("seaborn")


def save_show(fig_name):
    path = f"{PROJECT_DIR}analysis/training/{fig_name}.png"
    plt.savefig(path)
    plt.show()


df = pd.read_csv("analysis/dx-weighted-inception.csv")
# %%
x = df["epoch"]
plt.plot(x, df["accuracy"], label="Training Accuracy")
plt.plot(x, df["val_accuracy"], label="Validation Accuracy")
plt.title("Model Accuracy per Epoch")
plt.xticks(range(0,101,10))
plt.xlabel("Epoch")
plt.ylabel("Accuracy (as decimal)")
plt.legend()
save_show("model-acc")

#%%

plt.plot(x, df["loss"], label="Training Loss")
plt.plot(x, df["val_loss"], label="Validation Loss")
plt.title("Model Loss per Epoch")
plt.xticks(range(0,101,10))
plt.xlabel("Epoch")
plt.ylabel("Loss (Categorical Cross-Entropy)")
plt.legend()
save_show("model-loss")

#%%

plt.plot(x, df["mae"], label="Training MAE")
plt.plot(x, df["val_mae"], label="Validation MAE")
plt.title("Model Mean Absolute Error per Epoch")
plt.xticks(range(0,101,10))
plt.xlabel("Epoch")
plt.ylabel("Mean Absolute Error")
plt.legend()
save_show("model-mae")
