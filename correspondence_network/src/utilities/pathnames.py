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


def pathnames(cur, heuristic, weighted):

    local_dir = '../logs/' 
    server_dir = '/local/scratch/correspondence_network/'

    # below: change local_dir or server_dir in dir_name for accessing local or server dir
    if weighted == 'no': dir_name = local_dir + cur + '_logs/unweighted/' + heuristic + '/'
    else: dir_name = local_dir + cur + '_logs/weighted/' + heuristic + '/'
    
    local_data_dir = '../data/'
    server_data_dir = '/local/scratch/'
        
    if cur == 'btc_sample':       data_path = local_data_dir + 'btc_sample.csv'
    elif cur == 'iota_14days':    data_path = local_data_dir + 'first_14_days_UTXO_txs_of_IOTA.csv'
    elif cur == 'iota_split':     data_path = local_data_dir + 'first_14_days_UTXO_txs_of_IOTA.csv'
    elif cur == 'btc_2012':       data_path = server_data_dir + 'btc_trx/BTC_TXS.csv'
    elif cur == 'iota':           data_path = server_data_dir + 'exported/iota_tx_data/IOTA_1year_tx_data.csv'
    elif 'cardano' in cur:        data_path = server_data_dir + 'btc_trx/ADA_TXS.csv'
    elif cur == 'feathercoin':    data_path = server_data_dir + 'btc_trx/FTC_TXS.csv'
    elif cur == 'monacoin':       data_path = server_data_dir + 'btc_trx/MONA_TXS.csv'
    else: 
        print('Data Path not found for currency ' + cur + '. Check path or pathnames.py file for the entry of this currency')

    # below: change local_dir or server_dir in dir_name for accessing local or server dir
    if weighted == 'no': 
        load_graph_dir = server_dir + 'part1_final_logs/' + cur + '_logs/unweighted/' + heuristic + '/generated_files/graph/'
    else: load_graph_dir = server_dir + 'part1_final_logs/' + cur + '_logs/weighted/' + heuristic + '/generated_files/graph/'

    PATHNAMES = {
                    "data_path": data_path,
                    "figure_dir": dir_name + "figures/",
                    "generated_files": dir_name + "generated_files/",
                    "load_graph_dir": load_graph_dir,
                    "logs_home_dir" : local_dir
                }

    return PATHNAMES

