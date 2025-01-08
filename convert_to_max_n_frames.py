#!/usr/bin/env python3

from label_compare import read_labels_from_dir
from label_compare.label import Labelling
from label_compare.compare import LabelComparer
from label_compare.labelcomparers import *


from pathlib import Path


def save_max_N_frames(
        dat: list[Labelling],
        neighbour_N: int = 6,
        output_base_dir: Path = Path("output"),
        output_prefix: str = "conv"
        ):
    for d in dat:
        """
        d を前後nフレームの最大値で代表させた Labelling に置き換え，
        to_csv_in_seconds で assets/converted_to_max_6frames/conv_{d.name}.csv に保存
        """
        converted = d.take_max_beforeafter_N_frames(neighbour_N)
        savedir = Path(f"converted_to_max_{neighbour_N}frames")
        filename = Path(f"{output_prefix}_{neighbour_N}_{d.name}.csv" )
        with open(output_base_dir / savedir / filename , "w") as csvfile:
            csvfile.write("start,end,label\n")
            csvfile.write(converted.to_csv_in_seconds())

if __name__ == "__main__":
    datadir: Path = Path("./examples"),
    dat: list[Labelling] = read_labels_from_dir(datadir)
    save_max_N_frames(dat)
