#!/usr/bin/env python3

from label_compare.label import Labelling
from label_compare.compare import LabelComparer, lc_simple_agreement
from pathlib import Path


def main():
    datadir = Path("./examples/")
    dat = [Labelling.from_csv_in_seconds(f) for f in datadir.glob("label-data*.csv")]
    for d in dat:
        d.report_stats()
        print("\n_____________________")
        # print(d.labels)
    lc_simple_agreement.report(dat)


if __name__ == "__main__":
    main()
