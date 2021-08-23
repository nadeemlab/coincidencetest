from itertools import combinations
from itertools import product

def brute_force_count_covers(
    set_sizes: tuple=(),
    ambient_size: int=0,
):
    whole_set = set(range(ambient_size))
    tuples_of_subsets_fixed_size = [
        combinations(whole_set, size) for size in set_sizes
    ]
    subset_families = product(*tuples_of_subsets_fixed_size)
    covers = [
        family for family in subset_families if set().union(*family) == whole_set
    ]
    return len(covers)

print(brute_force_count_covers(set_sizes = (2, 2), ambient_size = 3))
# Output: 6
# Reasoning: There are (3 choose 2) * (3 choose 2) = 9 possible "a priori" configurations, and exactly 3 of them are not covers.

print(brute_force_count_covers(set_sizes = (3, 2), ambient_size = 4))
# Output: 12

print(brute_force_count_covers(set_sizes = (1, 1, 1), ambient_size = 3))
# Output: 6
# Reasoning: A cover by such sets is just a labelling. Ambient permutations achieve all possibilities from a given initial labelling.

print(brute_force_count_covers(set_sizes = (1, 1, 1, 1), ambient_size = 4))
# Output: 24
# Reasoning: Same as immediately preceding example.
