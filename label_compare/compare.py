from collections.abc import Iterator, Callable
from pprint import pprint
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
        # generates 2d list containing comparisons between Labellings
        # self.gen_comparison(ls)[i][j] == self.cmp(ls[i],ls[j])
        return [[self.cmp(li, lj) for lj in labellings] for li in labellings]

    def report(self, labellings: list[Labelling]) -> None:
        pprint(self.gen_comparison(labellings))


lc_simple_agreement = LabelComparer(
    "simple agreement",
    lambda l0, l1: (lambda x: x[0] / x[1])(l0.agreement_with(l1)),
    description="simple agreement between frames",
)
