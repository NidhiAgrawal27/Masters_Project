import pandas as pd
import argparse
import pathlib
import os
from utilities import utils, visualization


PATHNAMES = utils.pathnames()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, help="random seed", required=True)
    args = parser.parse_args()
    utils.set_seed(args.seed)

    df = pd.read_csv(PATHNAMES['processed_data'], parse_dates=['datetime'])
    df_tx_count_per_date = df.groupby([df['datetime'].dt.date]).size()

    tx_label = 'Number of transactions'
    date_label = 'Date'
    title = 'Total number of transactions on each date'
    ylog = 0
    rotation = 70

    # Create 'generated_files' directory if it does not exist.
    pathlib.Path(PATHNAMES["tx_basic_analysis_fig_dir"]).mkdir(parents=True, exist_ok=True)
    
    # Number of transaction on each date - Bar graph
    fig1 = visualization.plot_bar_or_line_graph(df_tx_count_per_date, 'bar', tx_label, date_label, title, 'cyan', ylog, rotation)
    fig1.savefig(os.path.join(PATHNAMES["tx_basic_analysis_fig_dir"], 'num_tx_per_date.png'), bbox_inches="tight")

    # Number of transaction on each date - Line graph
    title = 'Trend of number of transactions on each date'
    fig2 = visualization.plot_bar_or_line_graph(df_tx_count_per_date, 'line', tx_label, date_label, title, 'cyan', ylog, rotation)
    fig2.savefig(os.path.join(PATHNAMES["tx_basic_analysis_fig_dir"], 'num_tx_per_date_trend.png'), bbox_inches="tight")

    # Number of transactions where sum of input amounts != sum of output amounts
    tx_ipSum_notEqual_opSum = df.loc[df['sum_input_amounts'] != df['sum_output_amounts']].shape[0]
    print('\nNumber of transactions where sum of input amounts is not equal to sum of output amounts: {}\n'.format(tx_ipSum_notEqual_opSum))

    # Number of transactions with input addresses > 1
    df_ip_addrs_more_than_1 = df.loc[df['num_input_addresses'] > 1]
    print('Number of transactions with input addresses more than 1: {}\n'.format(df_ip_addrs_more_than_1.shape[0]))

    df_ip_addrs_more_than_1_count_per_date = df_ip_addrs_more_than_1.groupby([df_ip_addrs_more_than_1['datetime'].dt.date]).size()
    title = 'Number of transactions on each date where input addresses > 1'
    fig3 = visualization.plot_bar_or_line_graph(df_ip_addrs_more_than_1_count_per_date, 'bar', tx_label, date_label, title, 'blue', ylog, rotation)
    fig3.savefig(os.path.join(PATHNAMES["tx_basic_analysis_fig_dir"], 'num_tx_ip_adrs.png'), bbox_inches="tight")

    # Number of transactions with input addresses = 1
    df_ip_addrs_equalto_1 = df.loc[df['num_input_addresses'] == 1]
    df_ip_addrs_equalto_1_count_per_date = df_ip_addrs_equalto_1.groupby([df_ip_addrs_equalto_1['datetime'].dt.date]).size()
    title = 'Number of transactions on each date where input addresses = 1'

    fig4 = visualization.plot_bar_or_line_graph(df_ip_addrs_equalto_1_count_per_date, 'bar', tx_label, date_label, title, 'blue', ylog, rotation)
    fig4.savefig(os.path.join(PATHNAMES["tx_basic_analysis_fig_dir"], 'num_tx_ip_adrs_equal1.png'), bbox_inches="tight")

    # Number of transactions with output addresses > 1
    df_op_addrs_more_than_1 = df.loc[df['num_output_addresses'] > 1]
    print('Number of transactions with output addresses more than 1: {}\n'.format(df_op_addrs_more_than_1.shape[0]))
    
    df_op_addrs_more_than_1_count_per_date = df_op_addrs_more_than_1.groupby([df_op_addrs_more_than_1['datetime'].dt.date]).size()
    title = 'Number of transactions on each date where output addresses > 1'

    fig5 = visualization.plot_bar_or_line_graph(df_op_addrs_more_than_1_count_per_date, 'bar', tx_label, date_label, title, 'red', ylog, rotation)
    fig5.savefig(os.path.join(PATHNAMES["tx_basic_analysis_fig_dir"], 'num_tx_op_adrs.png'), bbox_inches="tight")

    # Number of transactions with output addresses = 1
    df_op_addrs_equalto_1 = df.loc[df['num_output_addresses'] == 1]
    df_op_addrs_equalto_1_count_per_date = df_op_addrs_equalto_1.groupby([df_op_addrs_equalto_1['datetime'].dt.date]).size()
    title = 'Number of transactions on each date where output addresses = 1'

    fig6 = visualization.plot_bar_or_line_graph(df_op_addrs_equalto_1_count_per_date, 'bar', tx_label, date_label, title, 'red', ylog, rotation)
    fig6.savefig(os.path.join(PATHNAMES["tx_basic_analysis_fig_dir"], 'num_tx_op_adrs_equal1.png'), bbox_inches="tight")

    # Distribution of number of input addresses
    ip_adrs_label = 'Number of input addresses'
    title = 'Distribution of number of input addresses'
    ylog = 1
    rotation = 0
    fig7 = visualization.plot_bar_or_line_graph(df['num_input_addresses'].value_counts(), 'bar', tx_label, ip_adrs_label, title, 'blue', ylog, rotation)
    fig7.savefig(os.path.join(PATHNAMES["tx_basic_analysis_fig_dir"], 'ip_addrs_dist.png'), bbox_inches="tight")

    # Distribution of number of output addresses
    op_adrs_label = 'Number of output addresses'
    title = 'Distribution of number of output addresses'
    fig8 = visualization.plot_bar_or_line_graph(df['num_output_addresses'].value_counts(), 'bar', tx_label, op_adrs_label, title, 'red', ylog, rotation)
    fig8.savefig(os.path.join(PATHNAMES["tx_basic_analysis_fig_dir"], 'op_addrs_dist.png'), bbox_inches="tight")



if __name__ == "__main__":
    main()

