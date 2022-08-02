### About
This repository contains the code for analysis of IoTa dataset using clustering techniques.

### Setup and execution on Terminal
Install and activate conda environment from master_project.yml

Note: This environment was created on an M1 MacBook running macOS and may not work on other systems, see [Requirements](#requirements) below for a list of main dependencies.

Next, execute the following commands:

cd ../src

./run.sh

Results are by default saved in the `logs` directory.

### Requirements
* `matplotlib`
* `numpy`
* `pandas`
* `networkx`
* `argparse`
* `pathlib`
* `os`
* `random`


### Reproducibility
All experiments are run with a fixed global seed (determined by argument `--seed`) to ensure reproducibility. Unfortunately, actual results may differ slightly due to some unknown stochastic behaviour. Rerunning the experiments may therefore produce slightly different results.
