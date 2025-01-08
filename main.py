#!/usr/bin/env python3

from label_compare import read_labels_from_dir
from label_compare.label import Labelling
from label_compare.compare import LabelComparer
from label_compare.labelcomparers import *


import argparse

from pathlib import Path

PART_HEADER = "🭕🭠"+ "🭶"*40

AP = argparse.ArgumentParser(description="Hey, you're great")
AP.add_argument("--dir", type=Path, help="Directory containing the data", default=Path("./examples"))
# 多分 read_labels_from_dir が prefix 違うのを想定してないので，エラーになるかも
AP.add_argument("--prefix", help="prefix for the csv files that we use", default="label-data")
subparsers = AP.add_subparsers(dest="command")

parser_stat = subparsers.add_parser("report-stats", help="Prints the stats of the labels")
parser_stat.add_argument("--with-majority", action="store_true", help="多数決結果を含めるか")



def main():
    args = AP.parse_args()
    dat: list[Labelling] = read_labels_from_dir(args.dir)
    match args.command:
        case "report-stats":
            do_stats(dat, args)
    # majority: Labelling = Labelling.majority_vote(dat)
    # majority.save_to_csv_in_seconds(args.dir / "majority_vote.csv")
    # dat[0].save_to_csv_in_seconds( f"{datadir}/{dat[0].name}-reconfigured.csv") works well

    
def do_stats(dat, args):
    if args.with_majority:
        majority: Labelling = Labelling.majority_vote(dat)
        dat.append(majority)
    for d in dat:
        d.report_stats()
        print("\n_____________________")
        # print(d.labels)
    for labelcompr in[lc_simple_agreement, lc_hyperactive_agreement, lc_nothyper_agreement] + lc_agreements_by_label:
        print(PART_HEADER)
        labelcompr.report_ascii(dat)

if __name__ == "__main__":
    main()
