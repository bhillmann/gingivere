import load_raw_data as lrd
import shelve_api as sapi
from sklearn import preprocessing
import pandas as pd
import numpy as np
from joblib import Parallel, delayed
import time
import sys
import multiprocessing
import os

print(__doc__)

def preprocess_data(input):
    file, r = input
    store = pd.HDFStore(file)
    data = store['data']
    size = 20000
    num_splits = int(data.shape[1]/size)
    X = np.array([])
    for row in data:
        for x in np.array_split(row, num_splits):
            np.append(X, np.histogram(x, density=True, range=r) )
    store['X'] = np.asarray(X)
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