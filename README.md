# coincidencetest
This exact test assesses the statistical significance of finding a feature subset in binary feature data such that the number of simultaneously-positive samples is large.

Example usage is shown below:
```py
import coincidencetest
from coincidencetest import coincidencetest
coincidencetest(2, [3, 3, 3, 3], 10)

0.0008877
```
This example shows that the probability is about 0.09% that four features, each occurring with frequency 3/10, will simultaneously occur in 2 or more members.

The example `coincidencetest(1, [5, 3, 7], 100)` yields p=0.01047, showing that the probability of *any* sample having all features can be very low, when enough of the features are individually relatively rare.

## Code testing
The package is tested with
```bash
pytest .
```

The key step is a computation of the number of covers of a set of a given size by sets of prescribed sizes, so the most important tests check that several different algorithms for cover counting agree in small-number cases.
