from sklearn.pipeline import Pipeline
from sklearn.svm import SVC
from sklearn.decomposition import PCA
from sklearn.grid_search import GridSearchCV

def make_clf():
    estimators = [('reduce_dim', PCA()), ('svm', SVC())]
    return Pipeline(estimators)


def make_gs():
    params = dict(reduce_dim__n_components=[2, 5, 10], svm__C=[0.1, 10, 100])
    return GridSearchCV(clf, param_grid=params)


def main():
    pass


if __name__ == "__main__":
    main()
