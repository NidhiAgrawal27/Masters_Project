import graph_tool.topology as gtt
import matplotlib.pyplot as plt
import graph_tool.inference as  gti
import graph_tool as gt
from graph_tool import dynamics as gtd
import numpy as np

def compute_components(graph_of_correspondences):
    components = {}
    comp_list = []
    comps, _ = gtt.label_components(graph_of_correspondences)

    for i in range(graph_of_correspondences.num_vertices()):
        c = comps[i]
        if c not in components: components[c] = [i]
        else: components[c].append(i)

    for c in components:
        comp_list.append({'component' : c, 'num_of_addrs' : len(components[c]), 'address_ids' : components[c]})

    return comp_list


def get_majority_voter_state(graph_of_correspondence,number_of_components):
    state = gtd.MajorityVoterState(graph_of_correspondence, q=graph_of_correspondence.num_vertices())

    for i in range(graph_of_correspondence.num_vertices()):
        state.get_state()[i] = i
    ret=1
    while ret>0:
        ret = state.iterate_async(niter=graph_of_correspondence.num_vertices())
    s = state.get_state()
    return s


def get_component_modularity(df_components_series,graph_of_correspondences,graph_vertex_property,graph_edge_property):

    address_ids = df_components_series[2]
    comp_graph = gt.GraphView(graph_of_correspondences, vfilt=lambda v: v in address_ids)
    modularity = gti.modularity(comp_graph,b=graph_vertex_property,weight=graph_edge_property)
 
    if np.isnan(modularity):
        return 0
    return modularity