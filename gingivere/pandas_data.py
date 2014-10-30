from __future__ import print_function

import pandas as pd
import numpy as np

import load_raw_data
from collections import defaultdict

print(__doc__)

patients = ["Dog_1", "Dog_2", "Dog_3", "Dog_4", "Dog_5", "Patient_1", "Patient_2"]
d_keys = ['data_length_sec', 'sampling_frequency', 'sequence', 'state', 'file']

d = defaultdict(list)

for patient in patients:
    for data in load_raw_data.walk_training_mats(patient):
        for key in d_keys:
            d[key].append(data[key])
        df = pd.DataFrame(data['data'], index=data['channels'])
        name = data['file'].split('.')[0]
        print(name)
        store = pd.HDFStore("D:/gingivere/data.h5")
        store[name] = df
        store.close()

store = pd.HDFStore("D:/gingivere/data.h5")
store['master'] = pd.DataFrame(d)
store.close()

if __name__ == "__main__":
    pass
