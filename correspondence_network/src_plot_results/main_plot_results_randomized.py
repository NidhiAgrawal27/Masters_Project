import pandas as pd
import pathlib
from plot_visualization import *
from tqdm import tqdm

def main(load_dir, save_dir, currencies, weighted, modularity_file):

    df_mod = pd.read_csv(modularity_file)

    for cur in tqdm(currencies):

        for wt in weighted:
            
            print('\n\n******************** Processing initiated for:', cur + '_logs/' + wt, '********************')
            print('Load dir: ', load_dir, '\n')

            title_h0 = ' '.join(cur.split('_')).capitalize() + ' h0' + ' ' + wt
            load_path_h0 = load_dir + cur + '_logs/' + wt + '/h0/generated_files/' + cur + '_h0'

            fig_path_h0 = save_dir + cur + '_logs/' + wt + '/h0/figures/'
            pathlib.Path(fig_path_h0).mkdir(parents=True, exist_ok=True)
            fig_path_h0 = fig_path_h0 +  cur
            save_fig_dir_h0 = fig_path_h0 + '_h0_'

            title_h0_h1 = ' '.join(cur.split('_')).capitalize() + ' h0_h1' + ' ' + wt
            # load_path_h0_h1 = load_dir + cur + '_logs/' + wt + '/h0_h1/generated_files/' + cur + '_h0_h1'

            fig_path_h0_h1 = save_dir + cur + '_logs/' + wt + '/h0_h1/figures/'
            pathlib.Path(fig_path_h0_h1).mkdir(parents=True, exist_ok=True)
            save_fig_dir_h0_h1 = fig_path_h0_h1 + cur + '_h0_h1_'

            if wt == 'weighted':
                comp_h0 = load_path_h0 + '_wt_components.csv'
                # comp_h0_h1 = load_path_h0_h1 + '_wt_components.csv'
                save_fig_dir_h0 = save_fig_dir_h0 + 'wt_'
                save_fig_dir_h0_h1 = save_fig_dir_h0_h1 + 'wt_'
                fig_path_h0 = fig_path_h0 + '_wt'
            else: 
                comp_h0 = load_path_h0 + '_components.csv'
                # comp_h0_h1 = load_path_h0_h1 + '_components.csv'

            df_components_h0 = pd.read_csv(comp_h0)
            # df_components_h0_h1 = pd.read_csv(comp_h0_h1)

            modularity = df_mod['modularity'].loc[df_mod['graph'] == cur + '_' + 'h0' + '_' + wt].values.item()

            # plot_density_graph(df_components_h0['component_size'], 'Connected Component Size', save_fig_dir_h0 + 'density_plot.png', title_h0)
            # plot_density_graph(df_components_h0_h1['component_size'], 'Connected Component Size', save_fig_dir_h0_h1 + 'density_plot.png', title_h0_h1)

            plot_modularity_graph(df_components_h0, "num_of_communities", title_h0, save_fig_dir_h0 + 'comp_size_communities.png')
            plot_modularity_graph(df_components_h0, "randomized_modularity", 'Modularity of ' + title_h0 + ' graph: ' + str(round(modularity, 4)), save_fig_dir_h0 + 'comp_size_modularity.png')
            
            # plotPowerLaw_superimpose(df_components_h0['component_size'], df_components_h0_h1['component_size'], cur, 'h0', 'h0_h1', wt, fig_path_h0 + '_powerlaw_plot.png', xmin= None, xmax = None)
            
            # plot_edges_gaussian(df_components_h0['component_size'], df_components_h0['num_of_edges'], title_h0, wt, 'Connected Component Size', 'Number of Edges', save_fig_dir_h0 + 'comp_size_edges.png')
            # plot_edges_gaussian(df_components_h0_h1['component_size'], df_components_h0_h1['num_of_edges'], title_h0_h1, wt, 'Connected Component Size', 'Number of Edges', save_fig_dir_h0_h1 + 'comp_size_edges.png')
            
            print('******************** Processing completed for:', cur + '_logs/' + wt, '********************\n\n')

if __name__ == "__main__":

    # load_dir = '/local/scratch/correspondence_network/part1_final_logs/'
    # save_dir = '/local/scratch/correspondence_network/part1_plots/'
    # modularity_file = '/local/scratch/correspondence_network/part1_final_logs/modularity_of_all_graphs.csv'
    
    load_dir = '/Users/nidhiagrawal/Desktop/Assignments/MastersProject/Github/FINAL/part1_final_logs/'
    save_dir = load_dir
    # save_dir = '../logs/plot_results/'
    modularity_file = load_dir + 'modularity_of_all_graphs.csv'

    # currencies = ['feathercoin', 'btc_2012', 'btc_sample', 'iota_14days', 'iota', 'monacoin', 'cardano_sample']
    currencies = ['iota_randomized']
    weighted = ['weighted', 'unweighted']
    
    main(load_dir, save_dir, currencies, weighted, modularity_file)
