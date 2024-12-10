from collections.abc import Iterator, Callable

from label_compare.label import Labelling


class LabelComparer:
    def __init__(self, cmp:Callable[[Labelling,Labelling], float]) -> None:
        self.cmp = cmp

    def gen_comparison(self, labellings: list[Labelling]) -> list[list[float]]:
        return [self.cmp(li,lj) for li in labellings for lj in labellings]

    def report(self,labellings: list[Labelling]) -> None:
        print(self.gen_comparison(labellings))
