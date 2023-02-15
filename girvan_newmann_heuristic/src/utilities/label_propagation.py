import graph_tool as gt
import graph_tool.dynamics as gtd
import graph_tool.generation as gtg
import graph_tool.inference as gti
import graph_tool.topology as gtt

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