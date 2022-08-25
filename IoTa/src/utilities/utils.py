import os
import random
import numpy as np

def set_seed(seed):
    """Set random seed for reproducibility.

    Args:
        seed (int): random seed.
    """
    os.environ["PYTHONHASHSEED"] = str(seed)
    random.seed(seed)
    np.random.seed(seed)


def pathnames():

    dir_name = "../logs/IoTa_logs/"

    PATHNAMES = {
            "data_path": "../data/first_14_days_UTXO_txs_of_IOTA.csv",
            # "data_path": "../data/sample_data.csv",
            "figure_dir": dir_name + "figures/",
            "generated_files": dir_name + "generated_files/",
            "processed_data": dir_name + "generated_files/processed_data.csv",
            "addresses_data": dir_name + "generated_files/unique_addresses.csv",
            "segregated_data": dir_name + "generated_files/segregated_data.csv",
            "heuristics": dir_name + "generated_files/heuristics.csv",
            "segregated_data_gml": dir_name + "generated_files/segregated_data_gml.gml",
            "network_analysis_fig_dir": dir_name + "figures/network_analysis/",
            "tx_basic_analysis_fig_dir": dir_name + "figures/tx_basic_analysis/",
        }

    return PATHNAMES

