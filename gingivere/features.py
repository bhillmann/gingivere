import numpy as np
from sklearn import preprocessing
from scipy.fftpack import rfft, fftfreq
from math import floor
from scipy.integrate import simps

from gingivere.utilities.time import Timer
from gingivere.pipeline import Pipeline
from gingivere.data import source

class FeaturePlumbing:
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
    def apply(self, origin):
        raise NotImplementedError

class Scale(FeaturePipe):
    def apply(self, origin):
        return preprocessing.scale(origin.astype('float64'))

class Window(FeaturePipe):
    def apply(self, origin):
        N = 10 * 16
        M = floor(origin.shape[1] / 10)
        destination = np.empty((N, M))
        i = 0
        for row in origin:
            for new_row in np.array_split(row, 10):
                destination[i] = new_row[:M]
                i += 1
        return destination

class Quantize(FeaturePipe):
    def apply(self, origin):
        f = lambda x: np.histogram(x, density=True)[1]
        return np.apply_along_axis(f, 1, origin)

class MeanStd(FeaturePipe):
    def apply(self, origin):
        f = lambda x: np.array([x.mean(), x.std()])
        return np.apply_along_axis(f, 1, origin)


class FFT(FeaturePipe):
    """
    Apply Fast Fourier Transform to the last axis.
    """
    def apply(self, origin):
        # t = Timer()
        destination = rfft(origin)
        # print("Completed FFT in %s" % t.pretty_str())
        return destination

class PIB(FeaturePipe):
    """
    Apply Fast Fourier Transform to the last axis.
    """

    def __init__(self, freq_bins, sampling_freq=400, origin=None):
        self.freq_bins = freq_bins
        self.time_step = 1 / sampling_freq
        if origin:
            self.ready_data_for_apply(origin)
        else:
            self.N, self.M, self.freqs, self.idx = None, None, None, None

    def freq_binning(self, row):
        destination = []
        for i in range(len(self.freq_bins) - 1):
            begin = self.freq_bins[i]
            end = self.freq_bins[i + 1]
            slice_begin = np.argmax(self.freqs >= begin)
            slice_end = np.argmax(self.freqs >= end) - 1
            destination.append((slice_begin, slice_end))
        return destination

    def ready_data_for_apply(self, origin):
        self.set_shape(origin)
        self.set_freqs_idx(origin)
        return self.set_power_spectrum(origin)

    def set_shape(self, origin):
        self.N, self.M = origin.shape

    def set_freqs_idx(self, origin):
        self.N, self.M = origin.shape
        freqs = fftfreq(self.M, self.time_step)
        self.freqs = freqs[:np.floor(self.M / 2)]
        self.idx = np.argsort(freqs)

    def set_power_spectrum(self, origin):
        f = lambda row: row[:np.floor(self.M / 2)] ** 2
        return np.apply_along_axis(f, 1, origin)

    def iterate_power_band_bins(self, row):
        freq_bins = self.freq_binning(row)
        for slice_begin, slice_end in freq_bins:
            yield row[slice_begin:slice_end], self.freqs[slice_begin:slice_end]


class PIBIntegrateLog(PIB):
    def __init__(self, freq_bins, sampling_freq=400):
        super().__init__(freq_bins, sampling_freq=sampling_freq)

    def apply(self, origin):
        t = Timer()
        origin = self.ready_data_for_apply(origin)
        destination = []
        for row in origin:
            dest_row = []
            for bin_arr, freq_arr in self.iterate_power_band_bins(row):
                power = simps(bin_arr, freq_arr)
                dest_row.append(np.log(power))
            destination.append(dest_row)
        print("Completed PIBIntegrateLog in %s" % t.pretty_str())
        return np.asarray(destination, dtype='float64')