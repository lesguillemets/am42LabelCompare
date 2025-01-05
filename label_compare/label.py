from __future__ import annotations
from collections.abc import Iterator, Callable

import csv
import math
import statistics
import itertools as it
from pathlib import Path

from label_compare.helper import majority

# label = (start, end (in frames), label)
# the video is currently 29.97 fps

VIDEO_FPS: float = 29.97
DEBUG = False
type Label = int
type Frame = int
# ここからここまでこのラベルだよ，というやつ
type SingleLabel = tuple[Frame, Frame, Label]


# SingleLabel を，各フレームでどのラベルが貼られたかのリストに変換
def to_bucket(labels: list[SingleLabel]) -> list[Label]:
    bucket = []
    for st, en, label in labels:
        bucket.extend([label] * (en - st))
    return bucket

# フレームごとのラベルのリストを SingleLabel のリストに戻す
def from_bucket(bucket:list[Label]) -> list[SingleLabel]:
    current: Label = bucket[0]
    current_start: Frame = 0
    streak = 0
    result = []
    for (i,label) in enumerate(bucket):
        if current == label:
            streak += 1
        else:
            result.append(((current_start, current_start+streak,current)))
            current = label
            current_start = i
            streak = 1
    result.append(((current_start, current_start+streak,current)))
    return result



class Labelling:
    """
    評定つけた人，SingleLabel のリストとしての評定データ，それの bucket 化したもの
    """ 
    def __init__(self, name: str, ls: list[SingleLabel]) -> None:
        self.name = name
        self.labels = ls
        self.__bucket = to_bucket(ls)
        print(from_bucket(self.__bucket))
        # ここの assertion はもちろんフレームの切れ目の違いでエラーになる
        try:
            assert(self.labels == from_bucket(self.__bucket))
        except AssertionError:
            print(f">>>>> warn: mismatch in {name}")

    def number_frames_of(self, l: Label | list[Label]) -> int:
        """
        l (単一のラベルまたはそのリスト)の評定されたフレーム数
        """
        n = 0
        if not isinstance(l, list):
            l = [l]
        for st, en, lb in self.labels:
            if lb in l:
                n += en - st
        return n

    def at(self, n: Frame) -> Label:
        """
        nフレーム目のラベルを返すヘルパ関数
        """
        return self.__bucket[n]

    def slice(self, fm: Frame, to: Frame) -> list[Label]:
        # slice で label を返す
        # to―th frame は含まれないのに留意 ([0,1,2,3,4][slice(2,4)] == [2,3])
        return self.__bucket[slice(fm, to)]

    def length(self) -> Frame:
        return self.labels[-1][1] - 1

    def report_stats(self) -> None:
        """
        一般的な統計情報
        """
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
        """
        Other との単なる合致率を， list[Label] で与えたラベルについて計算
        """
        if DEBUG:
            print(f"comparing {self.name} vs {other.name}, {for_label}")
        the_part = list(
            filter(
                lambda z: (for_label is None) or (z[0] in for_label),
                zip(self.__bucket, other.__bucket),
            )
        )
        outof = len(the_part)
        if for_label is None:
            agreement = len(list(filter(lambda z: (z[0] == z[1]), the_part)))
        else:
            agreement = len(list(filter(lambda z: (z[1] in for_label), the_part)))
        return (agreement, outof)

    @staticmethod
    def majority_vote(labellings: list[Labelling]) -> Labelling:
        """
        みんなの多数決で決めた評定
        """
        majority_bucket = list(
                map(majority,
                    zip(*(lb.__bucket for lb in labellings))
                    )
                )
        return Labelling("majority_vote", from_bucket(majority_bucket))


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

    def to_csv_in_seconds(self) -> str:
        """
        reverse of from_csv_in_seconds
        """
        return "\n".join(
            f"{start/VIDEO_FPS},{end/VIDEO_FPS},{lb}" for (start, end, lb) in self.labels
        )

    def save_to_csv_in_seconds(self, fl: Path) -> None:
        with open(fl, "w") as csvfile:
            csvfile.write("start,end,label\n")
            csvfile.write(self.to_csv_in_seconds())

    @staticmethod
    def count_majority_number(labellings: list[Labelling]) -> list[int]:
        """
        フレームごとに，何人の評定が合致してるか
        """
        frames = zip(*(lb.__bucket for lb in labellings))
        result = []
        for f in frames:
            counter: dict[Label, int] = {}
            for d in f:
                if d in counter:
                    counter[d] += 1
                else:
                    counter[d] = 1
            result.append(max(counter.values()))
        return result

    @staticmethod
    def count_agreement_HAorNOHA(labellings: list[Labelling]) -> list[int]:
        """
        フレームごとに，hyperactive かどうかの評定が何人で一致するか
        """
        frames = zip(*(lb.__bucket for lb in labellings))
        result = []
        for f in frames:
            counter: dict[bool, int] = {True:0, False:0}
            for d in f:
                is_hyper = d in [2,3]
                counter[is_hyper] += 1
            result.append(max(counter.values()))
        return result

    def take_max_beforeafter_N_frames(self, n:int) -> Labelling:
        """
        そのフレームの前後nフレームずつをとって，その中の最大のラベルを採用する
        """
        new_bucket:list[Label] = []
        for i in range(len(self.__bucket)):
            new_bucket.append(max(self.__bucket[max(0, i-n):i+n+1]))
        return Labelling(self.name, from_bucket(new_bucket))