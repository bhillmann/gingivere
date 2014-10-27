from __future__ import print_function

import load_data
import mongo_select

import numpy as np
import pandas as pd

from sklearn import preprocessing
from sklearn.pipeline import Pipeline
from sklearn.cross_validation import StratifiedKFold
from sklearn.cross_validation import train_test_split
from sklearn.metrics import classification_report
from sklearn.svm import SVC
from sklearn.decomposition import PCA

print(__doc__)

class RawClf:
    def __init__(self, name, verbose = True):
        self.name = name
        self.verbose = True
        self.load_data()
        self.preprocess_data()
        self.train_pca()
        self.train_svm()

    def load_data(self):
        data = mongo_select.load_random_training_set('Dog_2', num=1000)
        self.X =data['data']
        self.y = data['state']

    def preprocess_data(self):
        self.X = np.array(self.X).astype(np.float)
        self.y = np.array(self.y)
        self.X = preprocessing.scale(self.X)

    def train_pca(self):
        self.PCA = PCA(copy=True, n_components=100, whiten=True)
        self.PCA.fit(self.X)

    def train_svm(self):
        self.SVM = SVC(C=100, cache_size=200, class_weight=None, coef0=0.0, degree=3, gamma=0.001, kernel='rbf', max_iter=-1, probability=True,random_state=None, shrinking=True, tol=0.001, verbose=False)
        self.SVM.fit(self.PCA.transform(self.X), self.y)
        if self.verbose:
            self.verbose_svm()

    def predict(self, x):
        return self.SVM.predict(self.PCA.transform(x))

    def predict_proba(self, x):
        return self.SVM.predict_proba(self.PCA.transform(x))

    def clear_data(self):
        self.X = []
        self.y = []

    def verbose_svm(self):
        skf = StratifiedKFold(self.y, n_folds=2)
        for train_index, test_index in skf:
            print("Detailed classification report:")
            print()
            print("The model is trained on the full development set.")
            print("The scores are computed on the full evaluation set.")
            print()
            X_train, X_test = self.X[train_index], self.X[test_index]
            y_train, y_test = self.y[train_index], self.y[test_index]
            y_true, y_pred = y_test, self.predict(X_test)
            print(classification_report(y_true, y_pred))
            print()


if __name__ == "__main__":
    clf = RawClf('test')
