from multiprocessing.pool import Pool

import numpy as np

from gingivere import SETTINGS
from gingivere.data import generate_mat_cvs
from gingivere.classifiers import make_simple_lr
from gingivere.utilities import TransformationPipeline
from tests.trainer import train_strategy


def build_data_for_cv(data):
    X, paths = data
    X = np.array(X)
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
    y = np.array(y, dtype='float32')
    return X, y, p

def train_clf(data):
    X, y, paths = train_strategy(data)
    clf, name = make_simple_lr()
    clf.fit(X, y)
    return clf


def do_transformation_pipeline(target, transformations):
    pipeline = TransformationPipeline(transformations)
    pool = Pool(SETTINGS.N_jobs)
    paths = [path for path in generate_mat_cvs(target)]
    results = pool.map(pipeline.run, paths)
    return results, paths