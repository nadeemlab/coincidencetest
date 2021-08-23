#!/usr/bin/env python3

# from math import comb
# from math import prod

# import plotly.express as px

# def calculate_number_of_configurations(
#     intersection_size: int=0,
#     set_sizes: list=[],
#     ambient_size: int=0,
# ):
#     reduced_sizes = [size - intersection_size for size in set_sizes]
#     if any([size < 0 for size in reduced_sizes]):
#         raise ValueError('Intersection size not possible.')

#     residual_ambient_sizes = []
#     remaining = ambient_size - intersection_size
#     for i in range(len(reduced_set_sizes)):
#         residual_choice_sizes[i] = remaining
#         remaining -= reduced_set_sizes[i]
        

#      [comb(ambient_size, size) for size in reduced_sizes]
#     initial_choice_size = comb(ambient_size, intersection_size)
#     return prod(residual_choice_sizes + [initial_choice_size])

# def number_of_all_configurations(
#     set_sizes: list=[],
#     ambient_size: int=0,
# ):
#     choice
#     return prod([])


# fig = px.scatter(
#     x=[0, 1, 2, 3, 4],
#     y=[0, 1, 4, 9, 16],
# )
# fig.show()

from functools import lru_cache
from itertools import chain
from itertools import combinations
from math import factorial

from scipy.special import binom
from lfu_cache import LFUCache


class LFUCacheCoverCounts:
    def __init__(self, maxsize=0):
        self.cache = LFUCache(maxsize)

    def tuplize(self, kwargs):
        return tuple(kwargs[key] for key in sorted(list(kwargs.keys())))

    def decorator(self, function):
        def inner_function(**kwargs):
            key = self.tuplize(kwargs)
            try:
                value = self.cache.get(key)
            except KeyError:
                value = function(**kwargs)
                self.cache.put(key, value)
            return value
        return inner_function


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

@lru_cache(maxsize=10000)
def multinomial(params):
    if len(params) == 1:
        return 1
    binomial_factor = binom(sum(params), params[-1])
    multinomial_factor = multinomial(params[:-1])
    product = binomial_factor * multinomial_factor
    return product

@lru_cache(maxsize=10000)
def stirling_second_kind(
    ambient_size: int=0,
    number_parts: int=0,
):
    sign = lambda x: 1 if x % 2 == 0 else -1
    terms = [
        sign(i) * binom(number_parts, i) * pow(number_parts - i, ambient_size)
        for i in range(number_parts + 1)
    ]
    return sum(terms) / factorial(number_parts)

@lru_cache(maxsize=10000)
def number_surjective_functions(
    source_size: int=0,
    target_size: int=0,
):
    return factorial(target_size) * stirling_second_kind(
        ambient_size = source_size,
        number_parts = target_size,
    )

custom_lfu_covers = LFUCacheCoverCounts(100000)
lfu_cache_custom_covers = custom_lfu_covers.decorator

# @lfu_cache_custom_covers
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


if __name__=='__main__':
    print('')
    print('Sterling:')
    print(stirling_second_kind(ambient_size=3, number_parts=3))
    print(stirling_second_kind(ambient_size=4, number_parts=4))
    print(stirling_second_kind(ambient_size=4, number_parts=2))
    print(stirling_second_kind(ambient_size=5, number_parts=3))
    print(stirling_second_kind(ambient_size=10, number_parts=7))
    print(stirling_second_kind(ambient_size=10, number_parts=7) == 5880)

    print('')
    print(number_of_covers(set_sizes=(3,1), ambient_size=4))
    print('')
    print(number_of_covers(set_sizes=(3,3,4), ambient_size=7))
    print('')
    print(number_of_covers(set_sizes=(18, 15, 16, 8, 18), ambient_size=21))
    print(number_of_covers(set_sizes=(18, 15, 16, 8, 18), ambient_size=21) / factorial(21))
    print(number_of_covers(set_sizes=(18, 15, 16, 8, 18), ambient_size=21, denominator = factorial(21)))
    print('')
    l = (18, 15, 16, 8, 18)
    l = tuple([e + 100 for e in l])   # Hm... experiencing int overflow. All amounts can actually be discounted by ambient factorial?
    ambient = sum(l)
    print('Ambient: ' + str(ambient))
    print(number_of_covers(
        set_sizes=l,
        ambient_size=ambient,
    ))
    # print('')
    # print(number_of_covers(set_sizes=(18, 15, 16, 8, 14), ambient_size=21))


