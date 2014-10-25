from __future__ import print_function

import numpy as np

from sklearn import preprocessing

from sklearn.pipeline import Pipeline
from sklearn.cross_validation import StratifiedKFold
from sklearn.cross_validation import train_test_split
from sklearn.grid_search import GridSearchCV
from sklearn.metrics import classification_report
from sklearn.svm import SVC
from sklearn.decomposition import KernelPCA
import load_data

print(__doc__)

# Loading the Digits dataset

data = load_data.load_shelve('test')

X = preprocessing.scale(np.array(data['data']))
y = np.array(data['state'])

estimators = [('pca', KernelPCA()), ('svm', SVC(probability=True))]

# Set the parameters by cross-validation
tuned_parameters = {'svm__kernel': ['rbf',], 'svm__gamma': [1e-3],
                     'svm__C': [100], 'pca__n_components': [100,], 'pca__kernel':['rbf','linear']}
tuned_clf = Pipeline(estimators)

scores = ['roc_auc']

for score in scores:
    print("# Tuning hyper-parameters for %s" % score)
    print()

    clf = GridSearchCV(tuned_clf, tuned_parameters, cv=StratifiedKFold(y, n_folds=3), scoring=score)
    clf.fit(X, y)

    print("Best parameters set found on development set:")
    print()
    print(clf.best_estimator_)
    print()
    print("Grid scores on development set:")
    print()
    for params, mean_score, scores in clf.grid_scores_:
        print("%0.3f (+/-%0.03f) for %r"
              % (mean_score, scores.std() / 2, params))
    print()


    skf = StratifiedKFold(y, n_folds=2)
    for train_index, test_index in skf:
        print("Detailed classification report:")
        print()
        print("The model is trained on the full development set.")
        print("The scores are computed on the full evaluation set.")
        print()
        X_train, X_test = X[train_index], X[test_index]
        y_train, y_test = y[train_index], y[test_index]
        y_true, y_pred = y_test, clf.predict(X_test)
        print(classification_report(y_true, y_pred))
        print()

# Note the problem is too easy: the hyperparameter plateau is too flat and the
# output model is the same for precision and recall with ties in quality.

# Pipeline(steps=[('pca', RandomizedPCA(copy=True, iterated_power=3, n_components=100,
#        random_state=None, whiten=True)), ('svm', SVC(C=100, cache_size=200, class_weight=None, coef0=0.0, degree=3,
#   gamma=0.001, kernel='rbf', max_iter=-1, probability=True,
#   random_state=None, shrinking=True, tol=0.001, verbose=False))])
