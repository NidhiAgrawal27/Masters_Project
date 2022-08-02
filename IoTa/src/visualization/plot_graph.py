import matplotlib.pyplot as plt

# Function to plot bar graph  given a dataframe
def plot_graph(df, graph_type, ylabel, xlabel, title, colour, ylog, rotation):
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
    plt.show()

