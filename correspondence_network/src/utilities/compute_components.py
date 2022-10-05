import graph_tool.topology as gtt

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