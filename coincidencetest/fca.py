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
import pandas as pd

