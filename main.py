#!/usr/bin/env python3

from label_compare import read_labels_from_dir
from label_compare.label import Labelling
from label_compare.compare import LabelComparer
from label_compare.labelcomparers import *


from pathlib import Path

PART_HEADER = "🭕🭠"+ "🭶"*40



def main():
    datadir = Path("./examples/")
    dat: list[Labelling] = read_labels_from_dir(datadir)
    for d in dat:
        d.report_stats()
        print("\n_____________________")
        # print(d.labels)
    majority: Labelling = Labelling.majority_vote(dat)
    majority.report_stats()
    majority.save_to_csv_in_seconds(datadir / "majority_vote.csv")
    # dat[0].save_to_csv_in_seconds( f"{datadir}/{dat[0].name}-reconfigured.csv") works well
    dat.append(majority)
    print(PART_HEADER)
    lc_simple_agreement.report_ascii(dat)
    print(PART_HEADER)
    lc_hyperactive_agreement.report_ascii(dat)
    print(PART_HEADER)
    lc_nothyper_agreement.report_ascii(dat)
    for lc in lc_agreements_by_label:
        print(PART_HEADER)
        lc.report_ascii(dat)


if __name__ == "__main__":
    main()
