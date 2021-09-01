from decimal import Decimal

import coincidencetest
from coincidencetest._coincidencetest import compute_number_of_covers
from coincidencetest._coincidencetest import stirling_second_kind
from coincidencetest import calculate_probability_of_multicoincidence


class TestCoverCounting:
    sample_cases = [
        ((2, 2), 3),
        ((3, 1), 4),
        ((3, 2), 4),
        ((3, 3, 4), 7),
        ((3, 3, 5, 2), 8),
    ]

    @staticmethod
    def test_manually_validated_cases():
        cases = {
            ((2, 2), 3) : 6,
        }
        for (set_sizes, ambient_size), expected_count in cases.items():
            for strategy in ['binomial-formula', 'brute-force', 'recursion']:
                assert(compute_number_of_covers(
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
                assert(compute_number_of_covers(
                    set_sizes = set_sizes,
                    ambient_size = ambient_size,
                    strategy = strategy,
                ) == expected_count)

    @staticmethod
    def test_binomial_formula_matches_brute_force():
        for set_sizes, ambient_size in TestCoverCounting.sample_cases:
            covers1 = compute_number_of_covers(
                set_sizes = set_sizes,
                ambient_size = ambient_size,
                strategy = 'binomial-formula'
            )
            covers2 = compute_number_of_covers(
                set_sizes = set_sizes,
                ambient_size = ambient_size,
                strategy = 'brute-force',
            )
            assert(covers1 == covers2)

    @staticmethod
    def test_binomial_formula_matches_recursion():
        for set_sizes, ambient_size in TestCoverCounting.sample_cases:
            covers1 = compute_number_of_covers(
                set_sizes = set_sizes,
                ambient_size = ambient_size,
                strategy = 'binomial-formula'
            )
            covers2 = compute_number_of_covers(
                set_sizes = set_sizes,
                ambient_size = ambient_size,
                strategy = 'recursion',
            )
            assert(covers1 == covers2)


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

    def test_exact_probability_of_intersection(
        set_sizes: tuple=(),
        ambient_size: int=0,
    ):
        for set_sizes, ambient_size in TestExactProbabilityCalc.sample_cases:
            intersection_cases = [
                (i, set_sizes, ambient_size) for i in range(min(set_sizes) + 1)
            ]
            outputs = {
                intersection_size :
                Decimal(calculate_probability_of_multicoincidence(
                    intersection_size = intersection_size,
                    set_sizes = set_sizes,
                    ambient_size = ambient_size,
                ))
                for intersection_size, set_sizes, ambient_size in intersection_cases
            }
            t = sum(outputs.values())
            cdf = [
                t - sum([outputs[j] for j in range(0, i)]) for i in range(len(outputs))
            ]

