#!/usr/bin/env python3

from label_compare.label import Labelling
from label_compare.compare import LabelComparer
from label_compare.labelcomparers import *

import re

from pathlib import Path

PATTERN_FNAME_NAME = re.compile(r"label-data_*(.*)\.csv")


def fname_to_name(s: str) -> str:
    if (m := PATTERN_FNAME_NAME.match(s)) is not None:
        return m.group(1)
    else:
        return s


def main():
    datadir = Path("./examples/")
    dat = [
        Labelling.from_csv_in_seconds(f, name=fname_to_name(f.name))
        for f in datadir.glob("label-data*.csv")
    ]
    for d in dat:
        d.report_stats()
        print("\n_____________________")
        # print(d.labels)
    lc_simple_agreement.report_ascii(dat)
    lc_hyperactive_agreement.report_ascii(dat)
    lc_nothyper_agreement.report_ascii(dat)
    for lc in lc_agreements_by_label:
        lc.report_ascii(dat)


if __name__ == "__main__":
    main()
