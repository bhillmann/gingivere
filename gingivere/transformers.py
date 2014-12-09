from joblib import Memory
from numbapro import autojit

from gingivere import SETTINGS
from gingivere.data import load_mat_from_path

memory = Memory(SETTINGS.cache_dir, mmap_mode='r+')

def source(path):
    return load_mat_from_path(path)['data'].values

@memory.cache
def source_mem(path):
    return load_mat_from_path(path)['data'].values

def windower(size=75):
    pass

