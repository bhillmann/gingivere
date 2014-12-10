from multiprocessing.pool import Pool
import numpy as np
from sklearn.metrics import classification_report
from sklearn.metrics import roc_auc_score
from sklearn.cross_validation import StratifiedKFold

from gingivere import SETTINGS
from gingivere.data import generate_mat_cvs
from gingivere.classifiers import make_simple_lr
from gingivere.utilities import TransformationPipeline


def build_data_for_cv(data):
    X, paths = data
    X = np.array(X)
    num_feature_vecs = X.shape[1]
    len_feature_vec = X.shape[-1]
    X = X.reshape(-1, len_feature_vec)
    y = []
    for path in paths:
        if 'interictal' in path:
            y = y + [0] * num_feature_vecs
        elif 'preictal' in path:
            y = y + [1] * num_feature_vecs
    y = np.array(y, dtype='float32')
    return X, y, paths

def train_classifier(data):
    X, y, paths = data
    clf, name = make_simple_lr()
    skf = StratifiedKFold(y, n_folds=2)
    for train_index, test_index in skf:
        print("Detailed classification report:")
        print()
        print("The model is trained on the full development set.")
        print("The scores are computed on the full evaluation set.")
        print()
        X_train, X_test = X[train_index], X[test_index]
        y_train, y_test = y[train_index], y[test_index]
        clf.fit(X_train, y_train)
        y_true, y_pred = y_test, clf.predict(X_test)
        for i, num in enumerate(y_pred):
            if num < 0.0:
                y_pred[i] = 0.0
                continue
            elif num > 1.0:
                y_pred[i] = 1.0
                continue
        print(classification_report(np.around(y_true), np.around(y_pred)))
        print()
        print(roc_auc_score(y_true, y_pred))
        print()
    return clf


def do_transformation_pipeline(target, transformations):
    pipeline = TransformationPipeline(transformations)
    pool = Pool(SETTINGS.N_jobs)
    paths = [path for path in generate_mat_cvs(target)]
    results = pool.map(pipeline.run, paths)
    return results, paths