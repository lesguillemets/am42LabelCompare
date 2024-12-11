from label_compare.label import Labelling
from label_compare.compare import LabelComparer

lc_simple_agreement : LabelComparer[float] = LabelComparer(
    "simple agreement",
    lambda l0, l1: (lambda x: x[0] / x[1])(l0.agreement_with(l1)),
    description="simple agreement between frames",
)

lc_hyperactive_agreement : LabelComparer[float] = LabelComparer(
    "hyperactive agreement",
    lambda l0, l1: (lambda x: x[0] / x[1])(l0.agreement_with(l1, for_label=[2,3])),
    description="agreements on which frame is hyperactive",
)

lc_nothyper_agreement : LabelComparer[float] = LabelComparer(
    "nothyper agreement",
    lambda l0, l1: (lambda x: x[0] / x[1])(l0.agreement_with(l1, for_label=[1,2])),
    description="agreements on which frame is not hyperactive",
)
