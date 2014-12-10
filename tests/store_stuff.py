import pandas as pd
import numpy as np
from numpy import linalg as LA
from scipy import stats

store = pd.HDFStore("D:/gingivere/data.h5")
df = store['master']

dict = {}

for name in df.file:
    name = name.split('.')[0]
    data_df = store[name]
    data_df = data_df.astype('float64')
    data_df = data_df.T
    corr = data_df.corr()
    vs = data_df.apply
    ds = data_df.apply
    f_val, p_val = stats.f_oneway(*data_df.T.values)


    curr = np.concatenate((vs, ds, [f_val, p_val]))
    dict[name] = curr

    print(name)

df = pd.DataFrame(dict)
store['baseline'] = df
store.close()
