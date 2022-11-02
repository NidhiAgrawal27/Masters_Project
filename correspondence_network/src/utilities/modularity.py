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


def compute_modularity(g, components, currency, heuristic, fig_dir, dir_generated_files):
    
    sz_comp_edges = {}   # will not append these values for small communities
    sz_comp_comm = {}
    sz_comp_mod = {}
    
    no_entities = 0
    entities = g.new_vertex_property("int") 

    component_labels = np.unique( components.a )
    
    print('\nModularity Progress Bar:')
    for i_comp in tqdm(component_labels):

        # boolean vector components map
        vec_comp = components.a == i_comp 

        # no. of vertices belonging to the particular component- size of the component        
        sz_comp =  int(np.sum(vec_comp))  

        # giving the unique label for small communities
        if np.sum(vec_comp) < 6:
            for v in np.where(vec_comp)[0]:
                entities[v] = no_entities
            no_entities += 1
        
        else:
            gv= gt.GraphView(g, vfilt = vec_comp)   
            redv = defaultdict(lambda : no_entities+len(redv))
            communities = label_prop(gv, 20)
            for v in gv.vertices():
                entities[v] = redv[communities[v]]
            no_entities += len(redv)
            
            #store number of edges dictionary with component size
            if sz_comp in sz_comp_edges.keys():
                sz_comp_edges[sz_comp].append(gv.num_edges())
            else:
                sz_comp_edges[sz_comp]=[gv.num_edges()]
            
            #store number of communities dictionary with component size
            if sz_comp in sz_comp_comm.keys():
                sz_comp_comm[sz_comp].append(len(set(communities.fa)))
            else:
                sz_comp_comm[sz_comp]=[len(set(communities.fa))]
            
            #calculate modularity for only components having more than one community
            if len(set(communities.fa))>1:
                comp_modularity = gti.modularity(gv,communities)
                
                #store modularity in a dictionary with component size
                if sz_comp in sz_comp_mod.keys():
                    sz_comp_mod[sz_comp].append(comp_modularity)
                else:
                    sz_comp_mod[sz_comp]=[comp_modularity]
    print()

    modularity = gti.modularity(g,entities)

    sz_comp_edges = [[key,np.mean(value)] for key,value in sz_comp_edges.items()]
    sz_comp_comm = [[key,np.mean(value)] for key,value in sz_comp_comm.items()]
    sz_comp_mod = [[key,np.mean(value)] for key,value in sz_comp_mod.items()]

    df_sz_comp_edges = pd.DataFrame(sz_comp_edges,columns=["Component_Size","Number of edges"])
    df_sz_comp_comm = pd.DataFrame(sz_comp_comm,columns=["Component_Size","Number of communities"])
    df_sz_comp_mod = pd.DataFrame(sz_comp_mod,columns=["Component_Size","Modularity"])

    df_sz_comp_edges.to_csv(dir_generated_files + 'sz_comp_edges.csv', index = False)
    df_sz_comp_comm.to_csv(dir_generated_files + 'sz_comp_comm.csv', index = False)
    df_sz_comp_mod.to_csv(dir_generated_files + 'sz_comp_mod.csv', index = False)
    print(currency + ' ' + heuristic + ': writing modularity dictionaries completed')

    #plotting the graphs
    title = currency.capitalize() + ' ' + heuristic
    plot_modularity_graph(df_sz_comp_edges, "Number of edges" , title, fig_dir + 'modularity_edges.png')
    plot_modularity_graph(df_sz_comp_comm, "Number of communities", title, fig_dir + 'modularity_communities.png')
    plot_modularity_graph(df_sz_comp_mod, "Modularity", 'Modularity of ' + title + ' graph: ' + str(round(modularity, 4)), fig_dir + 'modularity.png')
    print(currency + ' ' + heuristic + ': modularity plots completed')

    return
