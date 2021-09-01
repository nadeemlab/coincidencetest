import math
from math import factorial
from itertools import combinations
from itertools import product
from itertools import chain

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
    return factorial(ambient_size) //   \
            factorial(subset_size) //   \
            factorial(ambient_size - subset_size)

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
    strategy : {'binomial-formula', 'brute-force', 'recursion'}, optional
        Selects the method of computation
        The following options are available (default is 'binomial-formula'):
          * 'binomial-formula': A closed formula using binomial coefficients.
          * 'brute-force': Enumeration of all covers with the given set sizes.
          * 'recursion': Recurrence formula deduced by removing one element from the
            ambient set, with base cases provided by classical partition counting
            formulas and surjective function counting formulas.

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
        sign = lambda x: 1 if x % 2 == 0 else -1
        terms = [
            sign(N+m)*binom(N,m)*math.prod([binom(m,n[i]) for i in range(len(n))])
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

    if strategy == 'recursion':
        number_subsets = len(set_sizes)
        if all([size == 1 for size in set_sizes]):
            if number_subsets == ambient_size:
                return factorial(ambient_size)
            if number_subsets < ambient_size:
                return 0
            if number_subsets > ambient_size:
                return number_of_surjective_functions(
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
            compute_number_of_covers(
                set_sizes = reduce_set_sizes(set_sizes=set_sizes, which=selected),
                ambient_size = ambient_size - 1,
                strategy = 'recursion',
            )
            for selected in powerset(number_subsets) if selected != ()
        ]
        return sum(counts_by_strata)

def multinomial(subset_sizes):
    """
    Computes a multinomial coefficient.

    Parameters
    ----------
    subset_sizes : tuple
        The integer parts of a partition of an integer.

    Returns
    -------
    coefficient: int
        The value.
    """
    if len(subset_sizes) == 1:
        return 1
    binomial_factor = binom(sum(subset_sizes), subset_sizes[-1])
    multinomial_factor = multinomial(subset_sizes[:-1])
    return binomial_factor * multinomial_factor

def stirling_second_kind(ambient_size: int=0, number_parts: int=0,
                         normalized: bool=False):
    """
    Computes an (unnormalized or ordinary) Stirling number of the second kind.
    If unnormalized, the division by the factorial of the ambient size is not
    performed.

    Parameters
    ----------
    ambient_size : int
        The ambient size whose partitions are to be counted.
    number_parts : int
        The number of parts for partitions to consider.
    normalized : bool
        Default False. If True, the ordinary Stirling number of the second kind is
        computed, i.e. the division by the factorial of the ambient size is
        performed.

    Returns
    -------
    stirling: int
        The value.
    """
    sign = lambda x: 1 if x % 2 == 0 else -1
    terms = [
        sign(i) * binom(number_parts, i) * pow(number_parts - i, ambient_size)
        for i in range(number_parts + 1)
    ]
    if normalized:
        return sum(terms) // factorial(number_parts)
    else:
        return sum(terms)

def number_of_surjective_functions(source_size: int=0, target_size: int=0):
    """
    Computes the number of surjective functions between two sets of given sizes.

    Parameters
    ----------
    source_size : int
        The size of the domain of the functions to be counted.
    target_size: int
        The size of the codomain of the functionsn to be counted.

    Returns
    -------
    count: int
        The value.
    """
    return stirling_second_kind(
        ambient_size = source_size,
        number_parts = target_size,
    )

def powerset(set_size):
    """
    Creates a list of all subsets of the set of integers {0, 1, ... `set_size - 1`}.

    Parameters
    ----------
    set_size : int
        The size of the base set.

    Returns
    -------
    subsets : list
        All subsets.
    """
    base_set = list(range(set_size))
    return list(chain.from_iterable(
        combinations(base_set, r) for r in range(len(base_set) + 1)
    ))

def reduce_set_sizes(set_sizes: tuple=(), which: list=[]):
    """
    Convience function to decrement specific members of a tuple of integers.

    Parameters
    ----------
    set_sizes : tuple
        The integers.
    which : list
        A list of the indices of the integers to be decremented.

    Returns
    -------
    reduced : tuple
        List of integers, with some decremented by 1. 0 values are omitted.
    """
    new_sizes = [
        set_sizes[i] - (1 if i in which else 0) for i in range(len(set_sizes))
    ]
    return tuple(s for s in new_sizes if s > 0)

