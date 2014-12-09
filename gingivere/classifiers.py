import numpy as np
import sklearn
import sklearn.pipeline
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler


class SimpleLogisticRegression(LinearRegression):
    def predict_proba(self, X):
        predictions = self.predict(X)
        predictions = sklearn.preprocessing.scale(predictions)
        predictions = 1.0 / (1.0 + np.exp(-0.5 * predictions))
        return np.vstack((1.0 - predictions, predictions)).T


def make_simple_lr():
    return sklearn.pipeline.make_pipeline(StandardScaler(), SimpleLogisticRegression()), 'ss-slr'
