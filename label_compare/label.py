from __future__ import annotations
from collections.abc import Iterator, Callable

import csv
import math
import statistics
import itertools as it
from pathlib import Path

# label = (start, end (in frames), label)
# the video is currently 29.97 fps

VIDEO_FPS: float = 29.97
type Label = int
type Frame = int
type SingleLabel = tuple[Frame, Frame, Label]


def to_bucket(labels: list[SingleLabel]) -> list[Label]:
    bucket = []
    for st, en, label in labels:
        bucket.extend([label] * (en - st))
    return bucket


class Labelling:
    def __init__(self, name: str, ls: list[SingleLabel]) -> None:
        self.name = name
        self.labels = ls
        self.__bucket = to_bucket(ls)

    def say_hi(self):
        print("HI")

    def number_frames_of(self, l: Label | list[Label]) -> int:
        n = 0
        if not isinstance(l, list):
            l = [l]
        for st, en, lb in self.labels:
            if lb in l:
                n += en - st
        return n

    def at(self, n: Frame) -> Label:
        return self.__bucket[n]

    def slice(self, fm: Frame, to: Frame) -> list[Label]:
        # slice で label を返す
        # to―th frame は含まれないのに留意 ([0,1,2,3,4][slice(2,4)] == [2,3])
        return self.__bucket[slice(fm, to)]

    def length(self) -> Frame:
        return self.labels[-1][1] - 1

    def report_stats(self) -> None:
        print(self.name)
        print(f"|\t {self.length()} frames total")
        print("|-\t Number of frames for each labels:")
        for lkind in it.chain(range(4), [[0, 1], [2, 3]]):
            nf = self.number_frames_of(lkind)
            print(
                f"|\t{nf} ({nf*100/self.length():.2f}%) frames with label {lkind}; ",
                end="\t",
            )
        print()
        length_spans = list(map(lambda l: l[1] - l[0], self.labels))
        print("|-\tlength of each span:\n|--\t\t", end="")
        print(
            f"mean: {statistics.mean(length_spans):.2f}",
            f"median: {statistics.median(length_spans)}",
            f"variance: {statistics.variance(length_spans):.3f}",
            f"stdev: {statistics.stdev(length_spans):.3f}",
            sep="\t",
        )

    def agreement_with(
        self, other: Labelling, for_label: list[Label] | None = None
    ) -> tuple[int, int]:
        the_part = list(
            filter(
                lambda z: for_label is None or z[0] in for_label,
                zip(self.__bucket, other.__bucket),
            )
        )
        outof = len(the_part)
        agreement = len(list(filter(lambda z: z[0] == z[1], the_part)))
        return (agreement, outof)

    @staticmethod
    def from_csv_in_seconds(fl: Path, name: str = "") -> Labelling:
        # 秒*29.97 が必ずしも整数に近づかないので，
        # 多分 js でとれる video.duration は
        # フレームごとに離散の値ではないんだと思う
        # …ので，ここは 29.97 かけて floor でフレームにすることに
        # (0,3,2), (3,10,0), (10,230,1) …みたいになるので，
        # 一旦 SingleLabel(start,end,label) は [start, end)
        # の区間を表してるものとみなすことにしよう．
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
