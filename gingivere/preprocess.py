from multiprocessing import Pool
import numpy as np
import random

from gingivere import SETTINGS
from gingivere.data import generate_mat_cvs
from gingivere.features import FeaturePipeline

def preprocess_data(target, feature_pipeline, submission=False):
    pool = Pool(SETTINGS.N_jobs)
    paths = [path for path in generate_mat_cvs(target)]
    if submission:
        paths = mask_for_state(paths, state='test')
    else:
        paths = mask_for_random_sample(paths)
    feature_pipeline = FeaturePipeline(feature_pipeline)
    results = pool.map(feature_pipeline.run, paths)
    gar = generate_accumulate_results(results)
    return wrap_preprocess_to_data(gar, paths)

def generate_accumulate_results(results):
    for result in results:
        result = np.hstack(result)
        yield result

def wrap_preprocess_to_data(gar, paths):
    X = np.array([r for r in gar])
    num_feature_vecs = X.shape[1]
    len_feature_vec = X.shape[-1]
    X = X.reshape(-1, len_feature_vec)
    y = []
    p = []
    for path in paths:
        if 'interictal' in path:
            y = y + [0] * num_feature_vecs
            p = p + [path] * num_feature_vecs
        elif 'preictal' in path:
            y = y + [1] * num_feature_vecs
            p = p + [path] * num_feature_vecs
        else:
            print('Test in')
            y = y + [-1] * num_feature_vecs
            p = p + [path] * num_feature_vecs
    y = np.array(y, dtype='float64')
    return X, y, p

def mask_for_state(paths, state='preictal'):
    return [i for i in paths if state in i]

def mask_for_random_sample(paths, n=False):
    preictals = mask_for_state(paths)
    interictals = mask_for_state(paths, state='interictal')
    if n:
        n = len(interictals)
    preictals = random.sample(preictals, n)
    return preictals + interictals