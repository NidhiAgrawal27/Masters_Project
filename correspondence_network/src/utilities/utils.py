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


def pathnames(cur, heuristic):

    if cur == 'btc':
        dir_name = "../logs/Bitcoin_logs/" + heuristic + '/'
        data_path = "../data/chunk.csv"
    elif cur == 'iota': 
        dir_name = "../logs/IoTa_logs/" + heuristic + '/'
        data_path = "../data/first_14_days_UTXO_txs_of_IOTA.csv"
    else: 
        dir_name = "../logs/sample_logs/" + heuristic + '/'
        data_path = "../data/sample_data.csv"

    PATHNAMES = {
            "data_path": data_path,
            "figure_dir": dir_name + "figures/",
            "generated_files": dir_name + "generated_files/"
        }

    return PATHNAMES

