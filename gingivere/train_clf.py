import pandas as pd
import numpy as np
import multiprocessing
from sklearn.linear_model import LinearRegression
from sklearn.cross_validation import StratifiedKFold
from sklearn.metrics import classification_report
from sklearn.metrics import roc_auc_score

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
    return X, y

def walk_training_data(patient):
    path = "D:/gingivere/data/"
    for file in os.listdir(path):
        if patient in file and not "test" in file:
            yield path + file

def walk_testing_data(patient):
    pass

def sort_data(data):
    X = []
    y = y
    for result in data:
        X = X + result[0]
        y = y + result[1]
    return np.asarray(X), np.asarray(y)

def train_clf(X, y, verbose=True):
    clf = LinearRegression()
    if verbose:
        skf = StratifiedKFold(y, n_folds=2)
        for train_index, test_index in skf:
            print("Detailed classification report:")
            print()
            X_train, X_test = X[train_index], X[test_index]
            y_train, y_test = y[train_index], y[test_index]
            clf.fit(X_train, y_train)
            y_true, y_pred = y_test, clf.predict(X_test)
            print(classification_report(np.around(y_true), np.around(y_pred)))
            print()
            print(roc_auc_score(y_true, y_pred))
            print()
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
        res = sort_data(data)
        clf = train_clf(*res)
        sapi.insert(clf, "%s_clf" % patient)
    else:
        for patient in patients:
            res =  Parallel(n_jobs=num_cores)(delayed(load_training_data)(file) for file in walk_training_data(patient))
            res = sort_data(data)
            clf = train_clf(*res)
            sapi.insert(clf, "%s_clf" % patient)
    print("Finished in", time.time()-now , "sec")
