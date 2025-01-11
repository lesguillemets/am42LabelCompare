#!/usr/bin/env python3

from label_compare import read_labels_from_dir
from label_compare.label import Labelling
from label_compare.compare import LabelComparer
from label_compare.labelcomparers import *

import convert_to_max_n_frames as conv

import argparse

from pathlib import Path

PART_HEADER = "🭕🭠"+ "🭶"*40

AP = argparse.ArgumentParser(description="Hey, you're great")
AP.add_argument("--dir", type=Path, help="Directory containing the data", default=Path("./examples"))
# 多分 read_labels_from_dir が prefix 違うのを想定してないので，エラーになるかも
AP.add_argument("--prefix", help="prefix for the csv files that we use", default="label-data")
subparsers = AP.add_subparsers(dest="command", required=True)

parser_stat = subparsers.add_parser("report-stats", help="Prints the stats of the labels")
parser_stat.add_argument("--with-majority", action="store_true", help="多数決結果を含めるか")

parser_create_max_n = subparsers.add_parser(
    "gen-max-n-frames", help="前後nフレームの最大値で見たファイルを作成")
parser_create_max_n.add_argument("-n", type=int, help="number of neighbouring frames to consider", default=6)
parser_create_max_n.add_argument("--output-dir", type=Path, help="ここの下にディレクトリを切る", default=Path("output"))
parser_create_max_n.add_argument("--output-prefix", type=str, help="{op}_{n}_{d.name}.csv に保存", default="conv")



def main():
    args = AP.parse_args()
    dat: list[Labelling] = read_labels_from_dir(args.dir, prefix=args.prefix)
    match args.command:
        case "report-stats":
            do_stats(dat, args)
        case "gen-max-n-frames":
            do_create_max_n(dat, args)
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

def do_create_max_n(dat,args):
    conv.save_max_N_frames(
        dat,
        neighbour_N=args.n,
        output_base_dir=args.output_dir,
        output_prefix=args.output_prefix)



if __name__ == "__main__":
    main()
