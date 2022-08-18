import matplotlib.pyplot as plt
import networkx.algorithms.community as nxcom
import seaborn as sns
import networkx as nx

# Function to plot bar graph  given a dataframe
def plot_bar_or_line_graph(df, graph_type, ylabel, xlabel, title, colour, ylog, rotation):
    plt.figure(figsize=(12,5))
    if graph_type == 'bar':
        plot_bar = plt.bar(df.index, df, color=colour)
        plt.bar_label(plot_bar)
    elif graph_type == 'line':
        plot_bar = plt.plot(df.index, df, color=colour)
    if ylog == 1:
        plt.yscale('log')
    plt.ylabel(ylabel, size = 14)
    plt.xlabel(xlabel, size = 14)
    plt.xticks(df.index, rotation = rotation)
    plt.title(title, size = 16)
    
    return plt

# function for plotting community detection 
def plot_community_detection(network_name, community, title):
    
    colour = sns.color_palette("flare", len(community))   
    i = 0
    for comm in community:                              # Loop to assign a colour to nodes of each community
        for node in network_name.nodes():
            if node in list(comm):                         # Check if node is in community
                network_name.nodes[node]['color'] = colour[i]  # Assign colour to each node of community
        i += 1                                          # Getting another colour for next community
    
    
    plt.figure(figsize=(7,7))                         # Increasing plot size
    nx.draw(network_name, with_labels=False, node_color = [network_name.nodes[node]['color'] for node in network_name.nodes()])
    plt.title(title, fontsize=15)  

    return plt     

# Function to plot scatter plot and  histogram
def plot_hist_or_scatter(x,y, graph_type, bin, ylabel, xlabel, title, color, ylog, density, edgecolor, marker,linestyle, rotation):
    plt.figure(figsize=(12,5))
    if graph_type == 'hist':
        plot_hist = plt.hist(x, bins = bin, color=color, density = density, edgecolor = edgecolor)
    elif graph_type == 'scatter':
        plot_bar = plt.plot(x,y, color=color, marker = marker, linestyle = linestyle)
    if ylog == 1:
        plt.yscale('log')
    plt.ylabel(ylabel, size = 14)
    plt.xlabel(xlabel, size = 14)
    plt.title(title, size = 16)
    return plt
