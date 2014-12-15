import argparse

from gingivere.features import Scale, Window, Quantize, MeanStd, FFT, PIBIntegrateLog
from gingivere.pipeline import Pipeline
from gingivere.tasks import make_target_cv_scores_pipeline


def main():
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

    feature_plumbing = [Pipeline((Scale(), Window(), Quantize())), Pipeline((Window(), MeanStd()))]
    # feature_plumbing = [Pipeline((Scale(), Window(), Quantize())), Pipeline((Window(), MeanStd())), Pipeline((Window(), FFT(), PIBIntegrateLog(range(100))))]

    make_target_cv_scores_pipeline('Dog_1', feature_plumbing)


if __name__ == "__main__":
    main()
