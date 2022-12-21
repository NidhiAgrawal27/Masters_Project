import pandas as pd
from ast import literal_eval
from tqdm import tqdm
import pathlib
tqdm.pandas()


def get_num_edges(arg, df_edge_data):
    idx = df_edge_data.index[(df_edge_data['node1'].isin(arg.address_ids) & df_edge_data['node2'].isin(arg.address_ids))].tolist()
    num_of_edges = len(idx)
    df_edge_data.drop(idx, inplace=True)
    arg.num_of_edges_from_logs = num_of_edges
    return arg

def main(load_dir, save_dir, currencies, weighted, heuristics):
    for cur in tqdm(currencies):
        for wt in weighted:
            for heuristic in heuristics:
                generated_files_dir = load_dir + cur + '_logs/' + wt + '/' + heuristic + '/generated_files/'
                if wt == 'weighted':
                    comp_file = generated_files_dir + cur + '_' + heuristic + '_wt_components.csv'
                    edge_data_file = generated_files_dir + cur + '_' + heuristic + '_wt_edge_data.csv'
                else:
                    comp_file = generated_files_dir + cur + '_' + heuristic + '_components.csv'
                    edge_data_file = generated_files_dir + cur + '_' + heuristic + '_edge_data.csv'
                save_file = save_dir + comp_file
                pathlib.Path(save_dir+generated_files_dir).mkdir(parents=True, exist_ok=True)
                df_comp = pd.read_csv(comp_file)
                df_edge_data = pd.read_csv(edge_data_file)

                print('df_comp.shape: ', df_comp.shape)
                print('df_edge_data.shape: ', df_edge_data.shape)

                df_comp['address_ids'] = df_comp['address_ids'].apply(literal_eval)
                df_comp['num_of_edges_from_logs']=0
                df_comp = df_comp.progress_apply(get_num_edges, df_edge_data=df_edge_data, axis = 1)
                df_comp.to_csv(save_file)



if __name__ == "__main__":

    # load_dir = '/local/scratch/correspondence_network/part1_final_logs/'
    # save_dir = '/local/scratch/correspondence_network/part1_plots/'
    
    load_dir = '/Users/nidhiagrawal/Desktop/Assignments/MastersProject/Github/FINAL/part1_final_logs/'
    # save_dir = load_dir
    save_dir = '../logs/num_edges/'

    # currencies = ['feathercoin', 'btc_sample', 'iota_14days', 'iota', 'monacoin', 'cardano_sample']
    currencies = ['cardano_sample']
    weighted = ['weighted', 'unweighted']
    heuristics = ['h0', 'h0_h1']
    
    main(load_dir, save_dir, currencies, weighted, heuristics)

