import pandas as pd
import numpy as np

store = pd.HDFStore("D:/gingivere/data.h5")
df = store['master']

dict = {}

#parallelize this for loop
for name in df.file:
    name = name.split('.')[0]
    data_df = store[name]
    data_df = data_df.astype('float64')
    data_df = data_df.T
    corr = data_df.corr()
    vs = []
    corrs = []
    for i in range(16):
        vs.append(data_df.icol(i).var())
        for j in range(i, 16):
            if j == i:
                continue
            else:
                corrs.append(corr.ix[i,j])
    curr = np.array(vs + corrs, dtype='float64')
    dict[name] = curr
    print(name)

df = pd.DataFrame(dict)
store['baseline'] = df
store.close()
