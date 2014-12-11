import numpy as np
from sklearn.metrics import classification_report
from sklearn.metrics import roc_auc_score

def postprocess_data(processed, submission=False):
    X, y, paths, clfs = processed
    scores_for_clf(X, y, paths, clfs)

def generate_mask_for_mats(paths):
    for unique_path in set(paths):
        yield [unique_path == path for path in paths]


def scores_for_clf(X, y, paths, clfs):
    for train_index, test_index, clf in clfs:
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