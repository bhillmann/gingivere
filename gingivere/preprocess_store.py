import time
import sys
import multiprocessing
import os

import pandas as pd
import numpy as np
from joblib import Parallel, delayed

from tests import shelve_api as sapi


print(__doc__)

def preprocess_data(input):
    file, r = input
    store = pd.HDFStore(file)
    data = store['data']
    size = 20000
    num_splits = int(data.shape[1]/size)
    data = data.T
    X = []
    for row in data:
        for x in np.array_split(data[row], num_splits):
            hist = np.histogram(x, density=False, range=r)
            X.append(hist[0])
    store['X'] = pd.DataFrame(X, dtype='float64')
    store.close()
    print(file)
    return len(X)

def get_min_max(patient):
    mm = sapi.load("%s_mm" % patient)
    return (np.min(mm), np.max(mm))

def walk_data(patient):
    path = "D:/gingivere/data/"
    for file in os.listdir(path):
        if patient in file:
            yield path + file


if __name__ == '__main__':
    patients = ["Dog_1", "Dog_2", "Dog_3", "Dog_4", "Dog_5", "Patient_1", "Patient_2"]
    # d_keys = ['data_length_sec', 'sampling_frequency', 'sequence', 'state', 'file']
    num_cores = multiprocessing.cpu_count()
    now = time.time()
    if len(sys.argv) >= 2:
        patient = sys.argv[1]
        r = get_min_max(patient)
        res = Parallel(n_jobs=num_cores)(delayed(preprocess_data)((i, r)) for i in walk_data(patient))
        sapi.insert(res, "%s_len" % patient)
    else:
        for patient in patients:
            r = get_min_max(patient)
            res =  Parallel(n_jobs=num_cores)(delayed(preprocess_data)((i, r)) for i in walk_data(patient))
            sapi.insert(res, "%s_len" % patient)
    print("Finished in", time.time()-now , "sec")
