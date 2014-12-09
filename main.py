import argparse

from gingivere.settings import load_settings
from utilities import Shelve


def main():
    settings = load_settings()

    parser = argparse.ArgumentParser()
    parser.add_argument("--target", help="the target patient")

    args = parser.parse_args()

    if args.target:
        targets = [args.target]
    else:
        targets = [
            'Dog_1',
            'Dog_2',
            'Dog_3',
            'Dog_4',
            'Dog_5',
            'Patient_1',
            'Patient_2'
        ]




    # pipelines = [
    #     FeatureConcatPipeline(
    #         Pipeline(InputSource(), Preprocess(), Windower(75), Correlation('none')),
    #         Pipeline(InputSource(), Preprocess(), Windower(75), FreqCorrelation(1, None, 'none')),
    #
    #         Pipeline(InputSource(Preprocess(), Windower(75), FFT(), Magnitude()), FreqBinning(winning_bins, 'mean'),
    #                  Log10(), FlattenChannels()),
    #         Pipeline(InputSource(Preprocess(), Windower(75), FFT(), Magnitude()),
    #                  PIBSpectralEntropy([0.25, 1, 1.75, 2.5, 3.25, 4, 5, 8.5, 12, 15.5, 19.5, 24])),
    #         Pipeline(InputSource(Preprocess(), Windower(75), FFT(), Magnitude()),
    #                  PIBSpectralEntropy([0.25, 2, 3.5, 6, 15, 24])),
    #         Pipeline(InputSource(Preprocess(), Windower(75), FFT(), Magnitude()),
    #                  PIBSpectralEntropy([0.25, 2, 3.5, 6, 15])),
    #         Pipeline(InputSource(Preprocess(), Windower(75), FFT(), Magnitude()), PIBSpectralEntropy([0.25, 2, 3.5])),
    #         Pipeline(InputSource(Preprocess(), Windower(75), FFT(), Magnitude()), PIBSpectralEntropy([6, 15, 24])),
    #         Pipeline(InputSource(Preprocess(), Windower(75), FFT(), Magnitude()), PIBSpectralEntropy([2, 3.5, 6])),
    #         Pipeline(InputSource(Preprocess(), Windower(75), FFT(), Magnitude()), PIBSpectralEntropy([3.5, 6, 15])),
    #
    #         Pipeline(InputSource(), Preprocess(), Windower(75), HFD(2)),
    #         Pipeline(InputSource(), Preprocess(), Windower(75), PFD()),
    #         Pipeline(InputSource(), Preprocess(), Windower(75), Hurst()),
    #     ),
    # ]
    #
    # classifiers = [
    #     make_svm(gamma=0.0079, C=2.7),
    #     make_svm(gamma=0.0068, C=2.0),
    #     make_svm(gamma=0.003, C=150.0),
    #     make_lr(C=0.04),
    #     make_simple_lr(),
    # ]
    #
    # submission_pipelines = [
    #     FeatureConcatPipeline(
    #         Pipeline(InputSource(), Preprocess(), Windower(75), Correlation('none')),
    #         Pipeline(InputSource(), Preprocess(), Windower(75), FreqCorrelation(1, None, 'none')),
    #         Pipeline(InputSource(Preprocess(), Windower(75), FFT(), Magnitude()), FreqBinning(winning_bins, 'mean'),
    #                  Log10(), FlattenChannels()),
    #         Pipeline(InputSource(Preprocess(), Windower(75), FFT(), Magnitude()),
    #                  PIBSpectralEntropy([0.25, 1, 1.75, 2.5, 3.25, 4, 5, 8.5, 12, 15.5, 19.5, 24])),
    #         Pipeline(InputSource(Preprocess(), Windower(75), FFT(), Magnitude()),
    #                  PIBSpectralEntropy([0.25, 2, 3.5, 6, 15, 24])),
    #         Pipeline(InputSource(Preprocess(), Windower(75), FFT(), Magnitude()),
    #                  PIBSpectralEntropy([0.25, 2, 3.5, 6, 15])),
    #         Pipeline(InputSource(Preprocess(), Windower(75), FFT(), Magnitude()), PIBSpectralEntropy([0.25, 2, 3.5])),
    #         Pipeline(InputSource(Preprocess(), Windower(75), FFT(), Magnitude()), PIBSpectralEntropy([6, 15, 24])),
    #         Pipeline(InputSource(Preprocess(), Windower(75), FFT(), Magnitude()), PIBSpectralEntropy([2, 3.5, 6])),
    #         Pipeline(InputSource(Preprocess(), Windower(75), FFT(), Magnitude()), PIBSpectralEntropy([3.5, 6, 15])),
    #         Pipeline(InputSource(), Preprocess(), Windower(75), HFD(2)),
    #         Pipeline(InputSource(), Preprocess(), Windower(75), PFD()),
    #         Pipeline(InputSource(), Preprocess(), Windower(75), Hurst()),
    #     ),
    # ]
    #
    # submission_classifiers = [
    #     make_simple_lr(),
    # ]
    #
    # if len(sys.argv) >= 2 and sys.argv[1] == 'submission':
    #     run_make_submission(settings, targets, submission_classifiers, submission_pipelines)
    # else:
    #     run_cross_validation(settings, targets, classifiers, pipelines)
    #
    # patients = ["Dog_1", "Dog_2", "Dog_3", "Dog_4", "Dog_5", "Patient_1", "Patient_2"]
    # num_cores = multiprocessing.cpu_count()
    # now = time.time()
    # if len(sys.argv) >= 2:
    #     patient = sys.argv[1]
    #     # res = Parallel(n_jobs=num_cores)(delayed(process_data)(i) for i in lrd.walk_files(patient))
    #     res = []
    #     for i in lrd.walk_files(patient):
    #         res.append(process_data(i))
    #     sapi.insert(res, "%s_mm" % patient)
    # else:
    #     for patient in patients:
    #         res = Parallel(n_jobs=num_cores)(delayed(process_data)(i) for i in lrd.walk_files(patient))
    #         sapi.insert(res, "%s_mm" % patient)
    # print("Finished in", time.time() - now, "sec")


if __name__ == "__main__":
    main()
