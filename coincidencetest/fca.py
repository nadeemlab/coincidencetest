"""
This module computes "formal concepts" (biclusters in binary feature data) using a
complete or truncated recursive pairwise closure strategy. The "lectic order" method
is not implemented. See [1]_ for a practical introduction to formal concepts, and
see [2]_ for a thorough treatment of the theory.

References
----------
.. [1] Ganter, Bernhard, and Obiedkov, Sergei. Conceptual Exploration. Germany,
       Springer Berlin Heidelberg, 2016.
.. [2] Ganter, Bernhard, and Stumme, Gerd. Formal Concept Analysis: Foundations and
       Applications. Germany, Springer, 2005.
"""
import random
from itertools import combinations

import pandas as pd

from .log_formats import colorized_logger
logger = colorized_logger(__name__)

class ConceptLattice:
    def __init__(self, data, level_limit: int=None, max_recursion: int=None):
        self.data = data
        self.level_limit = level_limit
        self.max_recursion = max_recursion

        if (not self.level_limit is None) or (not self.max_recursion is None):
            logger.debug('Using level limit %s, maximum recursions %s', self.level_limit, self.max_recursion)

        self.closed_sets = []
        self.dual_sets = []
        for feature in self.data.columns:
            closed_set, dual_set = self.closure([feature])
            if not self.already_have(closed_set):
                self.closed_sets.append(closed_set)
                self.dual_sets.append(dual_set)

        self.computed_pairs = []

    def compute_concepts(self):
        level = 1
        while True:
            previous_number_sets = len(self.closed_sets)
            new_pairs_computed = self.do_pairwise_closures()
            new_number_sets = len(self.closed_sets)
            if self.level_limit:
                logger.debug('Completed level %s. %s pairs tried, %s new sets.',
                    level,
                    self.level_limit,
                    new_number_sets - previous_number_sets,
                )
            else:
                logger.debug('Completed level %s. All pairs tried, %s new sets.',
                    level,
                    new_number_sets - previous_number_sets,
                )
            if previous_number_sets == new_number_sets:
                logger.debug('No new pairs at level %s.', level)
                return
            if self.max_recursion and level == self.max_recursion:
                logger.debug('Completed maximum level %s.', level)
                return
            level += 1

    def do_pairwise_closures(self):
        all_pairs = [
            tuple(sorted(c))
            for c in combinations(range(len(self.closed_sets)), 2)
        ]
        index_range = list(set(all_pairs).difference(self.computed_pairs))
        if len(index_range) == 0:
            return False
        new_pairs_computed = False
        if self.level_limit is not None:
            new_pairs = random.sample(index_range, self.level_limit)
        else:
            new_pairs = index_range
        for index1, index2 in new_pairs:
            union = sorted(list(
                set(self.closed_sets[index1]).union(self.closed_sets[index2])
            ))
            closed_set, dual_set = self.closure(union)
            if not self.already_have(closed_set) and len(dual_set) != 0:
                self.closed_sets.append(closed_set)
                self.dual_sets.append(dual_set)
                new_pairs_computed = True
            self.computed_pairs.append((index1, index2))
        return new_pairs_computed

    def closure(self, input_set):
        N = len(input_set)
        samples_mask = self.data.loc[:, input_set].apply(lambda row: sum(row) == N, axis=1)
        samples = sorted(list(self.data.index[samples_mask]))
        M = len(samples)
        features_mask = self.data.loc[samples, :].apply(lambda col: sum(col) == M, axis=0)
        features = sorted(list(self.data.columns[features_mask]))
        return features, samples

    def already_have(self, input_set):
        return input_set in self.closed_sets

def find_concepts(data, level_limit: int=None, max_recursion: int=None):
    """
    Computes the closure of each pair of features, then the closure of each pair of
    the resulting closed sets, etc. If `level_limit` is not None, the number of new
    closures to compute at each recursion level is `level_limit`.

    Parameters
    ----------
    data : pandas.DataFrame
        Binary data matrix, with row and column names. Rows are samples and columns
        are features.
    level_limit: int
        Default None. Limit on the number of new closures to compute per level. These are
        randomized among all possible pairs.
    max_recursion: int
        Default None. Limit on the number of levels.
    """
    lattice = ConceptLattice(data, level_limit=level_limit, max_recursion=max_recursion)
    lattice.compute_concepts()
    return [lattice.closed_sets, lattice.dual_sets]

