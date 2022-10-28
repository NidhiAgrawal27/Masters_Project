### About
This repository contains the code for analysis of cryptocurrency datasets using clustering techniques.

### Setup and execution on Terminal
Install and activate conda environment 'p38' from conda_env.yml

Next, execute the following commands:

cd correspondence_network/src

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
* `graph_tool`


### Reproducibility
All experiments are run with a fixed global seed (determined by argument `--seed`) to ensure reproducibility. Unfortunately, actual results may differ slightly due to some unknown stochastic behaviour. Rerunning the experiments may therefore produce slightly different results.

# Testing
