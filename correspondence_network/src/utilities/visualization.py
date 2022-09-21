import matplotlib.pyplot as plt

# Function to plot bar graph  given a dataframe
def plot_bar_or_line_graph(df, graph_type, anot, xlabel, ylabel, title, colour, log_scale, fig_file_name):
    plt.figure(figsize=(12,5))
    if graph_type == 'bar':
        plot_bar = plt.bar(df.index, df, color=colour)
        if anot == 1: plt.bar_label(plot_bar)
    elif graph_type == 'line':
        plot_bar = plt.plot(df.index, df, color=colour)
    if log_scale == 'y':
        plt.yscale('log')
    elif log_scale == 'x':
        plt.xscale('log')
    elif log_scale == 'xy':
        plt.xscale('log')
        plt.yscale('log')
    plt.ylabel(ylabel, size = 14)
    plt.xlabel(xlabel, size = 14)
    plt.title(title, size = 16)
    plt.savefig(fig_file_name, bbox_inches="tight")
    
    return plt

def prob_dist_plot(data, fig_file_name):
    plt.figure(figsize=(12,5))
    plt.hist(data, density = True)
    # plt.annotate()
    plt.ylim(0,1)
    plt.xlabel('Num of addresses n', size = 14)
    plt.ylabel('Probability a component will have num of addresses n', size = 14)
    plt.title("Distribution", size = 16)
    plt.savefig(fig_file_name+'_hist', bbox_inches="tight")

