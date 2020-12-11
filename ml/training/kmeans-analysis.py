#%%
from sklearn.cluster import KMeans

from training.utils import load_imgs_for_kmeans

N_CLUSTERS = 13
imgs = load_imgs_for_kmeans()

kmeans = KMeans(n=N_CLUSTERS)

predictions = kmeans.fit_predict(imgs)
