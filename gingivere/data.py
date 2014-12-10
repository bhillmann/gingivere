import scipy.io
import os
import pandas as pd

from gingivere import SETTINGS

def generate_mat_paths(target):
    folder = "%s/%s" % (SETTINGS.data_dir, target)
    for file in os.listdir(folder):
        if ".mat" in file:
            yield "%s/%s" % (folder, file)

def load_mat_from_path(path):
    mat = scipy.io.loadmat(path)
    values = mat[scipy.io.whosmat(path)[0][0]][0][0]
    keys = ['data', 'data_length_sec', 'sampling_frequency', 'channels', 'sequence']
    if 'test' in path:
        keys = keys[:-1]
    data = dict(zip(keys, values))
    # Clean the data
    for key in keys[1:]:
        if key == 'channels':
            channels = data[key][0]
            channels = [i[0] for i in channels]
            continue
        data[key] = data[key].flatten()[0]
    del data['channels']
    if 'test' not in path:
        data['sequence'] = int(data['sequence'])
    data['data_length_sec'] = int(data['data_length_sec'])
    df = pd.DataFrame(data['data'], index=channels)
    data['data'] = df
    return data

def source(path):
    return load_mat_from_path(path)['data'].values

def generate_mat_cvs(target):
    for path in generate_mat_paths(target):
        if 'test' not in path:
            yield path

def generate_mat_tests(target):
    for path in generate_mat_paths(target):
        if 'test' in path:
            yield path