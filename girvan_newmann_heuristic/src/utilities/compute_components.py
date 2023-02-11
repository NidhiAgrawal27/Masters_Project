from tqdm import tqdm

def compute_components(graph_of_correspondences, comps):
    components = {}
    comp_list = []

    print('\nCompute Components of Graph Progress Bar:')
    for i in tqdm(range(graph_of_correspondences.num_vertices())):
        c = comps[i]
        if c not in components: components[c] = [i]
        else: components[c].append(i)
    print()

    print('Create Components List Progress Bar:')
    for c in tqdm(components):
        comp_list.append({'component' : c, 'num_of_addrs' : len(components[c]), 'address_ids' : components[c]})

    return comp_list
