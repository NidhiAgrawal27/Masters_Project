import pandas as pd
import pathlib
from plot_visualization import plot_density_graph, plot_edges, plot_modularity_graph, plotPowerLaw_superimpose,plot_densitygraph_vertical,plot_find_exponent


def main(load_dir, save_dir, currencies, weighted, modularity_file):

    df_mod = pd.read_csv(modularity_file)

    for cur in currencies:

        for wt in weighted:
        
            fig_path = save_dir + cur + '/' + wt + '/'
            pathlib.Path(fig_path).mkdir(parents=True, exist_ok=True)

            title_h0 = ' '.join(cur.split('_')).capitalize() + ' h0'
            load_path_h0 = load_dir + cur + '_logs/' + wt + '/h0/generated_files/' + cur + '_h0'
            save_fig_dir_h0 = fig_path + cur + '_h0_'

            title_h0_h1 = ' '.join(cur.split('_')).capitalize() + ' h0_h1'
            load_path_h0_h1 = load_dir + cur + '_logs/' + wt + '/h0_h1/generated_files/' + cur + '_h0_h1'
            save_fig_dir_h0_h1 = fig_path + cur + '_h0_h1_'

            if wt == 'weighted':
                comp_h0 = load_path_h0 + '_wt_components.csv'
                comp_h0_h1 = load_path_h0_h1 + '_wt_components.csv'
                save_fig_dir_h0 = save_fig_dir_h0 + 'wt_'
                save_fig_dir_h0_h1 = save_fig_dir_h0_h1 + 'wt_'
            else: 
                comp_h0 = load_path_h0 + '_components.csv'
                comp_h0_h1 = load_path_h0_h1 + '_components.csv'

            df_components_h0 = pd.read_csv(comp_h0)
            df_components_h0_h1 = pd.read_csv(comp_h0_h1)

            modularity = df_mod['modularity'].loc[df_mod['graph'] == cur + '_' + 'h0' + '_' + wt].values.item()

            plot_density_graph(df_components_h0['num_of_addrs'], 'Number of addesses', save_fig_dir_h0 + 'density_plot.png', cur, 'h0')
            plot_modularity_graph(df_components_h0, "num_of_communities", title_h0, save_fig_dir_h0 + 'comp_size_communities.png')
            plot_modularity_graph(df_components_h0, "modularity", 'Modularity of ' + title_h0 + ' graph: ' + str(round(modularity, 4)), save_fig_dir_h0 + 'comp_size_modularity.png')
            plot_density_graph(df_components_h0_h1['num_of_addrs'], 'Number of addesses', save_fig_dir_h0_h1 + 'density_plot.png', cur, 'h0_h1')            
            plotPowerLaw_superimpose(df_components_h0['num_of_addrs'], df_components_h0_h1['num_of_addrs'], cur, 'h0', 'h0_h1', fig_path + cur + '_powerlaw_plot.png', xmin= None, xmax = None)
            plot_edges(df_components_h0, cur, save_fig_dir_h0 + 'edges.png')
            plot_edges(df_components_h0_h1, cur, save_fig_dir_h0_h1 + 'edges.png')
            plot_densitygraph_vertical((df_components_h0,df_components_h0_h1,'num_of_addrs',fig_path + cur + 'stacked_density_plots.png' , cur, 'h0', 'h0_h1'))
            plot_find_exponent(df_components_h0, 'num_of_communities', title_h0, save_fig_dir_h0)
            plot_find_exponent(df_components_h0_h1, 'num_of_communities', title_h0_h1, save_fig_dir_h0_h1)
            # plot_modularity_graph(df_components_h0, "num_of_edges", title_h0, save_fig_dir_h0 + 'comp_size_edges.png')
            # plot_modularity_graph(df_components_h0_h1, "num_of_edges", title_h0_h1, save_fig_dir_h0_h1 + 'comp_size_edges.png')
            # plotPowerLaw(df_components_h0['num_of_addrs'], cur, 'h0', save_fig_dir_h0 + 'powerlaw_plot.png')
            # plotPowerLaw(df_components_h0_h1['num_of_addrs'], cur, 'h0_h1', save_fig_dir_h0_h1 + 'powerlaw_plot.png')
            


if __name__ == "__main__":

    # load_dir = '/local/scratch/correspondence_network/part1_final_logs/'
    # save_dir = '/local/scratch/correspondence_network/part1_plots/'
    # modularity_file = '/local/scratch/correspondence_network/part1_plots/modularity_of_all_graphs.csv'
    
    load_dir = '/Users/nidhiagrawal/Desktop/Assignments/MastersProject/Github/FINAL/part1_final_logs/'
    save_dir = '../logs/plot_results/'
    modularity_file = '../logs/modularity_of_all_graphs.csv'

    currencies = ['feathercoin']#, 'btc_sample', 'iota_14days', 'iota', 'monacoin']
    weighted = ['weighted', 'unweighted']
    
    main(load_dir, save_dir, currencies, weighted, modularity_file)

