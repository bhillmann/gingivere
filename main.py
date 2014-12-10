import argparse

from gingivere.workers import do_transformation_pipeline
from gingivere.transformers import source, preprocess, window, quantize
from gingivere.tasks import build_data_for_cv, train_classifier


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

    transformations = [
        (source, {}),
        (preprocess, {}),
        (window, {}),
        (quantize, {})
    ]

    d = do_transformation_pipeline(targets[0], transformations)
    d = build_data_for_cv(d)
    train_classifier(d)
    return d


if __name__ == "__main__":
    data = main()
