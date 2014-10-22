import matplotlib.pyplot as plt
from sklearn.decomposition import PCA

def pca_reduce(data):
    pca = PCA(n_components=2)
    return pca.fit_transform(data)


def plot(data):
    plt.scatter([v[0] for v in data], [v[1] for v in data], c=[v[2] for v in data])
    plt.show()


def main():
    data_path = get_data_path()
    p = load_mat(data_path)
    i = load_mat(data_path, state='interictal')
    d = np.concatenate((p,i))
    dd = pca_reduce(d)
    dd = [np.append(v, 'y') for v in dd]
    for v in dd[16:]:
        v[2] = 'b'
    plot(dd)


if __name__ == "__main__":
    main()
