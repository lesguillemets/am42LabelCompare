from __future__ import annotations

import csv
import math
from pathlib import Path
# label = (start, end (in frames), label)
# the video is currently 29.97 fps

VIDEO_FPS: float = 29.97
type SingleLabel = tuple[int, int, int]


class Labelling:
    def __init__(self, name: str, ls: list[SingleLabel]) -> None:
        self.name = name
        self.labels = ls

    def say_hi(self):
        print("HI")

    @staticmethod
    def from_csv_in_seconds(fl: Path, name: str = "") -> Labelling:
        # 秒*29.97 が必ずしも整数に近づかないので，
        # 多分 js でとれる video.duration は
        # フレームごとに離散の値ではないんだと思う
        # …ので，ここは 29.97 かけて floor でフレームにすることに
        with open(fl, newline="") as csvfile:
            if name == "":
                name = fl.name
            reader = csv.reader(csvfile, delimiter=",")
            assert next(reader) == ["start", "end", "label"]
            dat = [
                (
                    math.floor(float(s) * VIDEO_FPS),
                    math.floor(float(e) * VIDEO_FPS),
                    int(l),
                )
                for (s, e, l) in reader
            ]
            return Labelling(name, dat)
