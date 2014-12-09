import ipdb
import pandas as pd
import numpy as np

import math

from sklearn.isotonic import IsotonicRegression
from sklearn.ensemble import AdaBoostRegressor
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import Ridge
from sklearn.metrics import classification_report
from sklearn.cross_validation import StratifiedKFold
from sklearn.metrics import roc_auc_score

from joblib import Parallel, delayed
import time
import sys
import multiprocessing
import os

import shelve_api as sapi

print(__doc__)

def load_training_data(file):
    store = pd.HDFStore(file)
    X = store['X']
    l = len(X)
    if 'interictal' in file:
        y = np.array([0.0]*l)
    else:
        y = np.array([1.0]*l)
    store.close()
    return X, y

def walk_training_data(patient):
    path = "D:/gingivere/data/"
    for file in os.listdir(path):
        if patient in file:
            if not ("test" in file):
                yield path + file

def walk_testing_data(patient):
    pass

def sort_data(data):
    X = []
    y = []
    for result in data:
        for row in result[0].values:
            X.append(row)
        y = y + list(result[1])
    return np.asarray(X), np.asarray(y)

def train_clf(X, y, verbose=True):
    clf = LinearRegression()
    XX = X[80000:]
    yy = y[80000:]
    if verbose:
        skf = StratifiedKFold(yy, n_folds=2)
        for train_index, test_index in skf:
            print("Detailed classification report:")
            print()
            print("The model is trained on the full development set.")
            print("The scores are computed on the full evaluation set.")
            print()
            X_train, X_test = XX[train_index], XX[test_index]
            y_train, y_test = yy[train_index], yy[test_index]
            clf.fit(X_train, y_train)
            y, y_pred = y, clf.predict(X)
            # for i, num in enumerate(y_pred):
            #     if num < 0.0:
            #         y_pred[i] = 0.0
            #         continue
            #     elif num > 1.0:
            #         y_pred[i] = 1.0
            #         continue
            y_pred = y_pred - y_pred.mean()
            y_pred = y_pred/y_pred.std()
            y_pred = [1/(1+math.pow(math.e, -.5*p)) for p in y_pred]
            print(classification_report(np.around(y), np.around(y_pred)))
            print()
            print(roc_auc_score(y, y_pred))
            print()
        # for train_index, test_index in skf:
        #     print("Detailed classification report:")
        #     print()
        #
        #     y_true, y_pred = y, clf.predict(X)
        #     print(roc_auc_score(y_true, y_pred))
            # y_pred = y_pred - y_pred.mean()
            # y_pred = y_pred/y_pred.std()
            # y_pred = [1/(1+math.pow(math.e, -.5*p)) for p in y_pred]
        #     print(roc_auc_score(y_true, y_pred))
        #     print()
    clf.fit(X, y)
    return clf

if __name__ == '__main__':
    patients = ["Dog_1", "Dog_2", "Dog_3", "Dog_4", "Dog_5", "Patient_1", "Patient_2"]
    # d_keys = ['data_length_sec', 'sampling_frequency', 'sequence', 'state', 'file']
    num_cores = multiprocessing.cpu_count()
    now = time.time()
    if len(sys.argv) >= 2:
        patient = sys.argv[1]
        res = Parallel(n_jobs=num_cores)(delayed(load_training_data)(file) for file in walk_training_data(patient))
        X, y = sort_data(res)
        clf = train_clf(X, y)
        sapi.insert(clf, "%s_clf" % patient)
    else:
        for patient in patients:
            res =  Parallel(n_jobs=num_cores)(delayed(load_training_data)(file) for file in walk_training_data(patient))
            X, y = sort_data(res)
            clf = train_clf(X, y)
            sapi.insert(clf, "%s_clf" % patient)
    print("Finished in", time.time()-now , "sec")
