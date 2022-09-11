import numpy as np
from ast import literal_eval
import graph_tool as gt
from graph_tool.all import graph_draw
import graph_tool.topology as gtt


def add_correspondence(row, graph_of_correspondences, ip_addrs_idx, op_addrs_idx, ip_amt_idx, 
                        op_amt_idx, nodes_dict, vertex_property, edge_property):

    # converts string to list form
    nodes_list = literal_eval(row[ip_addrs_idx])
    ip_amt = literal_eval(row[ip_amt_idx])
    op_amt = literal_eval(row[op_amt_idx])
    op_addrs = literal_eval(row[op_addrs_idx])
    h1 = 0
    
    # h1 - get change address
    if min(op_amt) < min(ip_amt): 
        idx = np.argmin(op_amt)
        change_addrs = op_addrs[idx]
        nodes_list.append(change_addrs)
        h1 = 1

    nodes_list = set(nodes_list)

    if len(nodes_list) <= 1: return

    for node in nodes_list :
        if node in nodes_dict: continue
        vertex = graph_of_correspondences.add_vertex()
        idx = graph_of_correspondences.vertex_index[vertex]
        nodes_dict[node] = idx
        vertex_property[vertex] = node

    v0 = nodes_dict[nodes_list.pop()]

    for node in nodes_list:
        v1 = nodes_dict[node]
        if not graph_of_correspondences.edge(v0,v1):
            e = graph_of_correspondences.add_edge(v0,v1)
            edge_property[e] = {'node1': v0, 'node2': v1, "h0": 1, "h1": h1, "count_of_same_edge": 1}
        else: 
            e = graph_of_correspondences.edge(v0,v1)
            edge_property[e]['count_of_same_edge'] += 1  
    return
    

def compute_components(graph_of_correspondences):
    components = {}
    comp_list = []
    comps, _ = gtt.label_components(graph_of_correspondences)

    for i in range(graph_of_correspondences.num_vertices()):
        c = comps[i]
        if c not in components: components[c] = [i]
        else: components[c].append(i)

    for c in components:
        comp_list.append({'component' : c, 'address_ids' : components[c]})

    return comp_list

