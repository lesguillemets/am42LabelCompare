from collections.abc import Iterator, Callable
from pprint import pprint

import textwrap
from label_compare.label import Labelling

COLUMN_WIDTH = 12
ROW_HEIGHT = 3


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

    def gen_report_ascii(self, labellings:list[Labelling]) -> str:
        print(f"{self.name} -- {self.description}")
        header_names = [textwrap.wrap(l.name, width=COLUMN_WIDTH) for l in labellings]
        header_height:int = max(map(len, header_names))
        header = [ "┏" + '┳'.join(["━"*COLUMN_WIDTH]*(len(labellings)+1)) + "┓" ]
        for line in range(header_height):
            header_line = "┃".join(
                    map(lambda c: (c[line] if len(c) > line else "").center(COLUMN_WIDTH), header_names)
                    )
            header.append("┃" + ' '*COLUMN_WIDTH + "┃" + header_line + "┃")
        header.append("┣" + '╋'.join(["━"*COLUMN_WIDTH]*(len(labellings)+1)) + "┫")

        comps = self.gen_comparison(labellings)
        content = []

        return('\n'.join(header))

    def report_ascii(self, lbls: list[Labelling]) -> None:
        print(self.gen_report_ascii(lbls))



