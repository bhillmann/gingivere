from joblib import Memory
import numpy as np
from numbapro import autojit
from sklearn import preprocessing

from gingivere import SETTINGS
from gingivere.data import load_mat_from_path

memory = Memory(SETTINGS.cache_dir, mmap_mode='r+')

def source(path):
    print("Loading: %s" % path)
    return load_mat_from_path(path)['data'].values

@memory.cache
def source_mem(path):
    return load_mat_from_path(path)['data'].values

def preprocess(origin):
    return preprocessing.scale(origin.astype('float32'))

def window(origin, size=10):
    destination = []
    for row in origin:
        destination.append(np.array_split(row, size))
    return destination

def quantize():
    pass

def flatten():
    pass

