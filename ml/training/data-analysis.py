# %%
from copy import deepcopy
import pandas as pd
from training.utils import get_img_metadata, get_dx_labels, PROJECT_DIR
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import seaborn as sns

plt.style.use("seaborn-poster")
sns.set_style("darkgrid")
sns.set_theme(palette="Set2")


def save_show(fig_name):
    path = f"{PROJECT_DIR}analysis/data/{fig_name}.png"
    plt.savefig(path)
    plt.show()


trimmed = pd.read_csv("training/train_data.csv")
original = get_img_metadata()
dx_labels = get_dx_labels()
training_dx_labels = deepcopy(dx_labels)
training_dx_labels.remove("hernia")
training_dx_labels.remove("pneumonia")

# %%
images_by_set = pd.melt(trimmed, id_vars=["split_set"],
                        value_vars=training_dx_labels,
                        var_name="Classification", value_name="Count")
images_by_set = images_by_set.loc[images_by_set.Count > 0]

plt.figure(figsize=(21, 10))
sns.countplot(y="Classification", hue="split_set", data=images_by_set,
              order=images_by_set["Classification"].value_counts().index)
plt.legend(bbox_to_anchor=(1.0, 0), loc=2, borderaxespad=0.0)
plt.title("Image classification by usage split")
plt.xlabel("Count")
save_show("classification-by-split")
# %%
only_dx_by_sex = pd.melt(original.drop(["no_finding"], axis=1),
                         id_vars=["pt_sex"],
                         value_vars=[lbl for lbl in dx_labels if
                                     lbl != "no_finding"],
                         var_name="Classification",
                         value_name="Count")
only_dx_by_sex = only_dx_by_sex.loc[only_dx_by_sex.Count > 0]

plt.figure(figsize=(14, 8))
gs = gridspec.GridSpec(14, 1)
ax1 = plt.subplot(gs[:12, :])
ax2 = plt.subplot(gs[13, :])

sns.countplot(y="Classification",
              hue="pt_sex",
              data=only_dx_by_sex,
              order=only_dx_by_sex["Classification"].value_counts().index,
              ax=ax1)
ax1.set(xlabel="", ylabel="Classification")
ax1.set_title("Image Classification by patient sex")
only_no_finding_by_sex = pd.melt(original[["pt_sex", "no_finding"]],
                                 id_vars=["pt_sex"],
                                 value_vars=["no_finding"],
                                 var_name="No Finding", value_name="Count")
only_no_finding_by_sex = only_no_finding_by_sex.loc[
    only_no_finding_by_sex.Count > 0]
sns.countplot(y="No Finding",
              hue="pt_sex",
              data=only_no_finding_by_sex,
              order=only_no_finding_by_sex["No Finding"].value_counts().index,
              ax=ax2)
ax2.legend("")
ax2.set(xlabel="Count", ylabel="")
save_show("classification-by-sex")

# %%
markers = ["o", "v", "^", "<", ">", "1", "2", "3", "4", "*", "x", "p", "h", "D"]
fig, ax = plt.subplots(figsize=(8, 8))
lbls = [lbl for lbl in dx_labels if lbl != "no_finding"]
for label, marker in zip(lbls, markers):
    counts = original[original[label] > 0]["pt_age"].value_counts()
    sns.scatterplot(x=counts.index,
                    y=counts.values,
                    label=label,
                    marker=marker,
                    alpha=1,
                    s=70, ax=ax)
plt.title("Diagnostic Frequency by Age")
plt.xlabel("Age")
plt.xticks(ticks=range(0, 100, 10))
plt.ylabel("Frequency")
save_show("dx-freq-by-age")
# %%
row = col = 0
fig, axes = plt.subplots(7, 2, sharex="all", figsize=(8, 9))

for label, marker in zip(lbls, markers):
    ax = axes[row, col]
    ax.set_title(label)
    ax.set_xticks(range(0, 100, 10))

    counts = original[original[label] > 0]["pt_age"].value_counts()
    sns.scatterplot(x=counts.index,
                    y=counts.values,
                    marker=marker,
                    alpha=1,
                    s=35, ax=ax)
    col = (col + 1) % 2
    if col == 0:
        row = (row + 1) % 7
fig.subplots_adjust(hspace=0.6)
fig.suptitle("Individual Diagnostic Frequencies by Age")
fig.text(0.5, 0.04, "Age", ha="center", va="center")
fig.text(0.05, 0.5, "Frequency", ha="center", va="center", rotation="vertical")
save_show("indiv-dx-by-age")

# %%
plt.clf()
plt.figure(figsize=(15,10))
lbls = [lbl for lbl in dx_labels if lbl != "no_finding"]
correlation = original[lbls].corr()
correlation = correlation.mask(lambda x: x == 1)
# correlation.style.set_precision(2)
g = sns.heatmap(correlation, annot=True, linewidths=0.25,
                cmap="coolwarm")
g.set_title("Diagnosis Correlation Matrix")
g.set_xticklabels(lbls, rotation=30, ha="right")
save_show("dx-corr-matrix")
