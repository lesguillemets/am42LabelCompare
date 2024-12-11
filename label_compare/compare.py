from collections.abc import Iterator, Callable
from pprint import pprint
from label_compare.label import Labelling


class LabelComparer[T]:
    def __init__(
        self,
        name: str,
        cmp: Callable[[Labelling, Labelling], T],
        description: str = "",
    ) -> None:
        self.name = name
        self.cmp = cmp
        self.description = description

    def gen_comparison(self, labellings: list[Labelling]) -> list[list[T]]:
        # generates 2d list containing comparisons between Labellings
        # self.gen_comparison(ls)[i][j] == self.cmp(ls[i],ls[j])
        return [[self.cmp(li, lj) for lj in labellings] for li in labellings]

    def report(self, labellings: list[Labelling]) -> None:
        print(self.description)
        pprint(self.gen_comparison(labellings))

