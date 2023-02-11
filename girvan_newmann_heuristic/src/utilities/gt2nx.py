import networkx as nx

def gt2nx(g0, vertex_property):
    g = nx.Graph()
    for i,j in g0.edges():
        if not vertex_property[i] in g.nodes():
            g.add_node(vertex_property[i])
        if not vertex_property[j] in g.nodes():
            g.add_node(vertex_property[j])
        g.add_edge(vertex_property[i],vertex_property[j])
    return g

# def gt2nx(g0):
#     g = nx.Graph()
#     for i,j in g0.edges():
#         g.add_edge(i,j)
#     return g
