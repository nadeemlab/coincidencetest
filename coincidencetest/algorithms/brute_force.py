from itertools import combinations
from itertools import product

def number_of_covers(
    set_sizes: tuple=(),
    ambient_size: int=0,
):
    whole_set = set(range(ambient_size))
    all_subsets_fixed_size = [
        combinations(whole_set, size) for size in set_sizes
    ]
    subset_families = product(*all_subsets_fixed_size)
    covers = [
        family for family in subset_families if set().union(*family) == whole_set
    ]
    return len(covers)
