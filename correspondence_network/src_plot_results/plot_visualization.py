import matplotlib.pyplot as plt
import powerlaw as pl
import numpy as np
import matplotlib as mpl
import matplotlib.font_manager as fm
from matplotlib import ticker as ticker
from matplotlib.ticker import MultipleLocator
from scipy.stats import gaussian_kde


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


font_path = '../src/utilities/Fonts/TheSans Plain.otf'
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
                    })

mpl.rcParams['axes.linewidth'] = 1.2
mpl.rcParams['axes.prop_cycle'] = mpl.cycler(color=uzh_color_map)



def plotPowerLaw_superimpose(df1, df2, cur, heuristic1, heuristic2, wt, fig_file_name, xmin= None, xmax = None):
    plt.figure(figsize=(8,8))
    fit1 = pl.Fit(df1 , xmin, xmax = xmax)
    fit2 = pl.Fit(df2 , xmin, xmax = xmax)
    alpha1 = fit1.power_law.alpha
    alpha1 = str(round(alpha1,2))
    xmin1 = fit1.power_law.xmin
    alpha2 = fit2.power_law.alpha
    alpha2 = str(round(alpha2,2))
    xmin2 = fit2.power_law.xmin
    xmax1 = max(df1)
    xmax2 = max(df2)
    fig1 = fit1.plot_ccdf(color= uzh_colors["red"], label= heuristic1 + ', '+ r'$\alpha$ = ' + alpha1 + ' in range c = [%.0f, %.0f]'%(xmin1,xmax1))
    fit1.power_law.plot_ccdf( color= uzh_colors['red'],linestyle='--',ax=fig1)
    fig2 = fit2.plot_ccdf(color= uzh_colors["green"], label= heuristic2 + ', '+ r'$\alpha$ = ' + alpha2 + ' in range c = [%.0f, %.0f]'%(xmin2,xmax2))
    fit2.power_law.plot_ccdf( color= uzh_colors["green"],linestyle='-.',ax=fig2)
    y_max_lim = max(fig1.properties()['ylim'][1], fig2.properties()['ylim'][1]) # get max value of y axis
    plt.ylim(0.0001, y_max_lim)
    plt.xscale('log')
    plt.yscale('log')
    plt.minorticks_off()
    plt.ylabel('Complementary cumulative distribution function: 1 - P(c)')
    plt.xlabel('Connected component size c')
    plt.title('PowerLaw Plot for: ' + ' '.join(cur.split('_')).capitalize() + ' ' + wt)
    # plt.title('PowerLaw Plot for: ' + ' '.join(cur.split('_')).capitalize() + ' ' + cur.capitalize() + 
    #             '\n' + r'$\alpha$' + ' = ' + alpha1 + ' for ' + heuristic1+' in range of component size c = [%.0f, %.0f]'%(xmin1,xmax1)+ 
    #             ' ' + 'and \n' + r'$\alpha$' + ' = ' + alpha2 + " for " + heuristic2+ " " + 'in range of component size c = [%.0f, %.0f]'%(xmin2,xmax2))
    plt.legend()
    plt.savefig(fig_file_name, bbox_inches="tight")
    plt.clf()
    return


def plot_modularity_graph(dataframe, community_property, title, fig_file_name):
    plt.figure(figsize = (8,8))
    x = dataframe["component_size"]
    y = dataframe[community_property]
    
    prop_name = ' '.join(community_property.split('_')).capitalize()
    min_val_comp = dataframe['component_size'].min()
    max_val_comp = dataframe['component_size'].max()
    title = title + '\n Component Size: Min: ' + str(min_val_comp) + ' Max: ' + str(max_val_comp)
    if 'modularity' not in community_property:
        plt.scatter(x, y, color=uzh_colors['green'])
        min_val = dataframe[community_property].min()
        max_val = dataframe[community_property].max()
        title = title + '\n'+ prop_name + ': Min: ' + str(min_val) + ' Max: ' + str(max_val)
    else: plt.scatter(x, y)
    if community_property == 'num_of_communities':
        X = np.array(np.log(dataframe['component_size']))
        Y = np.array(np.log(dataframe['num_of_communities']))
        slope, intercept  = np.polyfit(X, Y, 1)
        title = title + '\n' + ' Slope: ' + str(round(slope, 2)) + ' Intercept: ' + str(round(intercept, 2))
        plt.plot(x, x/3, color=uzh_colors['green_60'], label = 'Theoretical max num of communities')
        plt.legend()
    if max(x) > 10 : plt.xscale("log")
    if max(y) > 10 :
        if not (community_property=="modularity"): plt.yscale("log")
    plt.xlabel('Connected component size')
    plt.ylabel(prop_name)
    plt.title(title)
    plt.savefig(fig_file_name, bbox_inches="tight")
    plt.clf()
    return



def plot_edges_gaussian(x, y, title, wt, xlabel, ylabel, fig_file_name):
    fig = plt.figure(figsize = (8,8))
    xy = np.vstack([x,y])
    z = gaussian_kde(xy)(xy)
    fig, ax = plt.subplots()
    ax.scatter(x, y, c=z, s=5) 
    min_val = y.min()
    max_val = y.max()
    min_val_comp = x.min()
    max_val_comp = x.max()
    title = title + '\n ' + xlabel + ': Min: ' + str(min_val_comp) + ' Max: ' + str(max_val_comp) + \
                '\n '+ ylabel + ': Min: ' + str(min_val) + ' Max: ' + str(max_val)
    sm = plt.cm.ScalarMappable(cmap = plt.cm.get_cmap('viridis'))
    fig.colorbar(sm)
    x_unique = np.unique(x)
    if wt != 'weighted':
        plt.plot(x_unique, x_unique*(x_unique-1)/2, color = 'green', linewidth = 0.85, label = 'Theoretical max num of edges')
    plt.plot(x_unique, x_unique-1, color = 'red', linewidth = 0.85, label = 'Theoretical min num of edges')
    plt.legend()
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    if max(x) > 10 : plt.xscale("log")
    if max(y) > 10 : plt.yscale("log")
    plt.minorticks_off()
    plt.savefig(fig_file_name, bbox_inches="tight")
    plt.clf()
    return




def plot_density_graph(df, xlabel, fig_file_name, title):
    plt.figure(figsize=(8,8))
    bins_num = np.logspace(np.log10(min(df)), np.log10(max(df)+1),30)
    plt.hist(df, bins = bins_num, density = True, cumulative=-1, histtype='step')
    plt.xscale('log')
    plt.yscale('log')
    plt.minorticks_off()                        
    plt.xlabel('Connected component size')
    plt.ylabel('Probability Density')
    min_val_comp = df.min()
    max_val_comp = df.max()
    title = title + '\n Component Size: Min: ' + str(min_val_comp) + ' Max: ' + str(max_val_comp)
    plt.title(title)
    plt.savefig(fig_file_name, bbox_inches="tight")
    plt.clf()
    return
