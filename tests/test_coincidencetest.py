import coincidencetest
from coincidencetest._coincidencetest import compute_number_of_covers
from coincidencetest._coincidencetest import stirling_second_kind


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
            ((3, 3, 4), 7) : 10815,
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
            (10, 3) : 9330,
            (10, 7) : 588,
        }
        for (ambient_size, number_parts), value in cases.items():
            assert(stirling_second_kind(
                ambient_size=ambient_size,
                number_parts=number_parts,
                normalized=True,
            ) == value)

