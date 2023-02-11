import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.font_manager as fm


uzh_color_map = ['#0028a5', '#dc6027', '#91c34a', '#fede00', '#a3adb7', '#0b82a0', '#2a7f62', # FULL
                 '#667ec9', '#eaa07d', '#bfdf94', '#fcec7c', '#c8ced4', '#6bb7c7', '#80b6a4', # 60%
                 '#3353b7', '#e38052', '#aad470', '#fbe651', '#b5bdc5', '#3c9fb6', '#569d85', # 80%
                 '#99a9db', '#f1bfa9', '#d5e9b7', '#fdf3a8', '#dadee2', '#9ed0d9', '#abcec2', # 40%
                 '#ccd4ed', '#f8dfd4', '#eaf4db', '#fef9d3', '#edeff1', '#cfe8ec', '#d5e7e1'] # 20%

uzh_colors = {'blue': '#0028a5', 'blue_80': '#3353b7', 'blue_60': '#667ec9', 'blue_40': '#99a9db', 'blue_20': '#ccd4ed',
               'red': '#dc6027', 'red_80': '#e38052', 'red_60': '#eaa07d', 'red_40': '#f1bfa9', 'red_20': '#f8dfd4',
               'green': '#91c34a', 'green_80': '#aad470', 'green_60': '#bfdf94', 'green_40': '#d5e9b7', 'green_20': '#eaf4db',
               'yellow': '#fede00', 'yellow_80': '#fbe651', 'yellow_60': '#fcec7c', 'yellow_40': '#fdf3a8', 'yellow_20': '#fef9d3',
               'grey': '#a3adb7', 'grey_80': '#b5bdc5', 'grey_60': '#c8ced4', 'grey_40': '#dadee2', 'grey_20': '#edeff1',
               'turquoise': '#0b82a0', 'turquoise_80': '#3c9fb6', 'turquoise_60': '#6bb7c7', 'turquoise_40': '#9ed0d9', 'turquoise_20': '#cfe8ec',
               'green2': '#2a7f62', 'green2_80': '#569d85', 'green2_60': '#80b6a4', 'green2_40': '#abcec2', 'green2_20': '#d5e7e1'}

font_path = './utilities/Fonts/TheSans Plain.otf'
fm.fontManager.addfont(font_path)
prop = fm.FontProperties(fname=font_path)

plt.rcParams.update({
                        'text.usetex': False,
                        'font.family': 'sans-serif',
                        'font.sans-serif' : prop.get_name(),
                        'axes.labelsize' : 16,
                        'font.size' : 12,
                        'mathtext.fontset': 'cm',
                        'axes.unicode_minus': False,
                        'axes.formatter.use_mathtext': True,
                    })

mpl.rcParams['axes.linewidth'] = 1.2
mpl.rcParams['axes.prop_cycle'] = mpl.cycler(color=uzh_color_map)


def plot_girvan_newmann_metrics(x, y, xlabel, ylabel, title, colour, save_fig_filepath):
    plt.figure(figsize=(5,5))
    plt.plot(x, y, '-ok', color = uzh_colors[colour])
    plt.ylabel(ylabel)
    plt.xlabel(xlabel)
    plt.title(title)
    plt.minorticks_off()
    plt.tight_layout()
    plt.savefig(save_fig_filepath)
    return



def plot_metrics(df_list, title_list, metrics, metric_names, fig_dir):
    title_h0 = title_list[0]
    title_h0_h1 = title_list[1]
    df_h0 = df_list[0]
    df_h0_h1 = df_list[1]
    for i in range(len(metrics)):
        x1 = df_h0['prop_graph']
        y1 = df_h0[metrics[i]]
        x2 = df_h0_h1['prop_graph']
        y2 = df_h0_h1[metrics[i]]
        plt.figure(figsize=(5,5))
        plt.plot(x1, y1, '-ok', label=title_h0, color = uzh_colors['blue']) # plot h0
        plt.plot(x2, y2, '-ok', label=title_h0_h1, color = uzh_colors['red']) # plot h0_h1
        if metric_names[i] == 'Number of Cluster': plt.yscale('log')  
        plt.legend()
        plt.ylabel(metric_names[i])
        plt.xlabel('p')
        plt.title(f"{metric_names[i]} as a function of p")
        plt.minorticks_off()
        plt.tight_layout()
        plt.savefig(fig_dir + metrics[i] + '.png')
    return

