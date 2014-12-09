from multiprocessing import Pool

from gingivere.data import tuple_to_mat, generate_names
from gingivere import SETTINGS

def generate_target_data(target, verbose=True):
    pool = Pool(SETTINGS.N_jobs)
    pool.map(consume_mat, [t for t in generate_names(target)])
    return

def consume_mat(t):
    tuple_to_mat(t)
    print("Read")