import graph_tool as gt
import graph_tool.dynamics as gtd
import graph_tool.inference as gti
import graph_tool.topology as gtt
from graph_tool import draw
import numpy as np
import pandas as pd
from collections import defaultdict
from tqdm import tqdm
from utilities.visualization import plot_modularity_graph


def label_prop(gin, max_iter = 100, each_update = None):
           
    no_nodes = gin.num_vertices()
    if each_update is None:
        each_update = gin.num_edges()
    
    lp = gtd.MajorityVoterState(gin, q=no_nodes+1 )
    for _ in range(no_nodes):
        lp.get_state().fa[_] = _+1
    
    converged = False
    i_iter = 0    

    while not converged and i_iter < max_iter:
        ret = lp.iterate_async(each_update)
        converged = (ret == 0)
        i_iter += 1
        
    return lp.get_state()


def compute_modularity(g, components, heuristic):
    
    comp_size = []
    sz_comp_edges = []
    sz_comp_comm = []
    sz_comp_mod = []
    
    no_entities = 0
    entities = g.new_vertex_property("int") 

    component_labels = np.unique( components.a )
    
    print('\nModularity Progress Bar:')
    for i_comp in tqdm(component_labels):

        # boolean vector components map
        vec_comp = components.a == i_comp 

        # no. of vertices belonging to the particular component- size of the component        
        sz_comp =  int(np.sum(vec_comp))
        comp_size.append(sz_comp)

        if heuristic == "h0_h1":
            sz_comp_edges.append(gt.GraphView(g, vfilt = vec_comp).num_edges())
            continue
        
        # giving the unique label for small communities
        if np.sum(vec_comp) < 6 and heuristic=="h0":
            for v in np.where(vec_comp)[0]:
                entities[v] = no_entities
            no_entities += 1

            sz_comp_edges.append(gt.GraphView(g, vfilt = vec_comp).num_edges())
            sz_comp_comm.append(1)
            sz_comp_mod.append(0)

        else:
            gv= gt.GraphView(g, vfilt = vec_comp)    
            redv = defaultdict(lambda : no_entities+len(redv))
            communities = label_prop(gv, 20)
            for v in gv.vertices():
                entities[v] = redv[communities[v]]
            no_entities += len(redv)
            
            #store number of edges dictionary with component size
            sz_comp_edges.append(gv.num_edges())
            
            #store number of communities dictionary with component size
            sz_comp_comm.append(len(set(communities.fa)))
            
            #calculate modularity for only components having more than one community
            if len(set(communities.fa))>1:
                comp_modularity = gti.modularity(gv,communities)
                
                #store modularity in a dictionary with component size
                sz_comp_mod.append(comp_modularity)

            else: sz_comp_mod.append(0)

    #returns empty communities, modularity and entities for h0_h1 heuristic
    return comp_size, sz_comp_edges, sz_comp_comm, sz_comp_mod, entities
