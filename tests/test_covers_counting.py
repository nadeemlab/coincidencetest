from itertools import combinations
from itertools import product

import coincidencetest
from coincidencetest.algorithm import number_of_covers

def brute_force_count_covers(
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

def test_manually_validated_cases():
    cases = {
        ((2, 2), 3) : 6,
    }
    for (set_sizes, ambient_size), expected_count in cases.items():
        assert(number_of_covers(
            set_sizes = set_sizes,
            ambient_size = ambient_size,
        ) == expected_count)

def test_consistent_with_prior():
    cases = {
        ((3, 1), 4) : 4,
        ((3, 2), 4) : 12,
        ((3, 3, 4), 7) : 10815,
    }
    for (set_sizes, ambient_size), expected_count in cases.items():
        assert(number_of_covers(
            set_sizes = set_sizes,
            ambient_size = ambient_size,
        ) == expected_count)

def test_agreement_with_brute_force():
    cases = [
        ((2, 2), 3),
        ((3, 1), 4),
        ((3, 2), 4),
        ((3, 3, 4), 7),
        ((3, 3, 5, 2), 8),
    ]
    for set_sizes, ambient_size in cases:
        library_calculated = number_of_covers(
            set_sizes = set_sizes,
            ambient_size = ambient_size,
        )
        brute_force = brute_force_count_covers(
            set_sizes = set_sizes,
            ambient_size = ambient_size,
        )
        assert(library_calculated == brute_force)

def large_non_crashing_example():
    l = (18, 15, 16, 8, 18)
    l = tuple([e + 100 for e in l])
    ambient = sum(l)
    print('Ambient size: ' + str(ambient))
    print('Exact value, based on formula for number of partitions: ' + str(number_of_covers(
        set_sizes=l,
        ambient_size=ambient,
    )))

if __name__=='__main__':
    large_non_crashing_example()
