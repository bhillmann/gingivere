import scipy.io
import json
from sklearn.decomposition import PCA
import numpy as np
import matplotlib.pyplot as plt

#
# from sklearn.feature_selection import SelectKBest
# from sklearn.feature_selection import chi2
#
# import tables


def load_mat(path, number=1, state='preictal'):
    mat = scipy.io.loadmat(path + "Dog_22/Dog_2_%s_segment_%04d.mat" % (state, number))
    xx = mat['%s_segment_%d' % (state, number)][0, 0]
    data = xx[0]
    data_length_sec = xx[1]
    sampling_frequency = xx[2]

    channels = xx[3]
    # Clean the channels
    channels = [x[0] for x in channels[0]]
    sequence = xx[4]
    return data


def pca_reduce(data):
    pca = PCA(n_components=2)
    return pca.fit_transform(data)


def plot(data):
    plt.scatter([v[0] for v in data], [v[1] for v in data], c=[v[2] for v in data])
    plt.show()


def main():
    with open('config.json', 'r') as f:
        DATA_PATH = json.load(f)
        f.close()
    p = load_mat(DATA_PATH)
    i = load_mat(DATA_PATH, state='interictal')
    return p, i
    #  = pca_reduce(data)
    # return xx


if __name__ == "__main__":
    (p, i) = main()
    d = np.concatenate((p,i))
    dd = pca_reduce(d)
    dd = [np.append(v, 'y') for v in dd]
    for v in dd[16:]:
        v[2] = 'b'
    plot(dd)