from decimal import Decimal

import coincidencetest
from coincidencetest.algorithm import calculate_probability_of_multicoincidence

def do_example(
    set_sizes = (3, 3, 3),
    ambient_size = 5,
):
    cases = [(i, set_sizes, ambient_size) for i in range(min(set_sizes) + 1)]
    outputs = {
        intersection_size :
        Decimal(calculate_probability_of_multicoincidence(
            intersection_size = intersection_size,
            set_sizes = set_sizes,
            ambient_size = ambient_size,
        ))
        for intersection_size, set_sizes, ambient_size in cases
    }
    t = sum(outputs.values())
    cdf = [
        t - sum([outputs[j] for j in range(0, i)]) for i in range(len(outputs))
    ]

    print('For')
    print('subset sizes = ' + str(set_sizes))
    print('ambient set size = ' + str(ambient_size))
    print('the distribution of the coincidence degree test statistic is:')
    print('')
    print('\n'.join(str(i) + ' : ' + str(p) for i, p in outputs.items()))
    print('')
    print('Total probability: ' + str(t))
    print('')
    print('CDF:')
    print('\n'.join([str(i) + ' : ' + str(cdf[i]) for i in range(len(cdf))]))
    print('')

def basic_running_examples():
    do_example(set_sizes = (3, 3, 3), ambient_size = 5)
    do_example(set_sizes = (3, 4, 5), ambient_size = 7)
    do_example(set_sizes = (5, 7, 10), ambient_size = 20)
    do_example(set_sizes = (5, 5, 5), ambient_size = 80)
    do_example(set_sizes = (10, 10, 10), ambient_size = 100)

if __name__=='__main__':
    basic_running_examples()
