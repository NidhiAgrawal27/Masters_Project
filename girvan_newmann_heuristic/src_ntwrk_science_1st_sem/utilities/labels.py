def get_labels(cs_addr, known_addr_entity_dict, sample_known_addr):
        res = {}
        for idx, c in enumerate(cs_addr):
                for a in c:
                        if a in sample_known_addr:
                                res[a] = idx
        labels_true = []
        labels_pred = []
        for a in res.keys():
                labels_true.append(known_addr_entity_dict[a])
                labels_pred.append(res[a])
        return labels_true, labels_pred
