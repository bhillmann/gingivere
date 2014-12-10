from joblib import Memory
import numpy as np
from sklearn import preprocessing

from gingivere import SETTINGS
from gingivere.data import load_mat_from_path

memory = Memory(SETTINGS.cache_dir, mmap_mode='r+')

def source(path):
    # print("Loading: %s" % path)
    return load_mat_from_path(path)['data'].values

def preprocess(origin):
    return preprocessing.scale(origin.astype('float32'))

def window(origin, size=10):
    destination = []
    for row in origin:
        for i in np.array_split(row, size):
            destination.append(i)
    return destination

def quantize(origin):
    destination = []
    for row in origin:
        hist, bin_edges = np.histogram(row, density=True)
        destination.append(hist)
    return np.asarray(destination, dtype='float32')

def flatten():
    pass

