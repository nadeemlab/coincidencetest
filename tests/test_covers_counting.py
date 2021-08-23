
import coincidencetest
import coincidencetest.algorithms.recursion_method as rm
import coincidencetest.algorithms.brute_force as bf

def test_manually_validated_cases():
    cases = {
        ((2, 2), 3) : 6,
    }
    for (set_sizes, ambient_size), expected_count in cases.items():
        assert(rm.number_of_covers(
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
        assert(rm.number_of_covers(
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
        library_calculated = rm.number_of_covers(
            set_sizes = set_sizes,
            ambient_size = ambient_size,
        )
        brute_force = bf.number_of_covers(
            set_sizes = set_sizes,
            ambient_size = ambient_size,
        )
        assert(library_calculated == brute_force)

def large_non_crashing_example():
    l = (18, 15, 16, 8, 18)
    l = tuple([e + 100 for e in l])
    ambient = sum(l)
    print('Ambient size: ' + str(ambient))
    print('Exact value, based on formula for number of partitions: ' + str(rm.number_of_covers(
        set_sizes=l,
        ambient_size=ambient,
    )))

if __name__=='__main__':
    large_non_crashing_example()
