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


def pathnames(cur, heuristic, data_is_split):

    if data_is_split == 1:
        dir_name = "../logs/" + 'split/' + cur + "_logs/" + heuristic + '/'
    else:
        dir_name = "../logs/" + cur + "_logs/" + heuristic + '/'
        
    if cur == 'btc':
        data_path = "../data/btc.csv"
    elif cur == 'iota':
        data_path = "../data/first_14_days_UTXO_txs_of_IOTA.csv"
    else:
        data_path = "../data/sample_data.csv"

    PATHNAMES = {
            "data_path": data_path,
            "figure_dir": dir_name + "figures/",
            "generated_files": dir_name + "generated_files/"
        }

    return PATHNAMES

