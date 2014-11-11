import tempfile
import shutil
import os
import pandas as pd
import numpy as np

from joblib import Parallel, delayed
from joblib import load, dump

def create_feature_vector(input, output, name):
    """Compute the sum of a row in input and store it in output"""
    name = name.split('.')[0]
    data_df = input[name]
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
    output[i] = curr


if __name__ == "__main__":
    folder = tempfile.mkdtemp()
    output_name = os.path.join(folder, 'output')
    try:

        # Pre-allocate a writeable shared memory map as a container for the
        # results of the parallel computation
        output = np.memmap(output_name, shape=136, dtype='float64', mode='w+')

        store = pd.HDFStore("D:/gingivere/data.h5")
        df = store['master']

        # Fork the worker processes to perform computation concurrently
        Parallel(n_jobs=4)(delayed(create_feature_vector)(store, output, name)
                           for name in df.file)

        print("Actual sums computed by the worker processes:")
        print(output)

        assert np.allclose(expected_result, sums)
    finally:
        try:
            store.close()
            store = pd.HDFStore("D:/gingivere/data.h5")
            df = pd.DataFrame(dict)
            store['baseline'] = df
            store.close()
            shutil.rmtree(folder)
        except:
            print("Failed to delete: " + folder)
