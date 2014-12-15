import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.cross_validation import StratifiedKFold

from gingivere.utilities.shelve import load_shelve
from sklearn.metrics import roc_auc_score
from sklearn.metrics import classification_report

def postprocess_data(target, X, y, paths, train=False, submission=False):
    loaded = load_shelve('%s_clf' % target)
    score, clf, train = loaded
    XX, yy = accumulate_scores(X, y, clf, paths)
    scores_for_post(XX, yy)


def generate_mask_for_mats(paths):
    for unique_path in set(paths):
        yield np.array([unique_path == path for path in paths], dtype='bool')

def accumulate_scores(X, y, clf, paths):
    target = []
    pred = []
    for mask in generate_mask_for_mats(paths):
        pred.append(clf.predict_proba(X[mask])[:, 1])
        target.append(y[mask][0])
    return np.array(pred), np.array(target)

def scores_for_post(X, y):
    clf = RandomForestClassifier(n_estimators=10, max_depth=None, min_samples_split=1, random_state=0)
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
        y_true, y_pred = y_test, clf.predict_proba(X_test)
        print(classification_report(np.around(y_true), np.around(y_pred[:, 1])))
        print()
        print(roc_auc_score(y_true, y_pred[:, 1]))
        print()

# def scores_for_clf_3(X, y):
#     y_pred = np.array([np.mean(x) for x in X])
#     print("Detailed classification report:")
#     print()
#     print(classification_report(np.around(y), np.around(y_pred)))
#     print()
#     print(roc_auc_score(y, y_pred))
#     print()