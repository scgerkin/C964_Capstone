# %%
from training.utils import RND_SEED, PROJECT_DIR, load_imgs_for_kmeans
import pickle
from sklearn.cluster import MiniBatchKMeans
from sklearn.metrics import silhouette_score
import matplotlib.pyplot as plt

score_fp = PROJECT_DIR + f"models/kmeans/silhouette_score.csv"
with open(score_fp, "w") as f:
    f.write("n_clusters,inertia,silhouette_score\n")


def pickle_model(model, n_clusters, s_score):
    fp = PROJECT_DIR + f"models/kmeans/{n_clusters}.pkl"
    with open(fp, "wb") as file:
        pickle.dump(model, file)
    with open(score_fp, "a") as file:
        file.write(f"{n_clusters},{model.inertia_},{s_score}\n")


imgs, _, _ = load_imgs_for_kmeans()

models = []
inertias = []
scores = []

for k in range(2, 101):
    print(f"Creating KMeans for {k} clusters")
    kmeans = MiniBatchKMeans(n_clusters=k, random_state=RND_SEED).fit(imgs)
    models.append(kmeans)
    score = silhouette_score(imgs, kmeans.labels_)
    scores.append(score)
    inertias.append(kmeans.inertia_)
    pickle_model(kmeans, k, score)


def plot_and_save(x, y, y_label, fig_size):
    plt.figure(figsize=fig_size)
    plt.plot(x, y, "bo-")
    plt.xlabel("$k$", fontsize=14)
    plt.ylabel(y_label, fontsize=14)
    plt.axis([1, max(x), min(y), max(y)])
    plt.savefig(f"analysis/KMeans-{y_label}.png")
    plt.show()


plot_and_save(range(2, 101), inertias, "Inertia", fig_size=(12, 6))
plot_and_save(range(2, 101), scores, "Silhouette score", fig_size=(12, 6))
