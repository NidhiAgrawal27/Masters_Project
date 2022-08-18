import networkx as nx
import numpy as np
import scipy.stats as sp
import networkx.algorithms.community as nxcom



def av_neighbors_degree(network_name):
    av_neigh_degree = nx.k_nearest_neighbors(network_name) #getting a dictionary keyed by degree k with the value of average neighbor degree on a real network
    deg_list = av_neigh_degree.keys() #list of degrees
    list_av_neigh_degree = av_neigh_degree.values()    #list of average neighbour degrees
    
    return deg_list, list_av_neigh_degree

def assort_coef(network_name):
    assortativity = nx.degree_assortativity_coefficient(network_name) #getting assortativity coeficient on a real network    
    
    return print('Assortativity Coefficient:', assortativity)

#degree distribution on real network
def degree_distribution(network_name):
    deg = network_name.degree() #getting degrees
    deg_list = [val for (node, val) in deg] #adding degrees to a listv
    
    return deg_list

#degree centrality / closeness centrality
def deg_closs_cen(network_name):
    
    degree_cen = nx.degree_centrality(network_name)        # computing degree centrality for each node
    degree_centrality = [list for key, list in degree_cen.items()]
    
    close_cen = nx.closeness_centrality(network_name)      # computing closeness centrality for each node
    closeness_centrality = [list for key, list in close_cen.items()]            
    
    pearson = round(sp.pearsonr(degree_centrality,closeness_centrality)[0],3)     # computing Pearson's correlation coefficient 
    kendall = round(sp.kendalltau(degree_centrality,closeness_centrality)[0],3)   # computing Kendall's correlation coefficient
    spearman = round(sp.spearmanr(degree_centrality,closeness_centrality)[0],3)   # computing Pearson's correlation coefficient
    
    return  degree_centrality, closeness_centrality, pearson,kendall, spearman

#computing communities
def communities(network_name):    
    
    # Computing Greedy Modularity Communities
    GreedComm = nxcom.greedy_modularity_communities(network_name)               
    
    gr_real = len(GreedComm)               # Number of Greedy Modularity Communities 
    
    # Computing Label Propagation Communities
    LabelComm = [c for c in nxcom.label_propagation_communities(network_name)] 
    
    la_real = len(LabelComm)               # Number of Label Propagation Communities 

    return GreedComm, LabelComm, gr_real,la_real  