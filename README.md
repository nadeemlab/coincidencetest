This exact test assesses the statistical significance of finding a feature subset in binary feature data such that the number of simultaneously-positive samples is large.

Everything needed to perform the test is located in the standalone module [_coincidencetest.py](https://github.com/nadeemlab/coincidencetest/blob/main/coincidencetest/_coincidencetest.py).

## Example
Install from [PyPI](https://pypi.org/project/coincidencetest/):
```bash
pip install coincidencetest
```

Usage is shown below:
```py
import coincidencetest
from coincidencetest import coincidencetest
coincidencetest(2, [3, 3, 3, 3], 10)

0.0008877
```
This example shows that the probability is about 0.09% that four features, each occurring with frequency 3/10, will simultaneously occur in 2 or more samples.

The example `coincidencetest(1, [5, 3, 7], 100)` yields p=0.01047, showing that the probability of *even just one* sample having all features can be very low, provided that enough of the features are individually relatively rare.

## CLI application
To make the test immediately useful, this package is distributed together with a lightweight "Formal Concept Analysis" feature set discovery tool.

The installed package exposes the command-line program `coincidence-clustering` incoporating this tool. Use it like so:
```bash
coincidence-clustering \
  --input-filename=example_data/bc_cell_data.tsv \
  --output-tsv=signatures.tsv \
  --level-limit=50 \
  --max-recursion=3
```

## Web application
A Javascript port of the signature discovery and testing program is located in `webapp/`. To run it locally, use:

```bash
cd webapp/
chmod +x build.py
./build.py
python -m http.server 8080
```

Then open your browser to `localhost:8080` or `0.0.0.0:8080`.

*Note*: The Javascript application only requires the server to have the capability of serving static files, namely the files `index.html` and `worker.js` created by the build process. However, most browsers block the use of the "web workers" from the local file system, so this minimal Python server is needed for local deployment. We use web workers in order to allow dynamic display of feature sets in real-time as they are identified.

## Code testing
The package is tested with
```bash
pytest .
```

The key step is a computation of the number of covers of a set of a given size by sets of prescribed sizes (equivalently, the number of subsets of prescribed sizes without common intersection), so the most important tests check that several different algorithms for cover counting agree in small-number cases.

## Issues
Please report all issues as [GitHub issues](https://github.com/nadeemlab/coincidencetest/issues).

## License
© [Nadeem Lab](https://nadeemlab.org/) - The [core module](https://github.com/nadeemlab/coincidencetest/blob/main/coincidencetest/_coincidencetest.py) is distributed under the [3-clause BSD license](https://opensource.org/licenses/BSD-3-Clause). All other modules are distributed under [Apache 2.0 with Commons Clause](https://commonsclause.com) license, and are available for non-commercial academic purposes.

## Reference
If you use this code or parts of it, please cite [our paper](https://arxiv.org/abs/2109.13876):
```
@article{mathews2021coincidencetest,
  title={An exact test for significance of clusters in binary data},
  author={Mathews, James C, and Crowe, Cameron and Vanguri, Rami and Callahan, Margaret and Hollmann, Travis J and and Nadeem, Saad},
  journal={arXiv},
  year={2021}
}
```
