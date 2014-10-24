from sklearn.decomposition import RandomizedPCA

import load_data

data = load_data.load_shelve('test')
X = data['data']

def get_variance(n_components, X):
    pca = RandomizedPCA(n_components=n_components, whiten=True)
    pca.fit(X)
    print(pca.explained_variance_ratio_)
    return pca.explained_variance_ratio_
