import matplotlib.pyplot as plt
from sklearn.decomposition import PCA

def pca_reduce(data):
    pca = PCA(n_components=2)
    return pca.fit_transform(data)


def plot(data):
    plt.scatter([v[0] for v in data], [v[1] for v in data], c=[v[2] for v in data])
    plt.show()


def main():
    pass


if __name__ == "__main__":
    main()
