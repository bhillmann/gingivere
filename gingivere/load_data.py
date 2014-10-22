import scipy.io
import json
import numpy as np

import os

# from sklearn.feature_selection import SelectKBest
# from sklearn.feature_selection import chi2

def walk_files(path):
    for file in os.listdir(path):
        if 'interictal' in file:
            yield (file, 0)
        elif 'preictal' in file:
            yield (file, 1)


def load_mat(path, number=1, state='preictal', patient="Dog_2"):
    uniq_id = "%s_%s_segment_%04d" % (patient, state, number)
    mat = scipy.io.loadmat(path + "%s/%s.mat" % (patient, uniq_id))
    keys = ['data', 'data_length_sec', 'sampling_frequency', 'channels', 'sequence']
    values = mat['%s_segment_%d' % (state, number)][0, 0]
    data = dict(zip(keys, values))
    # Clean the data
    for key in keys[1:]:
        data[key] = data[key].flatten()
    data['state'] = state
    data['id'] = uniq_id
    return data


def get_standard_deviations(data):
    return np.std(data,axis=1)


def get_data_path():
    with open('config.json', 'r') as f:
        data_path = json.load(f)
        f.close()
    return data_path


def main():
    DATA_PATH = get_data_path()
    p = load_mat(DATA_PATH)
    i = load_mat(DATA_PATH, state='interictal')
    return p, i


if __name__ == "__main__":
    (p, i) = main()
    d = np.concatenate((p,i))
    dd = pca_reduce(d)
    dd = [np.append(v, 'y') for v in dd]
    for v in dd[16:]:
        v[2] = 'b'
    plot(dd)
