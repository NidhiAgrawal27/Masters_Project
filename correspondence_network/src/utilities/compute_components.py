import graph_tool.topology as gtt
import matplotlib.pyplot as plt
import graph_tool as gt
from graph_tool import dynamics as gtd

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


def get_majority_voter_state(graph_of_correspondence,number_of_components,fig_file_name):
    state = gtd.MajorityVoterState(graph_of_correspondence, q=number_of_components)
    x = [[] for r in range(number_of_components)]
    for t in range(2000):
        ret = state.iterate_async(niter=graph_of_correspondence.num_vertices())
        s = state.get_state().fa
        for r in range(4):
            x[r].append((s == r).sum())

    # plt.figure(figsize=(6, 4))
    # for r in range(4):
    #     plt.plot(x[r], label="Opinion %d" % r)
    #     plt.xlabel(r"Time")
    #     plt.ylabel(r"Number of nodes")
    #     plt.legend(loc="best")
    #     plt.tight_layout()
    #     plt.savefig(fig_file_name)

    return x