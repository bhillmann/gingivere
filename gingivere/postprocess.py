import numpy as np
from sklearn.metrics import classification_report
from sklearn.ensemble import RandomForestClassifier
from sklearn.cross_validation import StratifiedKFold

def postprocess_data(target, X, y, paths, trainers, submission=False):
    XX, yy = [], []
    for pred, target in accumulate_scores(X, y, trainers, paths):
        XX += list(pred)
        yy += list(target)
    scores_for_clf_2(np.array(XX), np.array(yy))
    for pred, target in accumulate_scores(X, y, trainers, paths):
        scores_for_clf_3(pred, target)

def generate_mask_for_mats(paths):
    print(len(set(paths)))
    for unique_path in set(paths):
        yield np.array([unique_path == path for path in paths], dtype='bool')


def accumulate_scores(X, y, trainers, paths):
    for train_index, test_index, clf in trainers:
        target = []
        pred = []
        for mask in generate_mask_for_mats(paths):
            pred.append(clf.predict_proba(X[mask])[:, 1])
            target.append(y[mask][0])
        yield np.array(pred), np.array(target)




def scores_for_clf(X, y, trainers):
    for train_index, test_index, clf in trainers:
        print("Detailed classification report:")
        print()
        print("The model is trained on a folded development set.")
        print("The scores are computed on the full set.")
        print()
        X_train, X_test = X[train_index], X[test_index]
        y_train, y_test = y[train_index], y[test_index]
        y_true, y_pred = y_test, clf.predict_proba(X_test)
        print(classification_report(np.around(y_true), np.around(y_pred[:, 1])))
        print()
        print(roc_auc_score(y_true, y_pred[:, 1]))
        print()

def scores_for_clf_2(X, y):
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

def scores_for_clf_3(X, y):
    y_pred = np.array([np.mean(x) for x in X])
    print("Detailed classification report:")
    print()
    print(classification_report(np.around(y), np.around(y_pred)))
    print()
    print(roc_auc_score(y, y_pred))
    print()