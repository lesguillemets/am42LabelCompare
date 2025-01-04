from collections.abc import Iterator, Callable
from pprint import pprint

import textwrap
from label_compare.label import Labelling

COLUMN_WIDTH = 18
COLUMN_FLOAT_FORMAT = "{:.4f}"
ROW_HEIGHT = 3

class LabelComparer[T]:
    """
    Labelling と Labelling を比較して，結果として T を返すのが仕事．
    gen_comparison では全通りの比較をして返す
    """
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

    def gen_ascii_table(self, labellings: list[Labelling]) -> str:
        header_names = [textwrap.wrap(l.name, width=COLUMN_WIDTH) for l in labellings]
        header_height: int = max(map(len, header_names))
        header = ["┏" + "┳".join(["━" * COLUMN_WIDTH] * (len(labellings) + 1)) + "┓"]
        for line in range(header_height):
            header_line = "┃".join(
                map(
                    lambda c: (c[line] if len(c) > line else "").center(COLUMN_WIDTH),
                    header_names,
                )
            )
            header.append("┃" + " " * COLUMN_WIDTH + "┃" + header_line + "┃")

        comps = self.gen_comparison(labellings)
        content = []
        for i, row in enumerate(comps):
            content.append(
                "┣" + "╋".join(["━" * COLUMN_WIDTH] * (len(labellings) + 1)) + "┫"
            )
            for l_in_row in range(ROW_HEIGHT):
                current_from = header_names[i]
                first_column = (
                    current_from[l_in_row] if len(current_from) > l_in_row else ""
                ).center(COLUMN_WIDTH)
                if l_in_row == (ROW_HEIGHT + 1) // 2:
                    columns = [
                        dat_to_cell_str(c) for c in row
                    ]
                else:
                    columns = [" " * COLUMN_WIDTH for c in row]
                content.append("┃" + "┃".join([first_column] + columns) + "┃")
        content.append(
            "┗" + "┻".join(["━" * COLUMN_WIDTH] * (len(labellings) + 1)) + "┛"
        )
        return "\n".join(header + content)

    def report_ascii(self, lbls: list[Labelling]) -> None:
        print(f"{self.name} -- {self.description}")
        print(self.gen_ascii_table(lbls))

def dat_to_cell_str(dat:object) -> str:
    """
    LabelComparer.cmp の返す T を，cell に収まるように返す．
    幅はCOLUMN_WIDTH のstr
    """
    if isinstance(dat, float):
        return COLUMN_FLOAT_FORMAT.format(dat).rjust(COLUMN_WIDTH)
    elif isinstance(dat, str):
        assert(len(dat) <= COLUMN_WIDTH)
        return dat.rjust(COLUMN_WIDTH)
    elif isinstance(dat, tuple) and (isinstance(dat[0], int) or isinstance(dat[0],float)):
        # (n, outof) の pair の場合
        ratio = dat[0]/dat[1]
        return f"{dat[0]}/{dat[1]}({ratio:.3f})"[:COLUMN_WIDTH].rjust(COLUMN_WIDTH)
    else:
        rep = f"{dat}"
        return rep[:COLUMN_WIDTH].center(COLUMN_WIDTH)
