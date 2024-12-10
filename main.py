#!/usr/bin/env python3

from label_compare.label import Labelling
from label_compare.compare import LabelComparer
from pathlib import Path


def main():
    datadir = Path("./examples/")
    dat = [Labelling.from_csv_in_seconds(f) for f in datadir.glob("label-data*.csv")]
    for d in dat:
        print(d.name)
        for label in range(4):
            print(f"{d.number_frames_of(label)} frames with label {label}; ", end='\t')
        print("\n_____________________")
        # print(d.labels)


if __name__ == "__main__":
    main()
