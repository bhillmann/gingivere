import load_raw_data as lrd

import shelve_api as sapi

from sklearn import preprocessing
import pandas as pd
import numpy as np
from joblib import Parallel, delayed
import time
import sys
import multiprocessing

print(__doc__)

def process_data(input):
    data = lrd.load_mat(*input)
    name = data['file'].split('.')[0]
    print(name)
    store = pd.HDFStore("D:/gingivere/data/%s.h5" % name)
    # pp = preprocessing.scale(data['data'])
    df = pd.DataFrame(data['data'], index=data['channels'])
    del data
    store['data'] = df
    store.close()
    return np.asarray([df.values.min(), df.values.max()])

if __name__ == '__main__':
    patients = ["Dog_1", "Dog_2", "Dog_3", "Dog_4", "Dog_5", "Patient_1", "Patient_2"]
    num_cores = multiprocessing.cpu_count()
    now = time.time()
    if len(sys.argv) >= 2:
        patient = sys.argv[1]
        # res = Parallel(n_jobs=num_cores)(delayed(process_data)(i) for i in lrd.walk_files(patient))
        res = []
        for i in lrd.walk_files(patient):
            res.append(process_data(i))
        sapi.insert(res, "%s_mm" % patient)
    else:
        for patient in patients:
            res =  Parallel(n_jobs=num_cores)(delayed(process_data)(i) for i in lrd.walk_files(patient))
            sapi.insert(res, "%s_mm" % patient)
    print("Finished in", time.time()-now , "sec")
