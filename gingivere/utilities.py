import numpy as np
from sklearn.metrics import classification_report
from sklearn.metrics import roc_auc_score
from sklearn.cross_validation import StratifiedKFold

class TransformationPipeline:
    def __init__(self, transformations):
        self.transformations = transformations

    def run(self, origin):
        destination = origin
        for transform, kargs in self.transformations:
            destination = transform(destination, **kargs)
        return destination

def scores_for_clf(data, clf):
    X, y, paths = data
    skf = StratifiedKFold(y, n_folds=2)
    for train_index, test_index in skf:
        print("Detailed classification report:")
        print()
        print("The model is trained on the full development set.")
        print("The scores are computed on the full evaluation set.")
        print()
        X_train, X_test = X[train_index], X[test_index]
        y_train, y_test = y[train_index], y[test_index]
        # clf.fit(X_train, y_train)
        y_true, y_pred = y_test, clf.predict(X_test)
        for i, num in enumerate(y_pred):
            if num < 0.0:
                y_pred[i] = 0.0
                continue
            elif num > 1.0:
                y_pred[i] = 1.0
                continue
        print(classification_report(np.around(y_true), np.around(y_pred)))
        print()
        print(roc_auc_score(y_true, y_pred))
        print()
    return clf

# (funct,kargs={})