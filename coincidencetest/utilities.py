from functools import lru_cache
from math import factorial

@lru_cache(maxsize=10000)
def binom(
    ambient_size: int=0,
    subset_size: int=0,
):
    return factorial(ambient_size) //   \
            factorial(subset_size) //   \
            factorial(ambient_size - subset_size)
