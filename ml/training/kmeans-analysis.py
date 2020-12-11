# %%
import seaborn as sn
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.metrics import (precision_score,
                             recall_score,
                             f1_score,
                             confusion_matrix,
                             )

from training.utils import load_imgs_for_kmeans

N_CLUSTERS = 13

x, y, lbls = load_imgs_for_kmeans()

kmeans = KMeans(n_clusters=N_CLUSTERS)
print("Fitting and predicting...")
predictions = kmeans.fit_predict(x)

precision = round(precision_score(y, predictions, average="micro") * 100, 2)
recall = round(recall_score(y, predictions, average="micro") * 100, 2)
f1 = round(f1_score(y, predictions, average="micro") * 100, 2)
cf = confusion_matrix(y, predictions)

metric_txt = f"Precision: {precision}%\nRecall: {recall}%\nF1: {f1}%"
plt.figure(figsize=(15, 15))
plt.text(0, 0, metric_txt)
g = sn.heatmap(cf, annot=True, linewidths=0.25)
g.set_title("Label Classification Confusion Matrix")
g.set_xlabel("Prediction Label")
g.set_ylabel("True Label")
g.set_yticklabels(lbls, rotation=0)
g.set_xticklabels(lbls, rotation=45, ha="right")
plt.savefig("analysis/kmeans-cf-matrix.png")
plt.show()
