from __future__ import print_function

from sklearn.pipeline import Pipeline

from sklearn.cross_validation import StratifiedKFold

from sklearn.cross_validation import train_test_split
from sklearn.grid_search import GridSearchCV
from sklearn.metrics import classification_report
from sklearn.svm import SVC
from sklearn.decomposition import RandomizedPCA
from sklearn.neighbors import KNeighborsClassifier



import load_data

print(__doc__)

# Loading the Digits dataset

data = load_data.load_shelve('test')

X = data['data']
y = data['state']

estimators = [('pca', RandomizedPCA(whiten=True)), ('svm', KNeighborsClassifier())]

# Set the parameters by cross-validation
tuned_parameters = {'svm__kernel': ['rbf'], 'svm__gamma': [1e-3],
                     'svm__C': [1, 10, 100, 1000], 'pca__n_components': [100]}
tuned_clf = Pipeline(estimators)

scores = ['roc_auc']

for score in scores:
    print("# Tuning hyper-parameters for %s" % score)
    print()

    # clf = GridSearchCV(KNeighborsClassifier(), {}, cv=StratifiedKFold(y, n_folds=3), scoring=score)
    clf = GridSearchCV(tuned_clf, {}, cv=StratifiedKFold(y, n_folds=3), scoring=score)
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

# Note the problem is too easy: the hyperparameter plateau is too flat and the
# output model is the same for precision and recall with ties in quality.
