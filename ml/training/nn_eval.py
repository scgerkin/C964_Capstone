# %%
import pandas as pd
from training.utils import get_img_metadata
from sklearn.metrics import roc_curve, auc
import matplotlib.pyplot as plt
import json

files = ["train", "valid", "test"]

for file in files:
    file_prefix = "analysis/"
    in_file = f"{file_prefix}{file}_preds.csv"

    actual = pd.read_csv(in_file)
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
    results = {}
    for label in expect.columns:
        fpr, tpr, _ = roc_curve(y_score=actual[label], y_true=expect[label])
        area = auc(fpr, tpr)
        results[label] = {"fpr": fpr.tolist(), "tpr": tpr.tolist(), "auc": area}

        c_ax.plot(fpr, tpr, label="%s (AUC:%0.2f)" % (label, area))
    c_ax.legend()
    c_ax.set_xlabel("False positive rate")
    c_ax.set_ylabel("True positive rate")
    fig.savefig(f"{file_prefix}{file}.png")

    with open(f"{file_prefix}{file}_roc.json", "w") as f:
        json.dump(results, f)
