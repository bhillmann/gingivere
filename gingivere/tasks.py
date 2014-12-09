import numpy as np
import sklearn.utils
from multiprocessing import Pool

from gingivere.data import generate_mats
from gingivere import SETTINGS

def consume_mats(target, verbose=True):
    pool = Pool(SETTINGS.N_jobs)
    pool.map(consume_mat, [mat for mat in generate_mats(target)])
    return

def consume_mat(mat):
    print(mat)

