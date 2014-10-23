import scipy.io
import json
import numpy as np
import re

import os

# from sklearn.feature_selection import SelectKBest
# from sklearn.feature_selection import chi2

def walk_files(path):
    for file in os.listdir(path):
        if 'interictal' in file:
            yield (path, file, 'interictal')
        elif 'preictal' in file:
            yield (path, file, 'preictal')
        else:
            continue

def walk_training_mats(patient):
    for data in walk_files(DATA_PATH + patient):
        path, file, state = data
        yield load_mat(path, file, state)

def load_mat(path, file, state):
    mat = scipy.io.loadmat("%s/%s" % (path, file))
    keys = ['data', 'data_length_sec', 'sampling_frequency', 'channels', 'sequence']
    number = int(re.match(r'\d+', file.split('_')[-1]).group())
    values = mat['%s_segment_%d' % (state, number)][0, 0]
    data = dict(zip(keys, values))
    # Clean the data
    for key in keys[1:]:
        data[key] = data[key].flatten()[0]
    data['channels'] = data['channels'][0]
    data['sequence'] = int(data['sequence'])
    data['data_length_sec'] = int(data['data_length_sec'])
    data['state'] = state
    data['file'] = file
    return data


def get_data_path():
    with open('config.json', 'r') as f:
        config = json.load(f)
        f.close()
    return config['data']

def get_db_path():
    with open('config.json', 'r') as f:
        config = json.load(f)
        f.close()
    return config['mongo']


DATA_PATH = get_data_path()
DB_PATH = get_db_path()

def main():
    # for data in walk_files(DATA_PATH + "Dog_2"):
    #     print(load_mat(*data))
    for data in walk_training_mats("Dog_2"):
        print(data['data'].shape)

if __name__ == "__main__":
    main()
