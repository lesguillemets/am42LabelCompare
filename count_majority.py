#!/usr/bin/env python3

from label_compare import read_labels_from_dir
from label_compare.label import (Labelling)

from pathlib import Path

import statistics as st


def main():
    """
    各フレームで，同じラベルを付けた最大のところで何人が一致してるかを計算して，
    それを単に保存している
    """
    datadir = Path("./assets/converted_to_max_6frames/iter02/")
    dat: list[Labelling] = read_labels_from_dir(datadir, prefix="conv_")
    majority_counts: list[int] = Labelling.count_majority_number(dat)
    with open("./assets/majority_iter2_conv_6frames_counts.csv", 'w') as f:
        f.write('\n'.join(map(str, majority_counts)))
    print(st.mean(majority_counts))
    print(st.stdev(majority_counts))

if __name__ == "__main__":
    main()
