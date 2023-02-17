### About
This repository contains the code for analysis of various cryptocurrency datasets using clustering techniques.

### Setup and execution on Terminal
Install and activate conda environment 'master_proj_env' from conda_env.yml
(The name of the environment can be changed in the conda_env.yml file.)

Next, execute the following steps:
1. Go to directory correspondence_network/src using command:
    $ cd correspondence_network/src
2. Change appropriate path names for fetching data and creating log files in src/utilities/pathnames.py files.
3. Run the following command to run the bash script to run the main file in src folder. The arguments in run.sh script can be altered as per the requirements of the user.
    $ ./run.sh

Results are by default saved in the `logs` directory generated on path given in src/utilities/pathnames.py file.

### Reproducibility
All experiments are run with a fixed global seed (determined by argument `--seed`) to ensure reproducibility. Unfortunately, actual results may differ slightly due to some unknown stochastic behaviour. Rerunning the experiments may therefore produce slightly different results.

