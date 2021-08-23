import math

from .algorithms.recursion_method import number_of_covers
from .algorithms.recursion_method import binom as _binom

def count_all_configurations(
    set_sizes: tuple=(),
    ambient_size: int=0,
):
    return math.prod([_binom(ambient_size, size) for size in set_sizes])

def calculate_probability_of_multicoincidence(
    intersection_size: int=0,
    set_sizes: tuple=(),
    ambient_size: int=0,
):
    reduced_sizes = [size - intersection_size for size in set_sizes]
    if any([size < 0 for size in reduced_sizes]):
        raise ValueError('Intersection size %s is not possible.', intersection_size)

    initial_choices = _binom(ambient_size=ambient_size, subset_size=intersection_size)
    reduced_ambient_size = ambient_size - intersection_size
    covers_of_remaining = number_of_covers(
        set_sizes = tuple(reduced_ambient_size - size for size in reduced_sizes),
        ambient_size = reduced_ambient_size,
    )
    all_configurations = count_all_configurations(
        set_sizes = set_sizes,
        ambient_size = ambient_size,
    )
    return initial_choices * covers_of_remaining / all_configurations
