import math

from ..utilities import binom

def number_of_covers(
    set_sizes: tuple=(),
    ambient_size: int=0,
):
    """
    q(N, k, n1, ..., nk) = ∑ (-1)^(N+m) {N, m} {m, n1} ... {m, nk}  
    """
    N = ambient_size
    n = set_sizes
    sign = lambda x: 1 if x % 2 == 0 else -1
    terms = [
        sign(N + m) * binom(N, m) * math.prod([binom(m, n[i]) for i in range(len(n))])
        for m in range(min(n), N)
    ]
    return sum(terms)
