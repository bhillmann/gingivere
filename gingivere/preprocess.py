from multiprocessing import Pool
import pandas as pd
import numpy as np
import random

from gingivere import SETTINGS
from gingivere.data import generate_mat_cvs
from gingivere.features import FeaturePipeline
from gingivere.pipeline import Pipeline

def preprocess_data(target, feature_pipeline, preprocess_pipeline):
    pool = Pool(SETTINGS.N_jobs)
    paths = [path for path in generate_mat_cvs(target)]
    feature_pipeline = FeaturePipeline(feature_pipeline)
    results = pool.map(feature_pipeline.run, paths)
    gar = generate_accumulate_results(results)
    return wrap_preprocess_to_data(gar, paths)

class PreprocessPipeline:
    def __init__(self, pipelines):
        self.pipelines = pipelines
        for pipeline in pipelines:
            assert isinstance(pipeline, Pipeline)

    def run(self, path):
        data = source(path)
        features = []
        for pipeline in self.pipelines:
            features.append(pipeline.run(data))
        return X, y, p

class PreprocessPipe(object):
    def __init__(self):
        pass

    @staticmethod
    def apply(origin):
        raise NotImplementedError

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


def build_df(data):
    X, y, paths = data
    df = pd.DataFrame(X)
    df['y'] = y
    df['paths'] = paths
    return df

def mask_for_mat(df, path):
    return df[df['paths'] == path]

def mask_for_state(df, state='preictal'):
    return df[[state in i for i in df['paths']]]

def mask_for_random_sample(df, n='auto'):
    if n == 'auto':
        n = int(sum(df['y']))
    # print(n)
    return df.ix[random.sample(list(df.index), n)]

def wrap_df_to_data(df):
    X = df.iloc[:, :-2].values
    y = df['y']
    y = y.as_matrix()
    paths = list(df['paths'])
    return X, y, paths

def train_strategy(data):
    df = build_df(data)
    df_1 = mask_for_random_sample(df)
    df_2 = mask_for_state(df)
    df = pd.concat([df_1, df_2])
    return wrap_df_to_data(df)