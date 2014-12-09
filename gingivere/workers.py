from multiprocessing import Pool

from gingivere.data import tuple_to_mat, generate_names
from gingivere import SETTINGS

def generate_target_data(target):
    pool = Pool(SETTINGS.N_jobs)
    results = pool.map(consume_mat, [t for t in generate_names(target)])
    return results

def consume_mat(t):
    return tuple_to_mat(t)['data']
