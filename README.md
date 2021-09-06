# coincidencetest
This exact test assesses the statistical significance of finding a feature subset in binary feature data such that the number of simultaneously-positive samples is large.

## Example
Usage is shown below:
```py
import coincidencetest
from coincidencetest import coincidencetest
coincidencetest(2, [3, 3, 3, 3], 10)

0.0008877
```
This example shows that the probability is about 0.09% that four features, each occurring with frequency 3/10, will simultaneously occur in 2 or more members.

The example `coincidencetest(1, [5, 3, 7], 100)` yields p=0.01047, showing that the probability of *any* sample having all features can be very low, provided that enough of the features are individually relatively rare.

## CLI application
To make the test useful, this package is distributed together with a lightweight "Formal Concept Analysis" feature set discovery tool.

The installed package exposes the command-line program `coincidence-clustering`. Use it like so:
```bash
coincidence-clustering --input-filename=example_data/multiplexed_1500.tsv --output-tsv=out_1500.tsv
```

The contents of `out_1500.csv`:

|Signature             |Frequency|Out of|p-value  |
|----------------------|---------|------|---------|
|CD3 CD8               |64       |1500  |1.452e-13|
|CD3 FOXP3 ICOS        |9        |1500  |5.021e-12|
|FOXP3 ICOS            |12       |1500  |1.678e-10|
|CD3 FOXP3             |24       |1500  |4.23e-08 |
|CD3 ICOS              |27       |1500  |4.522e-08|
|CD3 FOXP3 ICOS PDL1   |2        |1500  |0.0005534|
|CD3 FOXP3 PDL1        |4        |1500  |0.005722 |
|CD3 ICOS PDL1         |4        |1500  |0.01189  |
|FOXP3 PDL1            |5        |1500  |0.1811   |
|CD3 PDL1              |22       |1500  |0.2679   |
|ICOS PDL1             |5        |1500  |0.389    |
|CD3 CD8 FOXP3         |2        |1500  |1.0      |
|CD3 CK                |41       |1500  |1.0      |
|CK FOXP3              |2        |1500  |1.0      |
|CK ICOS               |2        |1500  |1.0      |
|CD3 CD8 CK            |11       |1500  |1.0      |
|CK PDL1               |13       |1500  |1.0      |
|CD8 FOXP3 ICOS        |1        |1500  |1.0      |
|CD3 CK PDL1           |4        |1500  |1.0      |
|CD8 FOXP3             |3        |1500  |1.0      |
|CD3 CD8 PDL1          |1        |1500  |1.0      |
|CD8 CK                |24       |1500  |1.0      |


## Web application
A Javascript port of the signature discovery and testing program is located in `webapp/`. To run it locally, use:

```bash
cd webapp/
chmod +x build.py
./build.py
python -m http.server 8080
```

Then open your browser to `localhost:8080` or `0.0.0.0:8080`.

*Note*: The application only requires the server to have the capability of serving static files, namely the files `index.html` and `worker.js` created by the build process. However, most browsers block the use of the "web workers" from the local file system, so this minimal Python server is needed for local deployment. We use web workers in order to allow dynamic display of feature sets in real-time as they are identified.

## Code testing
The package is tested with
```bash
pytest .
```

The key step is a computation of the number of covers of a set of a given size by sets of prescribed sizes, so the most important tests check that several different algorithms for cover counting agree in small-number cases.
