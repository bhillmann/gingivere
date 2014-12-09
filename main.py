import argparse

from workers import do_transformation_pipeline
from transformers import source, preprocess, window, quantize


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

    do_transformation_pipeline(targets[0], transformations)


if __name__ == "__main__":
    main()
