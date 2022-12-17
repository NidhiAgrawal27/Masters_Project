import pandas as pd
import argparse
import pathlib
from utilities import clustering_script
from utilities import set_seed, pathnames

import warnings
warnings.filterwarnings('ignore')

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, help="random seed", required=True)
    parser.add_argument("--currency", type=str, help="currency name example - btc: Bitcoin, iota: IoTa", required=True)
    parser.add_argument("--heuristic", type=str, help="name of heuristic, example: h0, or h0_h1", required=True)
    parser.add_argument("--weighted", type=str, help="Weighted graph: yes or no", required=True)
    args = parser.parse_args()

    set_seed.set_seed(args.seed)
    cur = args.currency
    heuristic = args.heuristic
    weighted = args.weighted

    PATHNAMES = pathnames.pathnames(cur, heuristic, weighted)
    pathlib.Path(PATHNAMES['generated_files']).mkdir(parents=True, exist_ok=True)
    pathlib.Path(PATHNAMES['figure_dir']).mkdir(parents=True, exist_ok=True)
    dir_generated_files = PATHNAMES['generated_files']
    fig_dir = PATHNAMES['figure_dir']
    fig_dir = fig_dir + cur + '_' + heuristic + '_'
    
    data_path = PATHNAMES['data_path']
    data_dir = data_path + cur + '/' + cur
    address_id_file = data_dir + '_' + heuristic + '_address_ids.csv' 
    edge_data_file = data_dir + '_' + heuristic + '_edge_data.csv'

    wt = 'unweighted'
    if weighted == 'yes':
        wt = 'weighted'
        address_id_file = data_dir + '_' + heuristic + '_wt_address_ids.csv' 
        edge_data_file = data_dir + '_' + heuristic + '_wt_edge_data.csv'
        fig_dir = fig_dir + '_wt_'

    print('\n\n*********************** Processing of ' + cur + ' ' + heuristic + ' ' + wt + ' initiated ***********************\n')    
    print('file_name: ', edge_data_file)
    
    df_edge_data = pd.read_csv(edge_data_file)
    df_address_id = pd.read_csv(address_id_file)
    df_gt = pd.read_csv(PATHNAMES['ground_truth_path'])
    
    # map actual addresses to address ids
    df_edge_data['node1'] = df_edge_data['node1'].map(df_address_id.set_index('address_id')['address'])
    df_edge_data['node2'] = df_edge_data['node2'].map(df_address_id.set_index('address_id')['address'])
    
    clustering_script.clustering(df_edge_data, df_gt, cur + '_' + heuristic + '_edge_data', heuristic, dir_generated_files)

    print('\n\n*********************** Processing of ' + cur + ' ' + heuristic + ' ' + wt + ' completed ***********************\n')
    print()

if __name__ == "__main__":
    main()


