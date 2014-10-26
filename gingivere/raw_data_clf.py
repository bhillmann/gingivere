from __future__ import print_function

import load_data

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

    def load_data(self):
        data = load_data.load_shelve('test')
        self.X =data['data']
        self.y = data['state']

    def preprocess_data(self):
        self.X = np.array(self.X).astype('float_')
        self.y = np.array(self.y).astype('int_')
        self.X = preprocessing.scale(self.X)

    def train_pca():
        self.PCA = PCA(copy=True, n_components=100, whiten=True)
        self.PCA.fit(self.X)

    def train_svm():
        self.SVM = SVC(C=100, cache_size=200, class_weight=None, coef0=0.0, degree=3, gamma=0.001, kernel='rbf', max_iter=-1, probability=True,random_state=None, shrinking=True, tol=0.001, verbose=False)
        self.SVM.fit(PCA./transform(self.X))
        if self.verbose:
