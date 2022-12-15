import pandas as pd
import argparse
import pathlib
import os
import pickle
from utilities import clustering_script
from utilities import set_seed, pathnames
from utilities.visualization import plot_metrics

import warnings
warnings.filterwarnings('ignore')

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, help="random seed", required=True)
    parser.add_argument("--currency", type=str, help="currency name example - btc: Bitcoin, iota: IoTa", required=True)
    parser.add_argument("--weighted", type=str, help="Weighted graph: yes or no", required=True)
    args = parser.parse_args()

    set_seed.set_seed(args.seed)
    cur = args.currency
    weighted = args.weighted

    PATHNAMES = pathnames.pathnames(cur, 'all', weighted)
    pathlib.Path(PATHNAMES['figure_dir']).mkdir(parents=True, exist_ok=True)
    dir_generated_files = PATHNAMES['generated_files']
    fig_dir = PATHNAMES['figure_dir']
    fig_dir = fig_dir + cur + '_'
    
    wt = 'unweighted'
    if weighted == 'yes':
        wt = 'weighted'
        fig_dir = fig_dir + 'wt_'

    print('\n\n*********************** Plots of metrics of ' + cur + ' ' + wt + ' initiated ***********************\n')    
    
    # Plot metrics
    metrics = ['n_clusters','ami', 'urs', 'homog', 'mod']
    metric_names = ['Number of Cluster', 'AMI', 'ARI', 'Homogeneity', 'Modularity']
    df_list = []
    title_list = []
    heuristics = ['h0', 'h0_h1']
    for heuristic in heuristics:
        PATHNAMES = pathnames.pathnames(cur, heuristic, weighted)
        dir_generated_files = PATHNAMES['generated_files']
        path = pathlib.Path(dir_generated_files).iterdir()
        files = []
        for x in path:
            if heuristic == 'h0':
                if x.is_file() and f"h0_edge_data" in x.stem and f'known_entity_counts' not in x.stem: files.append(x)
            else:
                if x.is_file() and f"h0_h1" in x.stem and f'known_entity_counts' not in x.stem: files.append(x)
        title = cur + ' ' + heuristic + ' ' + wt
        df = pd.read_csv(f"./{files[0]}")
        for i in range(len(files)-1):
            df_next = pd.read_csv(f"./{files[i+1]}")
            # sum of column of metrics across all output files
            for m in metrics:
                df[m] = df[m] + df_next[m]
        # mean of each metric column in df(which now has the sum of metrics over all files of pair h0 and h1)
        for m in metrics:
            df[m] = df[m]/len(files)
        df_list.append(df)
        title_list.append(title)
    plot_metrics(df_list, title_list, metrics, metric_names, fig_dir)

    print('\n\n*********************** Plots of metrics of ' + cur + ' ' + wt + ' completed ***********************\n')
    print()

if __name__ == "__main__":
    main()


