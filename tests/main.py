import argparse

from tests.transformers import source, preprocess, window, quantize
from tests.tasks import build_data_for_cv, do_transformation_pipeline, train_clf
from gingivere.utilities import scores_for_clf


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

    transformations2 = [
        (source, {}),
        (preprocess, {}),
        (window, {}),
        (quantize, {})
    ]

    d = do_transformation_pipeline(targets[0], transformations)
    d = build_data_for_cv(d)
    clf = train_clf(d)
    scores_for_clf(d, clf)
    return d, clf


if __name__ == "__main__":
    data, clf = main()
