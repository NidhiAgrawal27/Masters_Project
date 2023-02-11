import networkx as nx
import pandas as pd

def get_address_labels(nx_graph, local_ground_truth_data):
    entity = {}
    nx.set_node_attributes(nx_graph, entity, "entity")
    for comp in nx.connected_component_subgraph(nx_graph):
        list_of_addrs = pd.DataFrame([vertex for vertex in comp.nodes()], columns = ["address"])
        num_entities = list(pd.merge(list_of_addrs,local_ground_truth_data,left_on="address",right_on="address")['entity'])
        if len(set(num_entities)) == 1:
            for nodename in comp.nodes():
                entity[nodename] = num_entities[0]
        else:
            for nodename in comp.nodes():
                entity[nodename] = "Unknown"
                # # one solution
                # max_entity = num_entities.value_counts().index.tolist()[0]
                # entity[nodename] = max_entity
    
    return entity