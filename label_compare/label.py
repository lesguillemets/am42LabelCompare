# label = (start, end (in seconds), label)
type SingleLabelSecond = tuple[float, float, int]


class Labelling(object):
    def __init__(self, ls: list[SingleLabelSecond]):
        self.labels = ls
    def say_hi(self):
        print("HI")
