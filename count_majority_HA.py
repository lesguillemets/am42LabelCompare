"""
フレームが hyperactive かどうかの評定について何人が一致するか，を計算して assetsに表示
"""

from label_compare import read_labels_from_dir
from label_compare.label import (Labelling)

from pathlib import Path

import statistics as st

def main():
    datadir = Path("./examples/backup/iter01")
    dat: list[Labelling] = read_labels_from_dir(datadir)
    majority_counts: list[int] = Labelling.count_agreement_HAorNOHA(dat)
    with open("./assets/majority_counts_HAorNOHA.csv", 'w') as f:
        f.write('\n'.join(map(str, majority_counts)))
    print(st.mean(majority_counts))
    print(st.stdev(majority_counts))

if __name__ == "__main__":
    main()
