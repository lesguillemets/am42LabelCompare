from pathlib import Path
from label_compare.label import Labelling

import re

PATTERN_FNAME_NAME: re.Pattern[str] = re.compile(r"label-data_*(.*)\.csv")


def read_labels_from_dir(datadir: Path, prefix: str = "label-data") -> list[Labelling]:
    pattern: re.Pattern[str] = re.compile(f"{prefix}_*(.*)\.csv")
    return [
        Labelling.from_csv_in_seconds(f, name=fname_to_name(f.name, pattern))
        for f in sorted(datadir.glob(f"{prefix}*.csv"))
    ]


def fname_to_name(s: str, pat: re.Pattern[str] = PATTERN_FNAME_NAME) -> str:
    if (m := pat.match(s)) is not None:
        return m.group(1)
    else:
        return s
