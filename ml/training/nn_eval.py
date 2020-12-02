# %%
import pandas as pd
from training.utils import get_img_metadata
from sklearn.metrics import roc_curve, auc
import matplotlib.pyplot as plt

actual = pd.read_csv("valid_preds.csv")
actual = actual.sort_values(by="filename")

expect = get_img_metadata()
expect = expect[expect["img_filename"].isin(actual["filename"])]
expect = expect.rename(columns={"img_filename": "filename"})
unused = []
for lbl in expect.columns:
    if lbl not in actual.columns:
        unused.append(lbl)
expect = expect.drop(columns=unused, axis=1)
expect = expect.sort_values(by="filename")

actual = actual.set_index("filename", drop=True)
expect = expect.set_index("filename", drop=True)

fig, c_ax = plt.subplots(1, 1, figsize=(9, 9))
for label in expect.columns:
    fpr, tpr, _ = roc_curve(y_score=actual[label], y_true=expect[label])
    area = auc(fpr, tpr)

    c_ax.plot(fpr, tpr, label="%s (AUC:%0.2f)" % (label, area))
c_ax.legend()
c_ax.set_xlabel("False positive rate")
c_ax.set_ylabel("True positive rate")
fig.show()
