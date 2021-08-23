from functools import lru_cache
from itertools import chain
from itertools import combinations
from math import factorial

@lru_cache(maxsize=10000)
def binom(
    ambient_size: int=0,
    subset_size: int=0,
):
    return factorial(ambient_size) //   \
            factorial(subset_size) //   \
            factorial(ambient_size - subset_size)

@lru_cache(maxsize=10000)
def multinomial(subset_sizes):
    if len(subset_sizes) == 1:
        return 1
    binomial_factor = binom(sum(subset_sizes), subset_sizes[-1])
    multinomial_factor = multinomial(subset_sizes[:-1])
    return binomial_factor * multinomial_factor

@lru_cache(maxsize=10000)
def stirling_second_kind(
    ambient_size: int=0,
    number_parts: int=0,
    unnormalized: bool=False,
):
    sign = lambda x: 1 if x % 2 == 0 else -1
    terms = [
        sign(i) * binom(number_parts, i) * pow(number_parts - i, ambient_size)
        for i in range(number_parts + 1)
    ]
    if unnormalized:
        return sum(terms)
    else:
        return sum(terms) // factorial(number_parts)

@lru_cache(maxsize=10000)
def number_surjective_functions(
    source_size: int=0,
    target_size: int=0,
):
    return stirling_second_kind(
        ambient_size = source_size,
        number_parts = target_size,
        unnormalized = True,
    )

@lru_cache(maxsize=None)
def powerset(set_size):
    base_set = list(range(set_size))
    return list(chain.from_iterable(
        combinations(base_set, r) for r in range(len(base_set) + 1)
    ))

def reduce_set_sizes(
    set_sizes: tuple=(),
    which: list=[],
):
    new_sizes = [set_sizes[i] - (1 if i in which else 0) for i in range(len(set_sizes))]
    return tuple(s for s in new_sizes if s > 0)

@lru_cache(maxsize=100000)
def number_of_covers(
    set_sizes: tuple=(),
    ambient_size: int=0,
):
    number_subsets = len(set_sizes)
    if all([size == 1 for size in set_sizes]):
        if number_subsets == ambient_size:
            return factorial(ambient_size)
        if number_subsets < ambient_size:
            return 0
        if number_subsets > ambient_size:
            return number_surjective_functions(
                source_size = sum(set_sizes),
                target_size = ambient_size,
            )
    if sum(set_sizes) == ambient_size:
        return multinomial(set_sizes)

    if sum(set_sizes) < ambient_size:
        return 0

    if ambient_size == 0:
        return 0

    if any([size > ambient_size for size in set_sizes]):
        return 0

    if len(set_sizes) == 1:
        size = set_sizes[0]
        if size == ambient_size:
            return 1
        elif size < ambient_size:
            return 0

    if len(set_sizes) == 0:
        return 0

    counts_by_strata = [
        number_of_covers(
            set_sizes = reduce_set_sizes(set_sizes=set_sizes, which=selected),
            ambient_size = ambient_size - 1,
        )
        for selected in powerset(number_subsets) if selected != ()
    ]
    return sum(counts_by_strata)
