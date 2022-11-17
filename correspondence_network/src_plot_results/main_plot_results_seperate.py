import pandas as pd
import pathlib
# from utilities.visualization import plot_density_graph, plotPowerLaw, plot_modularity_graph
from plot_visualization import plot_density_graph, plotPowerLaw, plot_modularity_graph


def main(load_dir, save_dir, currencies, heuristic_list, weighted, modularity_file):

    df_mod = pd.read_csv(modularity_file)

    for cur in currencies:

        for wt in weighted:
        
            for heuristic in heuristic_list:

                fig_path = save_dir + cur + '_logs/' + wt + '/' + heuristic + '/figures/'
                pathlib.Path(fig_path).mkdir(parents=True, exist_ok=True)

                title = ' '.join(cur.split('_')).capitalize() + ' ' + heuristic
                load_path = load_dir + cur + '_logs/' + wt + '/' + heuristic + '/generated_files/' + cur + '_' + heuristic
                save_fig_dir = fig_path + cur + '_' + heuristic + '_'

                if wt == 'weighted':
                    comp_filename = load_path + '_wt_components.csv'
                    save_fig_dir = save_fig_dir + 'wt_'
                else: comp_filename = load_path + '_components.csv'

                df_components = pd.read_csv(comp_filename)

                plot_density_graph(df_components['num_of_addrs'], 'Number of addesses', save_fig_dir + 'density_plot.png', cur, heuristic)
                plotPowerLaw(df_components['num_of_addrs'], cur, heuristic, save_fig_dir + 'powerlaw_plot.png')
                plot_modularity_graph(df_components, "num_of_edges", title, save_fig_dir + 'comp_size_edges.png')

                if heuristic == 'h0':
                    modularity = df_mod['modularity'].loc[df_mod['graph'] == cur + '_' + heuristic + '_' + wt].values.item()
                    plot_modularity_graph(df_components, "num_of_communities", title, save_fig_dir + 'comp_size_communities.png')
                    plot_modularity_graph(df_components, "modularity", 'Modularity of ' + title + ' graph: ' + str(round(modularity, 4)), save_fig_dir + 'comp_size_modularity.png')



if __name__ == "__main__":

    # load_dir = '/local/scratch/correspondence_network/part1_final_logs/'
    # save_dir = '/local/scratch/correspondence_network/part1_plots/'
    # modularity_file = '/local/scratch/correspondence_network/part1_plots/modularity_of_all_graphs.csv'

    load_dir = '/Users/nidhiagrawal/Desktop/Assignments/MastersProject/Github/FINAL/part1_final_logs/'
    save_dir = '../logs/plot_results_seperate/'
    modularity_file = '../logs/modularity_of_all_graphs.csv'
    
    currencies = ['feathercoin', 'btc_sample']#, 'iota_14days', 'iota', 'monacoin']
    heuristic_list = ['h0', 'h0_h1']
    weighted = ['weighted', 'unweighted']
    
    main(load_dir, save_dir, currencies, heuristic_list, weighted, modularity_file)

