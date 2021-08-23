import coincidencetest
from coincidencetest.algorithms.recursion_method import stirling_second_kind

def test_small():
    assert(stirling_second_kind(ambient_size=3, number_parts=3) == 1)
    assert(stirling_second_kind(ambient_size=4, number_parts=4) == 1)
    assert(stirling_second_kind(ambient_size=5, number_parts=5) == 1)
    assert(stirling_second_kind(ambient_size=3, number_parts=2) == 3)

def test_larger():
    assert(stirling_second_kind(ambient_size=8, number_parts=4) == 1701)
    assert(stirling_second_kind(ambient_size=10, number_parts=3) == 9330)
    assert(stirling_second_kind(ambient_size=10, number_parts=7) == 5880)
