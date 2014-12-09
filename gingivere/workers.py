from multiprocessing import Pool

from gingivere.data import generate_paths
from gingivere import SETTINGS

def generate_target_data(target):
    pool = Pool(SETTINGS.N_jobs)
    results = pool.map(consume_mat, [t for t in generate_names(target)])
    return results
