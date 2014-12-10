import numpy as np

def build_data_for_cv(data):
    X, paths = data
    X = np.array(X)
    num_feature_vecs = X.shape[-2]
    len_feature_vec = X.shape[-1]
    X = X.reshape(-1, len_feature_vec)
    y = []
    for path in paths:
        if 'interictal' in path:
            y = y + [0] * num_feature_vecs
        elif 'preictal' in path:
            y = y + [1] * num_feature_vecs
    y = np.array(y, dtype='float32')
    return X, y

def build_target_vector():
    pass

def load_data_for_cv(data):
    features, paths = data
    X = build_feature_vectors(features)
    y = build_target_vector(features, path)
    return X, y