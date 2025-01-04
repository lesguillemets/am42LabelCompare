### 具体的な LabelComparer の定義

from label_compare.label import Labelling
from label_compare.compare import LabelComparer

lc_simple_agreement: LabelComparer[float] = LabelComparer(
    "simple agreement",
    lambda l0, l1: (lambda x: x[0] / x[1])(l0.agreement_with(l1)),
    description="simple agreement between frames",
)

lc_agreements_by_label: list[LabelComparer[tuple[float,float]]] = [
    LabelComparer(
        f"agreement for label {i}",
        lambda l0, l1, i=i: l0.agreement_with(l1, for_label=[i])
        ,
        description=f"simple agreement for label {i} between frames",
    )
    for i in range(4)
]

lc_hyperactive_agreement: LabelComparer[tuple[float,float]] = LabelComparer(
    "hyperactive agreement",
    lambda l0, l1: l0.agreement_with(l1, for_label=[2, 3]),
    # lambda l0, l1: (lambda x: x[0] / x[1])(l0.agreement_with(l1, for_label=[2, 3])),
    description="agreements on which frame is hyperactive",
)

lc_nothyper_agreement: LabelComparer[tuple[float,float]] = LabelComparer(
    "nothyper agreement",
    lambda l0, l1: l0.agreement_with(l1, for_label=[1, 2]),
    description="agreements on which frame is not hyperactive",
)
