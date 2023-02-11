import networkx as nx
import graph_tool.all as gt

def nx2gt(g0):
    mp = dict()
    g = nx.Graph()
    for i,j in g0.edges():
        if i not in mp:
            mp[i] = len(mp)
        if j not in mp:
            mp[j] = len(mp)
        g.add_edge(mp[i],mp[j])
    ggt = gt.Graph()
    vertex_property = ggt.new_vertex_property("object")
    mpi = {value:key for key,value in mp.items()}
    for i,j in g.edges():
        ggt.add_edge(i,j,add_missing = True)
    for i in ggt.vertices():
        vertex_property[i] = mpi[i]
    return ggt, vertex_property
