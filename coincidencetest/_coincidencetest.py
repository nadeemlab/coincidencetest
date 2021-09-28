"""
The `coincidencetest` is an exact test for the probability of "coincidence" of
several binary features along a subsample of a given size, given the positivity
rates for each feature.

It can be used to assess biclusters found in a feature matrix.
"""

import math
from math import log10
from math import floor
from math import factorial
from math import prod
from itertools import combinations
from itertools import product

def binom(ambient_size: int=0, subset_size: int=0):
    """
    Computes a binomial coefficient. This implementation is exact, not using
    floating point arithmetic.

    Parameters
    ----------
    ambient_size : int
        The size of the set being covered.
    subset_size : int
        The size of the subsets being counted.

    Returns
    -------
    coefficient : int
        The value.
    """
    if subset_size > ambient_size:
        return 0
    if subset_size < 0:
        return 0
    return factorial(ambient_size) //   \
            factorial(subset_size) //   \
            factorial(ambient_size - subset_size)

def sign(x):
    return 1 if x % 2 == 0 else -1

def compute_number_of_covers(set_sizes: tuple=(), ambient_size: int=0,
                             strategy: str='binomial-formula'):
    """
    Computes the number of coverings of a given set by sets with prescribed sizes.

    Parameters
    ----------
    set_sizes : tuple
        The integer sizes of the sets of a covering.
    ambient_size : int
        The size of the set being covered.
    strategy : {'binomial-formula', 'brute-force'}, optional
        Selects the method of computation.
        The following options are available (default is 'binomial-formula'):
          * 'binomial-formula': A closed formula using binomial coefficients.
          * 'brute-force': Enumeration of all covers with the given set sizes.

    Returns
    -------
    number_of_covers : int
        The count.

    See Also
    --------
    `coincidencetest`

    Examples
    --------
    Consider a set of size 3, to be covered by two sets, of sizes (2, 2). Each of
    the two sets is determined by which of the 3 elements to omit, and the pair of
    sets is a covering if and only if the omitted elements are not equal. Thus there
    are 3 * 3 - 3 = 6 coverings.

    >>> from coincidencetest import compute_number_of_covers
    >>> compute_number_of_covers(set_sizes=(2,2), ambient_size=3)
    6
    """
    if strategy == 'binomial-formula':
        N = ambient_size
        n = set_sizes
        terms = [
            sign(N+m)*binom(N,m)*prod([binom(m,n[i]) for i in range(len(n))])
            for m in range(max(n), N + 1)
        ]
        return sum(terms)

    if strategy == 'brute-force':
        whole_set = set(range(ambient_size))
        all_subsets_fixed_size = [
            combinations(whole_set, size) for size in set_sizes
        ]
        subset_families = product(*all_subsets_fixed_size)
        covers = [
            family for family in subset_families if set().union(*family) == whole_set
        ]
        return len(covers)

    return None

def count_all_configurations(set_sizes: tuple=(), ambient_size: int=0):
    """
    Computes the number of all configurations of subsets of a set of a given size,
    the subsets being of prescribed sizes.

    Parameters
    ----------
    set_sizes : tuple
        The prescribed integer sizes.
    ambient_size : int
        The size of the ambient set.

    Returns
    -------
    count : int
        The count.
    """
    return prod([binom(ambient_size, size) for size in set_sizes])

def calculate_probability_of_multicoincidence(ambient_size: int=0,
                                              set_sizes: tuple=(),
                                              intersection_size: int=0):
    """
    Calculates the probability that subsets of a set of a given size, themselves of
    prescribed sizes, have mutual intersection of a given cardinality.

    Parameters
    ----------
    ambient_size : int
        The size of the ambient set.
    set_sizes : tuple
        The integer sizes of some subsets.
    intersection_size : int
        The size of the intersection of the subsets.

    Returns
    -------
    probability : float
        The probability. Calculated as the number of configurations with the given
        intersection size, divided by the number of all configurations.
    """
    reduced_sizes = [size - intersection_size for size in set_sizes]
    if any(size < 0 for size in reduced_sizes):
        return 0

    initial_choices = binom(ambient_size=ambient_size, subset_size=intersection_size)
    reduced_ambient_size = ambient_size - intersection_size
    covers_of_remaining = compute_number_of_covers(
        set_sizes = tuple(reduced_ambient_size - size for size in reduced_sizes),
        ambient_size = reduced_ambient_size,
    )
    all_configurations = count_all_configurations(
        set_sizes = set_sizes,
        ambient_size = ambient_size,
    )
    return initial_choices * covers_of_remaining / all_configurations

def union_bound_count(ambient_size: int=0,
                      set_sizes: tuple=(),
                      union_size: int=0):
    """
    Computes the number of all configurations of subsets of a set of a given size,
    the subsets being of prescribed sizes, such that the union has given size
    *or less*.

    Parameters
    ----------
    ambient_size : int
        The size of the ambient set.
    set_sizes: tuple
        The prescibed integer sizes.
    union_size: int
        The (inclusive) bound on the union size.

    Returns
    -------
    count : int
        The count.
    """
    N = ambient_size
    v = set_sizes
    n = union_size
    return sign(n) * sum([
        sign(m) * binom(N,m) * binom(N-m-1,N-n-1) * prod([
            binom(m,vj) for vj in v
        ])
        for m in range(max(v), n+1)
    ])

def configurations_bounded_intersection(ambient_size: int=0,
                                        set_sizes: list=[],
                                        intersection_size: int=0):
    """
    Computes the number of configurations of subsets of a set of a given size,
    the subsets being of prescribed sizes, such that the intersection has given
    size or *more*.

    Parameters
    ----------
    ambient_size : int
        The size of the ambient set.
    set_sizes : list
        The prescribed integer sizes.
    intersection_size : int
        The (inclusive) lower bound on the size of the mutual intersection.

    Returns
    -------
    count : int
        The number of configurations satisfying the intersection bound.
    """
    n = ambient_size
    v = set_sizes
    i = intersection_size
    l = n - min(v)
    u = n - i
    return sum([
        sign(m) * binom(n,m) * ( sign(l) * binom(n-m-1,n-l) + sign(n-i) * binom(n-m-1,i-1) ) * prod([
            binom(m,n-vj) for vj in v
        ])
        for m in range(l, u+1)
    ])

def coincidencetest(incidence_statistic, frequencies, number_samples,
                    format_p_value: bool=True,
                    correction_feature_set_size: int=None,
                    strategy: str='closed-form'):
    """
    Parameters
    ----------
    incidence_statistic : int
        The observed incidence statistic, i.e. the number of samples positive
        simultaneously for all features.
    frequencies : tuple
        The integer number of positive samples for each respective feature.
    number_samples : int
        The total number of samples.
    format_p_value : bool
        Default True. If True, reduces the number of significant figures of the
        p-value to 4, for readability.
    correction_feature_set_size : int
        Default None. If provided, performs p-value correction for multiple testing
        by multiplying by the number of subsets of the full set of features
        (which are `correction_feature_set_size` in number) which are the size of
        the length of `frequencies`.
    strategy : {'closed-form', 'sum-distribution'}, optional
        Selects the method of computation.
        The following options are available (default is 'closed-form'):
          * 'closed-form': The direct closed formula (a single summation).
          * 'closed-form-covers': The closed formula deduced using cover-counting.
          * 'sum-distribution': Sums values of the distribution (i.e. values of the
            function `calculate_probability_of_multicoincidence`), amounting to a
            double summation.

    Returns
    -------
    p_value : float
        The probability that the incidence statistic is greater than or equal to the
        given one, among all configurations with the given number of positive
        samples for each feature.
    """
    if not isinstance(incidence_statistic, int):
        raise TypeError('incidence_statistic must be int.')

    if not isinstance(number_samples, int):
        raise TypeError('number_samples must be int.')

    set_sizes = tuple(frequencies)
    ambient_size = number_samples
    if incidence_statistic > min(set_sizes):
        return 0

    if strategy == 'closed-form':
        configurations = configurations_bounded_intersection(
            ambient_size = ambient_size,
            set_sizes = frequencies,
            intersection_size = incidence_statistic,
        )
        all_configurations = count_all_configurations(
            set_sizes = set_sizes,
            ambient_size = ambient_size,
        )
        p_value = configurations / all_configurations

    if strategy == 'closed-form-covers':
        complements = [ambient_size - s for s in set_sizes]
        configurations = union_bound_count(
            ambient_size = ambient_size,
            set_sizes = complements,
            union_size = ambient_size - incidence_statistic,
        )
        all_configurations = count_all_configurations(
            set_sizes = set_sizes,
            ambient_size = ambient_size,
        )
        p_value = configurations / all_configurations

    if strategy == 'sum-distribution':
        intersection_cases = [
            (i, set_sizes, ambient_size)
            for i in range(incidence_statistic, min(set_sizes) + 1)
        ]
        probabilities = {
            intersection_size :
            calculate_probability_of_multicoincidence(
                intersection_size = intersection_size,
                set_sizes = set_sizes,
                ambient_size = ambient_size,
            )
            for intersection_size, set_sizes, ambient_size in intersection_cases
        }
        total = sum(probabilities.values())
        if correction_feature_set_size:
            total = total * binom(correction_feature_set_size, len(set_sizes))
            if total > 1.0:
                total = 1.0
        p_value = total

    if format_p_value:
        return reduce_digits_p_value(p_value)
    return p_value

def reduce_digits_p_value(p_value):
    """
    Parameters
    ----------
    p_value : float
        A p-value to format for easier reading.

    Returns
    -------
    p_value : float
        The same value, but with the number of significant figures reduced to 4.
        The string formatting for floats takes care of shortening the string
        representation using the exponent notation, when the number of digits would
        be large due to the number being very small.
    """
    precision = 4
    return round(p_value, precision-int(floor(log10(abs(p_value))))-1)
