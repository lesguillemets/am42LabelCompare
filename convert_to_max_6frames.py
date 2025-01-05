#!/usr/bin/env python3

from label_compare import read_labels_from_dir
from label_compare.label import Labelling
from label_compare.compare import LabelComparer
from label_compare.labelcomparers import *


from pathlib import Path


def main():
    datadir = Path("./examples/iter02")
    dat: list[Labelling] = read_labels_from_dir(datadir)
    for d in dat:
        """
        d を前後6フレームの最大値で代表させた Labelling に置き換え，
        to_csv_in_seconds で assets/converted_to_max_6frames/conv_{d.name}.csv に保存
        """
        converted = d.take_max_beforeafter_N_frames(6)
        with open(Path(f"assets/converted_to_max_6frames/conv_{d.name}.csv"), "w") as csvfile:
            csvfile.write("start,end,label\n")
            csvfile.write(converted.to_csv_in_seconds())     

if __name__ == "__main__":
    main()
