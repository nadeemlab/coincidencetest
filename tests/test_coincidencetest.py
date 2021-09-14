import time
from math import factorial
from itertools import chain
from itertools import combinations

import coincidencetest
from coincidencetest._coincidencetest import compute_number_of_covers
from coincidencetest._coincidencetest import binom
from coincidencetest._coincidencetest import calculate_probability_of_multicoincidence
from coincidencetest import coincidencetest


def _compute_number_of_covers(set_sizes: tuple=(), ambient_size: int=0,
                             strategy: str='binomial-formula'):
    """
    For testing purposes, adds support for the "recursion" strategy. This uses
    a recurrence formula deduced by removing one element from the ambient set, with
    base cases provided by classical partition counting formulas and surjective
    function counting formulas.
    """
    if strategy in ['binomial-formula', 'brute-force']:
        return compute_number_of_covers(set_sizes=set_sizes,
                                        ambient_size=ambient_size,
                                        strategy=strategy)
    if strategy == 'recursion':
        number_subsets = len(set_sizes)
        if all(size == 1 for size in set_sizes):
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
        if any(size > ambient_size for size in set_sizes):
            return 0
        if len(set_sizes) == 1:
            size = set_sizes[0]
            if size == ambient_size:
                return 1
            if size < ambient_size:
                return 0
            raise ValueError('ambient_size %s too small?' % ambient_size)
        if len(set_sizes) == 0:
            return 0

        counts_by_strata = [
            _compute_number_of_covers(
                set_sizes = reduce_set_sizes(set_sizes=set_sizes, which=selected),
                ambient_size = ambient_size - 1,
                strategy = 'recursion',
            )
            for selected in powerset(number_subsets) if selected != ()
        ]
        return sum(counts_by_strata)
    return None

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
    Default is unnormalized, meaning that the division by the factorial of the
    ambient size is not performed.

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

def reduce_set_sizes(set_sizes: tuple=(), which: list=None):
    """
    Convenience function to decrement specific members of a tuple of integers.

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


class TestCoverCounting:
    sample_cases = [
        ((2, 2), 3),
        ((3, 1), 4),
        ((3, 2), 4),
        ((3, 3, 4), 7),
        ((3, 3, 5, 2), 8),
    ]

    extreme_sample_cases = [
        [20, [101, 85, 75, 110, 99], 500],
        [50, [101, 85, 75, 110, 99], 500],
        [65, [101, 85, 75, 110, 99], 500],
        [50, [101, 185, 75, 210, 99], 1000],
        [50, [101, 185, 75, 210, 99], 5000],
        [50, [101, 185, 75, 210, 99], 10000],
        [120, [201, 215, 375, 210, 250], 10000],
    ]

    @staticmethod
    def test_manually_validated_cases():
        cases = {
            ((2, 2), 3) : 6,
        }
        for (set_sizes, ambient_size), expected_count in cases.items():
            for strategy in ['binomial-formula', 'brute-force', 'recursion']:
                assert(_compute_number_of_covers(
                    set_sizes = set_sizes,
                    ambient_size = ambient_size,
                    strategy = strategy,
                ) == expected_count)

    @staticmethod
    def test_consistent_with_previous_runs():
        cases = {
            ((3, 1), 4) : 4,
            ((3, 2), 4) : 12,
        }
        for (set_sizes, ambient_size), expected_count in cases.items():
            for strategy in ['binomial-formula', 'brute-force', 'recursion']:
                assert(_compute_number_of_covers(
                    set_sizes = set_sizes,
                    ambient_size = ambient_size,
                    strategy = strategy,
                ) == expected_count)

    @staticmethod
    def test_binomial_formula_matches_brute_force():
        for set_sizes, ambient_size in TestCoverCounting.sample_cases:
            covers1 = _compute_number_of_covers(
                set_sizes = set_sizes,
                ambient_size = ambient_size,
                strategy = 'binomial-formula'
            )
            covers2 = _compute_number_of_covers(
                set_sizes = set_sizes,
                ambient_size = ambient_size,
                strategy = 'brute-force',
            )
            assert(covers1 == covers2)

    @staticmethod
    def test_binomial_formula_matches_recursion():
        for set_sizes, ambient_size in TestCoverCounting.sample_cases:
            covers1 = _compute_number_of_covers(
                set_sizes = set_sizes,
                ambient_size = ambient_size,
                strategy = 'binomial-formula'
            )
            covers2 = _compute_number_of_covers(
                set_sizes = set_sizes,
                ambient_size = ambient_size,
                strategy = 'recursion',
            )
            assert(covers1 == covers2)

    @staticmethod
    def test_closed_formula_for_cdf():
        p_values = []
        for set_sizes, ambient_size in TestCoverCounting.sample_cases:
            for I in range(1, min(set_sizes)+1):
                p1 = coincidencetest(
                    incidence_statistic = I,
                    frequencies = set_sizes,
                    number_samples = ambient_size,
                    strategy = 'closed-form',
                    format_p_value = False,
                )
                p2 = coincidencetest(
                    incidence_statistic = I,
                    frequencies = set_sizes,
                    number_samples = ambient_size,
                    strategy = 'sum-distribution',
                    format_p_value = False,
                )
                assert(p1 == p2)
                p_values.append((p1,p2))
        return p_values

    @staticmethod
    def gauge_performance_closed_formula_for_cdf():
        times = []
        p_values = []
        for incidence_statistic, set_sizes, ambient_size in TestCoverCounting.extreme_sample_cases:
            tic = time.perf_counter()
            p1 = coincidencetest(
                incidence_statistic = incidence_statistic,
                frequencies = set_sizes,
                number_samples = ambient_size,
                strategy = 'closed-form',
                format_p_value = False,
            )
            toc = time.perf_counter()
            time1 = toc - tic

            tic = time.perf_counter()
            p2 = coincidencetest(
                incidence_statistic = incidence_statistic,
                frequencies = set_sizes,
                number_samples = ambient_size,
                strategy = 'sum-distribution',
                format_p_value = False,
            )
            toc = time.perf_counter()
            time2 = toc - tic

            times.append({'closed-form' : time1, 'sum-distribution' : time2, 'ratio' : time2 / time1})
            p_values.append({'closed-form' : p1,'sum-distribution' : p2})
        return [times, p_values]


class TestStirlingNumberCalc:
    @staticmethod
    def test_small():
        cases = {
            (3, 3) : 1,
            (4, 4) : 1,
            (5, 5) : 1,
            (3, 2) : 3,
        }
        for (ambient_size, number_parts), value in cases.items():
            assert(stirling_second_kind(
                ambient_size=ambient_size,
                number_parts=number_parts,
                normalized=True,
            ) == value)

    @staticmethod
    def test_larger():
        cases = {
            (8, 4) : 1701,
            # (10, 3) : 9330,
            (10, 7) : 5880,
        }
        for (ambient_size, number_parts), value in cases.items():
            assert(stirling_second_kind(
                ambient_size=ambient_size,
                number_parts=number_parts,
                normalized=True,
            ) == value)


class TestExactProbabilityCalc:
    sample_cases = [
        ((3, 3, 3), 5),
        ((3, 4, 5), 7),
        ((5, 7, 10), 20),
        ((5, 5, 5), 80),
        ((10, 10, 10), 100),
    ]

    @staticmethod
    def do_test(set_sizes, ambient_size):
        intersection_cases = [
            (i, set_sizes, ambient_size) for i in range(min(set_sizes) + 1)
        ]
        outputs = {
            intersection_size :
            calculate_probability_of_multicoincidence(
                intersection_size = intersection_size,
                set_sizes = set_sizes,
                ambient_size = ambient_size,
            )
            for intersection_size, set_sizes, ambient_size in intersection_cases
        }
        total = sum(outputs.values())
        cdf = [
            total - sum([outputs[j] for j in range(0, i)]) for i in range(len(outputs))
        ]
        return outputs, cdf # Needs assert

    @staticmethod
    def test_exact_probability_of_intersection():
        for set_sizes, ambient_size in TestExactProbabilityCalc.sample_cases:
            TestExactProbabilityCalc.do_test(set_sizes, ambient_size)


class TestStatisticalSignificanceTest:
    sample_cases = {
        ((1, (2, 2, 2), 10)) : 0.07951,
    }

    @staticmethod
    def test_p_values():
        cases = TestStatisticalSignificanceTest.sample_cases
        for (incidence_statistic, frequencies, number_samples), p_expected in cases.items():
            p = coincidencetest(incidence_statistic, frequencies, number_samples)
            assert(p == p_expected)

