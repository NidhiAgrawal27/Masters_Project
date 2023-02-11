import numpy as np

def get_initial_and_fixed(g, sample_known_addr, known_addr_entity_dict, sample_size, seed=32512163):
        known_idxs = [idx for idx, addr in enumerate(g.vs["name"]) if addr in sample_known_addr]
        initial = np.zeros(len(g.vs), dtype=np.int)
        rng = np.random.RandomState(seed)
        sample_known_idxs = rng.choice(known_idxs, size=sample_size, replace=False) # TODO: set seed
        non_sample_idxs = np.setdiff1d(range(len(g.vs)), sample_known_idxs)
        for idx in sample_known_idxs:
                initial[idx] = known_addr_entity_dict[g.vs[idx]["name"]]

        available_labels = np.setdiff1d(range(len(g.vs)), initial[sample_known_idxs])[:len(g.vs) - sample_size]
        initial[non_sample_idxs] = available_labels
        fixed = np.zeros(len(g.vs), dtype=np.int)
        fixed[sample_known_idxs] = 1
        fixed = fixed.astype(bool)
        return initial, fixed
