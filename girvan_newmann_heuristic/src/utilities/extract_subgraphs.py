import networkx as nx
from tqdm import tqdm

def extract_subgraphs(G, df): #gives the component subgraphs of the original graph that have more than one entity
    subgraphs = []
    components = list(nx.connected_components(G))
    print('Extracting subgraphs...')
    for component in tqdm(components):
        entities = set(df[df['address'].isin(component)]['entity'].tolist())
        if len(entities) > 1:
            subgraph = G.subgraph(component)
            entity_count = len(entities)
            subgraphs.append((subgraph, entity_count))
    return subgraphs

