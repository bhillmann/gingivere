from classifiers import make_simple_lr
import numpy as np
from sklearn.cross_validation import StratifiedKFold
from sklearn.metrics import roc_auc_score
from sklearn.metrics import classification_report

from gingivere.utilities.shelve import insert_shelve, load_shelve

def process_data(target, X, y, paths, submission=False, clf=False):
    #TODO customize classifier
    if clf:
        pass
    else:
        make_clf = make_simple_lr
    #TODO Prepare for submission
    if submission:
        pass
    else:
        score, clf, train = save_best_classifier(target, X, y, make_clf)
    return X, y, paths, clf, train

def save_best_classifier(target, X, y, make_clf, verbose=False):
    try:
        best = load_shelve('%s_clf' % target)
    except:
        best = (float('-inf'), False, (False, False))
    new = False
    cv = StratifiedKFold(y, n_folds=5)
    for train_index, test_index in cv:
        clf, name = make_clf()
        X_train, X_test = X[train_index], X[test_index]
        y_train, y_test = y[train_index], y[test_index]
        clf.fit(X_train, y_train)
        y_true, y_pred = y_test, clf.predict_proba(X_test)
        curr_score = roc_auc_score(y_true, y_pred[:, 1])
        if verbose:
            print("Detailed classification report:")
            print()
            print("The model is trained on a folded development set.")
            print("The scores are computed on the full set.")
            print()
            print(classification_report(np.around(y_true), np.around(y_pred[:, 1])))
            print()
            print(curr_score)
            print()
        if curr_score > best[0]:
            new = True
            best = curr_score, clf, (train_index, test_index)
    if new:
        print("Saving the best classifier in %s as %s_clf with a score of %.2f" % (name, target, best[0]))
        insert_shelve(best, '%s_clf' % target)
    else:
        print("Loaded the best classifier in %s as %s_clf with a score of %.2f" % (name, target, best[0]))
    return best
