import numpy as np
from ast import literal_eval



def add_correspondence(row, graph_of_correspondences, ip_addrs_idx, op_addrs_idx, ip_amt_idx, 
                        op_amt_idx, nodes_dict, vertex_property, edge_property, heuristic):

    # h0: all input addresses of a tx belong to same user
    nodes_list = literal_eval(row[ip_addrs_idx])

    # h1: get change address
    h1 = 0

    if heuristic == 'h0+h1':
        ip_amt = literal_eval(row[ip_amt_idx])
        op_amt = literal_eval(row[op_amt_idx])
        op_addrs = literal_eval(row[op_addrs_idx])

        # apply h1 only if op addresses are different from ip addreses
        if len(set(nodes_list) & set(op_addrs)) == 0: 
            if min(op_amt) < min(ip_amt): 
                idx = np.argmin(op_amt)
                change_addrs = op_addrs[idx]
                nodes_list.append(change_addrs)
                h1 = 1

    nodes_list = list(set(nodes_list))

    if len(nodes_list) <= 1: return

    # create nodes
    for node in nodes_list :
        if node in nodes_dict: continue
        vertex = graph_of_correspondences.add_vertex()
        idx = graph_of_correspondences.vertex_index[vertex]
        nodes_dict[node] = idx
        vertex_property[vertex] = node

    # create edges for fully connected clusters in network
    for i in range(len(nodes_list)-1):
        v0 = nodes_dict[nodes_list.pop(0)]

        for j in range(len(nodes_list)):
            v1 = nodes_dict[nodes_list[j]]

            if heuristic == 'h0':
                if not graph_of_correspondences.edge(v0,v1):
                    e = graph_of_correspondences.add_edge(v0,v1)
                    edge_property[e] = {
                                        'node1': v0, 
                                        'node2': v1, 
                                        'h0': 1,
                                        'count_of_same_edge_h0': 1
                                        }
                else: 
                    e = graph_of_correspondences.edge(v0,v1)
                    edge_property[e]['count_of_same_edge_h0'] += 1
            
            elif heuristic == 'h0+h1':
                if not graph_of_correspondences.edge(v0,v1):
                    e = graph_of_correspondences.add_edge(v0,v1)
                    edge_property[e] = {
                                        'node1': v0, 
                                        'node2': v1, 
                                        'h0': 1, 
                                        'h1': h1, 
                                        'count_of_same_edge_h0': 1, 
                                        'count_of_same_edge_h0_h1': h1
                                        }
                else: 
                    e = graph_of_correspondences.edge(v0,v1)
                    edge_property[e]['count_of_same_edge_h0'] += 1
                    edge_property[e]['count_of_same_edge_h0_h1'] += h1

    return nodes_dict
    

def add_correspondence_directed(row, graph_of_correspondences, ip_addrs_idx, op_addrs_idx, ip_amt_idx, 
                        op_amt_idx, nodes_dict, vertex_property, edge_property, heuristic):

    # h0: all input addresses of a tx belong to same user
    nodes_list = literal_eval(row[ip_addrs_idx])

    # h1: get change address
    h1 = 0

    if heuristic == 'h0+h1':
        ip_amt = literal_eval(row[ip_amt_idx])
        op_amt = literal_eval(row[op_amt_idx])
        op_addrs = literal_eval(row[op_addrs_idx])

        # apply h1 only if op addresses are different from ip addreses
        if len(set(nodes_list) & set(op_addrs)) == 0: 
            if min(op_amt) < min(ip_amt): 
                idx = np.argmin(op_amt)
                change_addrs = op_addrs[idx]
                nodes_list.append(change_addrs)
                h1 = 1

    nodes_list = list(set(nodes_list))

    if len(nodes_list) <= 1: return

    # create nodes
    for node in nodes_list :
        if node in nodes_dict: continue
        vertex = graph_of_correspondences.add_vertex()
        idx = graph_of_correspondences.vertex_index[vertex]
        nodes_dict[node] = idx
        vertex_property[vertex] = node

    # create edges for fully connected clusters in network
    for i in range(len(nodes_list)-1):
        v0 = nodes_dict[nodes_list.pop(0)]

        for j in range(len(nodes_list)):
            v1 = nodes_dict[nodes_list[j]]

            e1 = graph_of_correspondences.add_edge(v0,v1)
            e2 = graph_of_correspondences.add_edge(v1,v0)               

    return nodes_dict