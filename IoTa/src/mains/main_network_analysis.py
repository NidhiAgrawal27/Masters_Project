from enum import unique
from itertools import count
from operator import index
import argparse
import pathlib
from utilities import utils, network_analysis, visualization
import os
import  networkx as nx

PATHNAMES = utils.pathnames()

def main():
    
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, help="random seed", required=True)
    args = parser.parse_args()

    network_name = nx.read_gml(PATHNAMES['segregated_data_gml'])

    utils.set_seed(args.seed)

    pathlib.Path(PATHNAMES["network_analysis_fig_dir"]).mkdir(parents=True, exist_ok=True)


    ylog = 0
    rotation = 0

    #plotting average neighbor degree
    av_neig_deg = network_analysis.av_neighbors_degree(network_name)
    x_label = "Degree k"
    y_label = "Average Degree Of Neighbour knn(k)"
    title = 'IOTA Average network degree'
    fig9 = visualization.plot_hist_or_scatter(x = av_neig_deg[0],y = av_neig_deg[1],graph_type='scatter',bin = None,ylabel= y_label,xlabel= x_label,title= title,color= 'blue',ylog= ylog, density=None,edgecolor=None,marker = 'o', linestyle = '',rotation= rotation)
    fig9.savefig(os.path.join(PATHNAMES["network_analysis_fig_dir"], 'av_neigh_deg.png'), bbox_inches="tight")


    #assortativity coefficient
    network_analysis.assort_coef(network_name)

    #degree distribution
    degree_list = network_analysis.degree_distribution(network_name)
    x_label = 'Number of transactions (k)'
    y_label = 'Fraction of addresses with degree k'
    title = 'Degree Distribution On IOTA Transaction Network'
    fig10 = visualization.plot_hist_or_scatter(x = degree_list,y = None, graph_type = 'hist',bin = max(degree_list), ylabel = y_label,xlabel = x_label, title = title,color = 'blue', ylog = ylog, density=True,edgecolor='white',rotation= rotation, marker = None, linestyle = None)
    fig10.xlim([0,10])
    fig10.savefig(os.path.join(PATHNAMES["network_analysis_fig_dir"], 'degree_distribution.png'), bbox_inches="tight")

    #closeness centrality /degree centrality
    centralities = network_analysis.deg_closs_cen(network_name)
    x_label = 'Degree Centrality'
    y_label = 'Closeness Centrality'
    title = 'Degree Centrality vs Closeness Centrality'
    fig11 = visualization.plot_hist_or_scatter(x = centralities[0],y = centralities[1],graph_type='scatter',bin = None,ylabel= y_label,xlabel= x_label,title= title,color= 'red',ylog= ylog, density=None,edgecolor=None,marker = 'o', linestyle = '',rotation= rotation)
    fig11.plot([], [], ' ', label="Pearson's correlation {}".format(centralities[2]))    # adding Pearson's correlation coefficient to an empty plot with blank marker containing the extra label
    fig11.plot([], [], ' ', label= "Kendall's correlation {}".format(centralities[3]))   # empty plot for Kendall's correlation coefficient in legend
    fig11.plot([], [], ' ', label= "Spearman's correlation {}".format(centralities[4])) # empty plot for Spearman's correlation coefficient in legend
    fig11.legend()
    fig11.savefig(os.path.join(PATHNAMES["network_analysis_fig_dir"], 'centralities.png'), bbox_inches="tight")
 

    #Community detection

    community_det = network_analysis.communities(network_name)
    title = "Greedy Modularity Communities"
    fig12 = visualization.plot_community_detection(network_name, community_det[0], title)
    fig12.savefig(os.path.join(PATHNAMES["network_analysis_fig_dir"], 'Greedy_mod_comm.png'), bbox_inches="tight")
    print("Number of Greedy Modularity Communities:", community_det[2])

    title = "Label Propagation Communities"
    fig13 = visualization.plot_community_detection(network_name, community_det[1], title)
    fig13.savefig(os.path.join(PATHNAMES["network_analysis_fig_dir"], 'Label_prop_comm.png'), bbox_inches="tight")
    print("Number of Label Propagation Communities:", community_det[3])


if __name__ == "__main__":
    main()    
