import load_raw_data as lrd

import pandas as pd
import numpy as np
from joblib import Parallel, delayed
import time
import sys

print(__doc__)

def process_data(input):
    data = lrd.load_mat(*input)
    store =

    return res

if __name__ == '__main__':
    patients = ["Dog_1", "Dog_2", "Dog_3", "Dog_4", "Dog_5", "Patient_1", "Patient_2"]
    d_keys = ['data_length_sec', 'sampling_frequency', 'sequence', 'state', 'file']

    now = time.time()
    if len(sys.argv) >= 2:
        patient = sys.argv[1]
        res = Parallel(n_jobs=8)(delayed(process_data)(i) for i in lrd.walk_files(patient))
    else:
        res = [check_paths(Path(points)) for points in b]
    print "Finished in", time.time()-now , "sec"
