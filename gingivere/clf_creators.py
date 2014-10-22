from sklearn.pipeline import Pipeline
from sklearn.svm import SVC
from sklearn.decomposition import PCA
from sklearn.grid_search import GridSearchCV

def make_clf():
    estimators = [('reduce_dim', PCA()), ('svm', SVC())]
    return Pipeline(estimators)


def make_gs():
    params = dict(reduce_dim__n_components=[2, 5, 10], svm__C=[0.1, 10, 100])
    return GridSearchCV(clf, param_grid=params, scoring='f1-score0', cv=5)

def print_best_parameters(gs_clf):
    best_parameters, score, _ = max(gs_clf.grid_scores_, key=lambda x: x[1])
    for param_name in sorted(parameters.keys()):
        print("%s: %r" % (param_name, best_parameters[param_name]))


def main():
    pass


if __name__ == "__main__":
    main()
