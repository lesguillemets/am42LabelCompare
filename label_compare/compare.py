from collections.abc import Iterator, Callable

from label_compare.label import Labelling


class LabelComparer:
    def __init__(
        self,
        name: str,
        cmp: Callable[[Labelling, Labelling], float],
        description: str = "",
    ) -> None:
        self.cmp = cmp

    def gen_comparison(self, labellings: list[Labelling]) -> list[list[float]]:
        # self.gen_comparison(ls)[i][j] == self.cmp(ls[i],ls[j])
        return [[self.cmp(li, lj) for lj in labellings] for li in labellings]

    def report(self, labellings: list[Labelling]) -> None:
        print(self.gen_comparison(labellings))
