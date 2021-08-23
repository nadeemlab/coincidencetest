#!/usr/bin/env python3

import coincidencetest
from coincidencetest.algorithm import stirling_second_kind

def test_stirling_numbers():
    assert(stirling_second_kind(ambient_size=3, number_parts=3) == 1)
    assert(stirling_second_kind(ambient_size=4, number_parts=4) == 1)
    assert(stirling_second_kind(ambient_size=5, number_parts=5) == 1)
    assert(stirling_second_kind(ambient_size=3, number_parts=3) == 3)
    assert(stirling_second_kind(ambient_size=8, number_parts=4) == 1701)
    assert(stirling_second_kind(ambient_size=10, number_parts=3) == 9330)
    assert(stirling_second_kind(ambient_size=10, number_parts=7) == 5880)

if __name__=='__main__':
    print(number_of_covers(set_sizes=(3,1), ambient_size=4))
    print(number_of_covers(set_sizes=(3,3,4), ambient_size=7))
    print(number_of_covers(set_sizes=(18, 15, 16, 8, 18), ambient_size=21))

    l = (18, 15, 16, 8, 18)
    l = tuple([e + 100 for e in l])
    ambient = sum(l)
    print('Ambient size: ' + str(ambient))
    print('Exact value, based on formula for number of partitions: ' + str(number_of_covers(
        set_sizes=l,
        ambient_size=ambient,
    )))


