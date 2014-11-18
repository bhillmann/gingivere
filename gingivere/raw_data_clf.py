from __future__ import print_function

# import load_data
import shelve_api
# import mongo_select

import numpy as np
import pandas as pd

from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.cross_validation import StratifiedKFold
from sklearn.cross_validation import train_test_split
from sklearn.metrics import classification_report
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.decomposition import PCA
from sklearn.metrics import roc_auc_score

print(__doc__)

class RawClf:
    def __init__(self, name, verbose = True, data=None):
        self.name = name
        self.verbose = True
        if data:
            self.X = data[0]
            self.y = data[1]
            # self.scaler = StandardScaler()
            # self.X = self.scaler.fit_transform(self.X)
        else:
            # self.load_data()
            self.preprocess_data()
        self.verbose_svm()

        # self.train_pca()
        # self.train_svm()

    # def load_data(self):
    #     data = mongo_select.load_random_training_set(self.name, num=360)
    #     self.X =data['data']
    #     self.y = data['state']

    def preprocess_data(self):
        self.X = np.array(self.X).astype('float32')
        self.y = np.array(self.y)
        self.scaler = StandardScaler()
        self.X = scaler.fit_transform(self.X)
        # print(self.X[0])

    def get_pca(self):
        return PCA(copy=True, n_components=100, whiten=True)

    def train_pca(self):
        self.PCA = PCA(copy=True, n_components=100, whiten=False)
        self.PCA.fit(self.X)

    def get_svm(self):

        # return SVC(C=100, cache_size=200, class_weight=None, coef0=0.0, degree=3, gamma=0.001, kernel='rbf', max_iter=-1, random_state=None, shrinking=True, tol=0.001, verbose=False)
        return KNeighborsClassifier()

    def train_svm(self):
        self.SVM = SVC(C=100, cache_size=200, class_weight=None, coef0=0.0, degree=3, gamma=0.001, kernel='rbf', max_iter=-1, random_state=None, shrinking=True, tol=0.001, verbose=False)
        X = self.PCA.transform(self.X)
        # X = self.scaler.fit_transform(X)
        self.SVM.fit(X, self.y)
        if self.verbose:
            self.verbose_svm()

    def predict(self, x):
        return self.SVM.predict(self.PCA.transform(x))

    # def predict_proba(self, x):
    #     return self.SVM.predict_proba(self.PCA.transform(x))

    def clear_data(self):
        self.X = []
        self.y = []

    def verbose_svm(self):
        skf = StratifiedKFold(self.y, n_folds=2)
        print(self.name)
        for train_index, test_index in skf:
            print("Detailed classification report:")
            print()
            print("The model is trained on the full development set.")
            print("The scores are computed on the full evaluation set.")
            print()
            X_train, X_test = self.X[train_index], self.X[test_index]
            PCA = self.get_pca()
            PCA.fit(self.X)
            y_train, y_test = self.y[train_index], self.y[test_index]
            SVC = self.get_svm()
            X_train = PCA.transform(X_train)
            SVC.fit(X_train, y_train)
            X_test = PCA.transform(X_test)
            y_true, y_pred = y_test, SVC.predict(X_test)
            print(classification_report(y_true, y_pred))
            print()
            print(roc_auc_score(y_true, y_pred))
            print()




if __name__ == "__main__":
    clf = RawClf('Dog_1', data=(shelve_api.load('clf_x'), shelve_api.load('clf_y')))
