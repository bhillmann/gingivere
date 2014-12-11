from classifiers import make_simple_lr
from sklearn.cross_validation import StratifiedKFold

def process_data(pre_processed, submission=False, clf=False):
    #TODO customize classifier
    if clf:
        pass
    else:
        make_clf = make_simple_lr

    X, y, paths = pre_processed
    #TODO Prepare for submission
    if submission:
        pass
    else:
        clf, name = make_clf()
        clfs = []
        cv = StratifiedKFold(y, n_folds=5)
        for train_index, test_index in cv:
            X_train, X_test = X[train_index], X[test_index]
            y_train, y_test = y[train_index], y[test_index]
            clf.fit(X_train, y_train)
            clfs.append((train_index, test_index, clf))
    return X, y, paths, clfs

