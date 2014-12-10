import numpy as np
from sklearn import preprocessing

from gingivere.pipeline import Pipeline
from gingivere.data import source

class FeaturePipeline:
    def __init__(self, pipelines):
        self.pipelines = pipelines
        for pipeline in pipelines:
            assert isinstance(pipeline, Pipeline)

    def run(self, path):
        data = source(path)
        features = []
        for pipeline in self.pipelines:
            features.append(pipeline.run(data))
        return features

class FeaturePipe(object):
    def __init__(self):
        pass

    @staticmethod
    def apply(origin):
        raise NotImplementedError

class Scale(FeaturePipe):
    @staticmethod
    def apply(origin):
        return preprocessing.scale(origin.astype('float32'))

class Window(FeaturePipe):
    @staticmethod
    def apply(origin):
        destination = []
        for row in origin:
            #TODO Change the size to be dynamic
            for i in np.array_split(row, 10):
                destination.append(i)
        return destination

class Quantize(FeaturePipe):
    @staticmethod
    def apply(origin):
        destination = []
        for row in origin:
            hist, bin_edges = np.histogram(row, density=True)
            destination.append(hist)
        return np.asarray(destination, dtype='float32')