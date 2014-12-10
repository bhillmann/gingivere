import argparse

from gingivere.features import Scale, Window, Quantize, MeanStd
from gingivere.pipeline import Pipeline
from gingivere.preprocess import preprocess_data


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

    feature_pipeline = [Pipeline((Scale, Window, Quantize)), Pipeline((Window, MeanStd))]

    preprocess_data('Dog_1', feature_pipeline)


if __name__ == "__main__":
    main()
