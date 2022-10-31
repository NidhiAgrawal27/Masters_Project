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

    dir_name = "../logs/" + cur + "_logs/" + heuristic + '/'
        
    if cur == 'btc_sample':       data_path = "../data/btc_sample.csv"
    elif cur == 'btc_2012':       data_path = "/local/scratch/btc_trx/BTC_TXS.csv"
    elif cur == 'iota_14days':    data_path = "../data/first_14_days_UTXO_txs_of_IOTA.csv"
    elif cur == 'iota_split':     data_path = "../data/first_14_days_UTXO_txs_of_IOTA.csv"
    elif cur == 'iota':           data_path = "/local/scratch/exported/iota_tx_data.csv"
    elif cur == 'cardano':        data_path = "/local/scratch/btc_trx/ADA_TXS.csv"
    elif cur == 'feathercoin':    data_path = "/local/scratch/btc_trx/FTC_TXS.csv"
    elif cur == 'monacoin':       data_path = "/local/scratch/btc_trx/MONA_TXS.csv"
    else: data_path = "../data/sample_data.csv"

    PATHNAMES = {
                    "data_path": data_path,
                    "figure_dir": dir_name + "figures/",
                    "generated_files": dir_name + "generated_files/"
                }

    return PATHNAMES

