
def gen_tex_table[T](dat: list[list[T]]) -> str:
    return ""

def majority[T](dat:list[T]) -> T:
    """
    majority vote.
    majority([1,1,1, 2, 190, 190]) == 1
    majority([1,1,1, 2,2,2 190, 190]) == 2
    """
    counter: dict[T, int] = {}
    for d in dat:
        if d in counter:
            counter[d] += 1
        else:
            counter[d] = 1
    return max(counter, key=lambda x: (counter.get(x), x))


