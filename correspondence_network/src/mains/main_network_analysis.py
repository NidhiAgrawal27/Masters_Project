import pandas as pd
import argparse
import pathlib
from utilities.visualization import plot_bar_or_line_graph
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

    PATHNAMES = utils.pathnames(cur, heuristic)
    fig_dir = PATHNAMES['figure_dir']

    df = pd.read_csv(PATHNAMES['generated_files'] + 'components.csv')

    pathlib.Path(fig_dir).mkdir(parents=True, exist_ok=True)

    plot_bar_or_line_graph(df['num_of_addrs'], 'line', 0, 'Component Number', 'Num of addresses', 
                        'Num of addesses in each component', 'red', 0, fig_dir+'line_chart_num_of_addrs_vs_comp')
    plot_bar_or_line_graph(df['num_of_addrs'], 'bar', 0, 'Component Number', 'Num of addresses', 
                        'Num of addesses in each component', 'blue', 0, fig_dir+'bar_chart_num_of_addrs_vs_comp')
    
    df_grouped_by_num_addrs = df.groupby(['num_of_addrs']).size()
    plot_bar_or_line_graph(df_grouped_by_num_addrs, 'bar', 1, 'Number of addresses in component', 
                            'Num of Components', 'Distribution of addresses in components', 'cyan', 0, 
                            fig_dir+'dist_addrs_in_comp')
        

    plot_bar_or_line_graph(df['num_of_addrs'], 'line', 0, 'Component Number', 'Num of addresses', 
                        'Num of addesses in each component', 'red', 'x', fig_dir+'log_line_chart_num_of_addrs_vs_comp')
    plot_bar_or_line_graph(df['num_of_addrs'], 'bar', 0, 'Component Number', 'Num of addresses', 
                        'Num of addesses in each component', 'blue', 'x', fig_dir+'log_bar_chart_num_of_addrs_vs_comp')
    plot_bar_or_line_graph(df_grouped_by_num_addrs, 'bar', 1, 'Number of addresses in component', 
                            'Num of Components', 'Distribution of addresses in components', 'cyan', 'y', 
                            fig_dir+'log_dist_addrs_in_comp')


if __name__ == "__main__":
    main()


