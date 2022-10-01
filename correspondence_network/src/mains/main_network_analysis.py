from __future__ import annotations
import pandas as pd
import argparse
import pathlib
from utilities.visualization import plot_graph
from utilities import utils


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, help="random seed", required=True)
    parser.add_argument("--currency", type=str, help="btc: Bitcoin, iota: IoTa", required=True)
    parser.add_argument("--heuristic", type=str, help="Name of heuristic: h0, or h0+h1", required=True)

    args = parser.parse_args()

    utils.set_seed(args.seed)
    cur = args.currency
    heuristic = args.heuristic
    
    if cur in ['btc_3GB_chunk', 'btc', 'cardano']: data_is_split = 1
    else: data_is_split = 0
    
    PATHNAMES = utils.pathnames(cur, heuristic, data_is_split)
    fig_dir = PATHNAMES['figure_dir']

    df = pd.read_csv(PATHNAMES['generated_files'] + 'components.csv')

    pathlib.Path(fig_dir).mkdir(parents=True, exist_ok=True)

    df_grouped_by_num_addrs = df.groupby(['num_of_addrs']).size()
    yes_annotation = 1
    no_annotation = 0

    if 'btc' in cur: logscale = 'xy'
    elif 'iota' in cur: logscale = 'x'
    else: logscale = 0

    plot_graph(df['num_of_addrs'], 'line', no_annotation, 
                'Component Number', 'Num of addresses', 
                'Num of addesses in each component', 'red', 
                logscale, fig_dir+'line_num_of_addrs_vs_comp')

    plot_graph(df['num_of_addrs'], 'bar', no_annotation, 
                'Component Number', 'Num of addresses', 
                'Num of addesses in each component', 'blue', 
                logscale, fig_dir+'bar_num_of_addrs_vs_comp')
    
    
    if 'btc' in cur: logscale = 'xy'
    elif 'iota' in cur: logscale = 'y'
    else: logscale = 0

    plot_graph(df_grouped_by_num_addrs, 'bar', yes_annotation, 
                'Number of addresses', 
                'Num of Components', 'Distribution of addresses in components', 'cyan', 
                logscale, fig_dir+'dist_addrs_in_comp')

    plot_graph(df['num_of_addrs'], 'dist', no_annotation, 
                'Num of addresses n', 
                'Probability a component has n addresses', 
                'Probability Distribution', 'red', 
                logscale, fig_dir+'prob_dist_addrs_in_comp')

    print(cur + ' ' + heuristic + ': plotting graphs completed.')

if __name__ == "__main__":
    main()


