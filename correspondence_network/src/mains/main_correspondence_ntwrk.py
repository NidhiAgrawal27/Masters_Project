import pandas as pd
import argparse
import pathlib
import os
import pickle
import graph_tool.all as gt
from graph_tool import inference as gti
import graph_tool.topology as gtt
from graph_tool import draw
from utilities import set_seed, compute_components, pathnames, correspondence_network
from utilities.modularity import compute_modularity
from utilities.modularity_multiprocess import Modularity
from utilities.visualization import plotPowerLaw, plot_density_graph, plot_modularity_graph, plot_edges_gaussian

import warnings
warnings.filterwarnings('ignore')

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, help="random seed", required=True)
    parser.add_argument("--currency", type=str, help="currency name example - btc: Bitcoin, iota: IoTa", required=True)
    parser.add_argument("--heuristic", type=str, help="name of heuristic, example: h0, or h0_h1", required=True)
    parser.add_argument("--vis", type=str, help="visualization: yes or no", required=True)
    parser.add_argument("--data_is_split", type=str, help="Data is read in chunks: yes or no", required=True)
    parser.add_argument("--save_graph", type=str, help="Save graph: yes or no", required=True)
    parser.add_argument("--load_graph", type=str, help="Load saved graph: yes or no", required=True)
    parser.add_argument("--weighted", type=str, help="Weighted graph: yes or no", required=True)
    parser.add_argument("--chunksize", type=int, help="Chunk of data to be read in one iteration", required=False)

    args = parser.parse_args()

    set_seed.set_seed(args.seed)
    cur = args.currency
    heuristic = args.heuristic
    vis = args.vis
    chunksize = args.chunksize
    data_is_split = args.data_is_split
    save_graph = args.save_graph
    load_graph = args.load_graph
    weighted = args.weighted

    PATHNAMES = pathnames.pathnames(cur, heuristic, weighted)
    pathlib.Path(PATHNAMES['generated_files']).mkdir(parents=True, exist_ok=True)
    pathlib.Path(PATHNAMES['figure_dir']).mkdir(parents=True, exist_ok=True)
    dir_generated_files = PATHNAMES['generated_files'] + cur + '_' + heuristic + '_'
    fig_dir = PATHNAMES['figure_dir'] + cur + '_' + heuristic + '_'
    modularity_file = PATHNAMES['logs_home_dir'] + 'modularity_of_all_graphs.csv'
    load_graph_dir = PATHNAMES['load_graph_dir']
    load_graph_path = load_graph_dir + cur + '_' + heuristic + '_'
    save_graph_dir = PATHNAMES['generated_files'] + 'graph/'
    pathlib.Path(save_graph_dir).mkdir(parents=True, exist_ok=True)
    save_graph_path = save_graph_dir + cur + '_' + heuristic + '_'
    wt = 'unweighted'
    if weighted == 'yes':
        dir_generated_files = dir_generated_files + 'wt_'
        fig_dir = fig_dir + 'wt_'
        load_graph_path = load_graph_path + 'wt_'
        save_graph_path = save_graph_path + 'wt_'
        wt = 'weighted'
    

    graph_of_correspondences = gt.Graph( directed=False )
    vertex_property = graph_of_correspondences.new_vertex_property("string")
    edge_property = graph_of_correspondences.new_edge_property("object")
    nodes_dict = {}
    vertices_mapping = []
    edge_mapping = []
    df_tx_ids = pd.DataFrame()
    df_address_ids = pd.DataFrame()
    df_edge_data = pd.DataFrame()
    df_components = pd.DataFrame()
    iter = 0

    print('\n\n*********************** Processing of ' + cur + ' ' + heuristic + ' ' + wt + ' initiated ***********************\n')


    if load_graph == 'no':
        
        print()
        if data_is_split == 'no':
            if cur=='feathercoin' or cur=='monacoin':
                df = pd.read_csv(PATHNAMES['data_path'], header=None)
                df.columns=['transaction_id','block_index','input_addresses_x','input_amounts_x',
                                'output_addresses_y','output_amounts_y','timestamp']
            # elif cur == 'btc_2012':
            #     df = pd.read_csv(PATHNAMES['data_path'], nrows=15000000)
            #     df_timestamp = pd.DataFrame(df['timestamp'].between(1310000000, 1360000000))
            #     idx = df_timestamp.index[df_timestamp['timestamp'] == True].tolist()
            #     df = df.iloc[idx]
            elif cur == 'cardano_sample':
                df = pd.read_csv(PATHNAMES['data_path'], nrows=20000000)
            else: df = pd.read_csv(PATHNAMES['data_path'])

            print('Create Correspondence Network Progress Bar:')
            graph_of_correspondences, vertex_property, edge_property, nodes_dict, df_tx_ids, iter = correspondence_network.correspondence_network(df, graph_of_correspondences, vertex_property, edge_property, nodes_dict, df_tx_ids, cur, heuristic, iter, weighted)


        elif data_is_split == 'yes':
            import ray
            import modin.pandas as mpd
            ray.init()
            if cur == 'feathercoin' or cur == 'monacoin':
                chunks_df = mpd.read_csv(PATHNAMES['data_path'], chunksize=chunksize,header=None)
                chunks_df.columns=['transaction_id','block_index','input_addresses_x','input_amounts_x',
                                        'output_addresses_y','output_amounts_y','timestamp']
            else: chunks_df = mpd.read_csv(PATHNAMES['data_path'], chunksize=chunksize)
            iter = 0
            for df in chunks_df:
                df = df._to_pandas()
                graph_of_correspondences, vertex_property, edge_property, nodes_dict, df_tx_ids, iter = correspondence_network.correspondence_network(df, graph_of_correspondences, vertex_property, edge_property, nodes_dict, df_tx_ids, cur, heuristic, iter, weighted)


        # start of no_modin_split
        elif data_is_split == 'no_modin_split':
            if cur == 'feathercoin' or cur == 'monacoin':
                chunks_df = pd.read_csv(PATHNAMES['data_path'], chunksize=chunksize,header=None)
                chunks_df.columns=['transaction_id','block_index','input_addresses_x','input_amounts_x',
                                        'output_addresses_y','output_amounts_y','timestamp']
            else: chunks_df = pd.read_csv(PATHNAMES['data_path'], chunksize=chunksize)            
            for i, df in enumerate(chunks_df):
                    graph_of_correspondences, vertex_property, edge_property, nodes_dict, df_tx_ids, iter = correspondence_network.correspondence_network(df, graph_of_correspondences, vertex_property, edge_property, nodes_dict, df_tx_ids, cur, heuristic, iter, weighted)
        # end of no_modin split

        print('\n\n' + wt + ' ' + cur + ' ' + heuristic + ': correspondence network created')

        # write csv file for transaction_ids
        df_tx_ids.to_csv(dir_generated_files + 'transaction_ids.csv', index=False)
        print(wt + ' ' + cur + ' ' + heuristic + ': writing transaction_ids.csv completed')

        # save graph_of_correspondences, address data and edge data
        if save_graph == 'yes':
            print(wt + ' ' + cur + ' ' + heuristic + ': saving graph and properties...')
            graph_of_correspondences.save(save_graph_path + 'graph.xml.gz')
            with open(save_graph_path + 'vertex_prop.pickle', 'wb') as handle:
                pickle.dump(vertex_property, handle, protocol=pickle.HIGHEST_PROTOCOL)
            with open(save_graph_path + 'edge_prop.pickle', 'wb') as handle:
                pickle.dump(edge_property, handle, protocol=pickle.HIGHEST_PROTOCOL)
            print(wt + ' ' + cur + ' ' + heuristic + ': graph and properties saved')

             # map vertext and edge properties and write csv files for address_id
            for i in range(graph_of_correspondences.num_vertices()):
                vertices_mapping.append({'address' : vertex_property[i], 'address_id' : i})
            df_address_ids = pd.DataFrame.from_dict(vertices_mapping, orient='columns')
            df_address_ids.to_csv(dir_generated_files + 'address_ids.csv', index=False)
            print(wt + ' ' + cur + ' ' + heuristic + ': writing address_ids.csv completed')

            # map vertext and edge properties and write csv files for edge data
            for e in graph_of_correspondences.edges(): 
                edge_mapping.append(edge_property[e])
            df_edge_data = pd.DataFrame.from_dict(edge_mapping, orient='columns')
            df_edge_data.to_csv(dir_generated_files + 'edge_data.csv', index=False)
            print(wt + ' ' + cur + ' ' + heuristic + ': writing edge_data.csv completed')
            

    # load graph
    else:
        try:
            print('\n\nLoading graph: ' + load_graph_path + 'graph.xml.gz\n')
            print(wt + ' ' + cur + ' ' + heuristic + ': loading graph and properties...')
            graph_of_correspondences = gt.load_graph(load_graph_path + 'graph.xml.gz')
            with open(load_graph_path + 'vertex_prop.pickle', 'rb') as handle:
                vertex_property = pickle.load(handle)
            with open(load_graph_path + 'edge_prop.pickle', 'rb') as handle:
                edge_property = pickle.load(handle)
            print(wt + ' ' + cur + ' ' + heuristic + ': graph and properties loaded')
        except:
            print('ERROR: Load Graph failed. Graph or vertex_prop.pickle or edge_prop.pickle not found on given path.')
            return

    # compute components    
    components, _ = gtt.label_components(graph_of_correspondences)
    components_list = compute_components.compute_components(graph_of_correspondences, components)
    df_components = pd.DataFrame.from_dict(components_list, orient='columns')

    #title of the plots
    title = ' '.join(cur.split('_')).capitalize() + ' ' + heuristic

    # visualization: density graph
    plot_density_graph(df_components['num_of_addrs'], 'Connected Component Size', fig_dir + 'density_plot.png', title)
    print(wt + ' ' + cur + ' ' + heuristic + ': density_plot.png completed\n')

    # visualization: power law plot
    plotPowerLaw(df_components['num_of_addrs'], cur, heuristic, fig_dir + 'powerlaw_plot.png')
    print('\n'+ wt + ' ' + cur + ' ' + heuristic + ': powerlaw_plot.png completed')

    # compute modularity, num of edges and num of communities in the components- w/o multiprocess   
    # comp_size, sz_comp_edges, sz_comp_comm, sz_comp_mod, entities = compute_modularity(graph_of_correspondences, components, heuristic)
    
    # compute modularity, num of edges and num of communities in the components- with multiprocess
    comp_size, sz_comp_edges, sz_comp_comm, sz_comp_mod, entities = Modularity().compute_modularity(graph_of_correspondences,components, heuristic)
    
    df_components["component_size"] = comp_size
    df_components["num_of_edges"] = sz_comp_edges

    if heuristic=="h0":
        df_components["num_of_communities"] = sz_comp_comm
        df_components["modularity"] = sz_comp_mod
        #save entities as a vertex property
        with open(save_graph_path + 'graph_vp_lp_entities.pickle', 'wb') as handle:
                pickle.dump(entities, handle, protocol=pickle.HIGHEST_PROTOCOL)
        #modularity of whole graph
        modularity = gti.modularity(graph_of_correspondences,entities)

        # save modularity value in a file
        if os.path.isfile(modularity_file): 
            df_mod = pd.read_csv(modularity_file)
            if cur + '_' + heuristic + '_' + wt in df_mod['graph'].values:
                df_mod['modularity'].loc[df_mod['graph'] == cur + '_' + heuristic + '_' + wt] = modularity
            else:
                df_mod = df_mod.append({'graph' : cur + '_' + heuristic + '_' + wt, 'modularity' : modularity}, ignore_index=True)
        else: 
            df_mod = pd.DataFrame(columns =['graph' , 'modularity'])
            df_mod = df_mod.append({'graph' : cur + '_' + heuristic + '_' + wt, 'modularity' : modularity}, ignore_index=True)
        df_mod.to_csv(modularity_file, index = False)

    # map vertext and edge properties and write csv files for components data
    df_components.to_csv(dir_generated_files + 'components.csv', index=False)
    print(wt + ' ' + cur + ' ' + heuristic + ': writing components.csv completed')


    #visualisation: Component size vs Edges
    plot_edges_gaussian(df_components['num_of_addrs'], df_components['num_of_edges'], title, wt, 'Connected Component Size', 'Number of Edges', fig_dir + 'comp_size_edges.png')
    print(wt + ' ' + cur + ' ' + heuristic + ': comp_size_edges.png completed\n')

    if heuristic=="h0":
        #visualisation: Component size vs Number of communities
        plot_modularity_graph(df_components, "num_of_communities", title, fig_dir + 'comp_size_communities.png')
        print(wt + ' ' + cur + ' ' + heuristic + ': comp_size_communities.png completed\n')

        #visualisation: Component size vs Modularity
        plot_modularity_graph(df_components, "modularity", 'Modularity of ' + title + ' graph: ' + str(round(modularity, 4)), fig_dir + 'comp_size_modularity.png')
        print(wt + ' ' + cur + ' ' + heuristic + ': comp_size_modularity.png completed\n')

    # visualize network
    if vis == 'yes':
        print(wt + ' ' + cur + ' ' + heuristic + ': saving graph_draw visualization...')
        draw.graph_draw(graph_of_correspondences, vertex_text=graph_of_correspondences.vertex_index, 
                        output = fig_dir + 'correspondence_network' + '.pdf')
        print(wt + ' ' + cur + ' ' + heuristic + ': network figure completed')
        

    print('\n\n*********************** Processing of ' + cur + ' ' + heuristic + ' ' + wt + ' completed ***********************\n')

    print()

if __name__ == "__main__":
    main()


