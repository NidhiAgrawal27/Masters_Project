import matplotlib.pyplot as plt
import powerlaw as pl
import numpy as np
import matplotlib as mpl
import matplotlib.font_manager as fm

uzh_color_map = ['#0028a5', '#dc6027', '#91c34a', '#fede00', '#a3adb7', '#0b82a0', '#2a7f62', # FULL
                 '#667ec9', '#eaa07d', '#bfdf94', '#fcec7c', '#c8ced4', '#6bb7c7', '#80b6a4', # 60%
                 '#3353b7', '#e38052', '#aad470', '#fbe651', '#b5bdc5', '#3c9fb6', '#569d85', # 80%
                 '#99a9db', '#f1bfa9', '#d5e9b7', '#fdf3a8', '#dadee2', '#9ed0d9', '#abcec2', # 40%
                 '#ccd4ed', '#f8dfd4', '#eaf4db', '#fef9d3', '#edeff1', '#cfe8ec', '#d5e7e1'] # 20%


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
                    })

mpl.rcParams['axes.linewidth'] = 1.2
mpl.rcParams['axes.prop_cycle'] = mpl.cycler(color=uzh_color_map)


def plot_density_graph(df, xlabel, fig_file_name, cur, heuristic):
    plt.figure(figsize=(8,8))
    # bins_num = np.logspace(np.log10(min(df)), np.log10(max(df)+1),30)
    # plt.hist(df, bins = bins_num, density = True, edgecolor='White')

    import scipy.stats as stats
    df_plot = df.copy().sort_values()
    df_mean = np.mean(df_plot)
    df_std = np.std(df_plot)
    pdf = stats.norm.pdf(df_plot, df_mean, df_std)
    plt.scatter(df_plot, pdf)

    plt.xscale('log')
    plt.yscale('log')                            
    plt.xlabel('Connected component size')
    plt.ylabel('Probability Density')
    plt.title(' '.join(cur.split('_')).capitalize() + ' ' + heuristic)
    plt.savefig(fig_file_name, bbox_inches="tight")
    return


def plotPowerLaw(df, cur, heuristic, fig_file_name, xmin= None, xmax = None):
    plt.figure(figsize=(8,8))
    fit = pl.Fit(df , xmin, xmax = xmax)
    alpha = fit.power_law.alpha
    xmin = fit.power_law.xmin
    if xmax is None: xmax = max(df)
    fig = fit.plot_ccdf()
    fit.power_law.plot_ccdf( color= 'b',linestyle='--',label='fit ccdf',ax=fig)
    plt.xscale('log')
    plt.yscale('log')
    plt.ylabel('Complementary cumulative distribution function 1 - P(c)')
    plt.xlabel('Connected component size c')
    # plt.xlabel('\nNumber of addresses\nfit.distribution_compare(power_law, lognormal): '+ str(fit.distribution_compare('power_law', 'lognormal')), fontsize = 14)
    plt.title('PowerLaw Plot for ' + ' '.join(cur.split('_')).capitalize() + ' ' + 
                    heuristic + '\n' + r'$\alpha$' + '= %f in range [xmin, xmax] = [%.0f, %.0f]'%(alpha,xmin,xmax))
    plt.savefig(fig_file_name, bbox_inches="tight")
    return


def plot_modularity_graph(dataframe, community_property, title, fig_file_name):
    plt.figure(figsize = (8,8))
    plt.scatter(x = dataframe["component_size"], y = dataframe[community_property])
    plt.xscale("log")
    if not (community_property=="modularity"): plt.yscale("log") 
    if community_property == 'num_of_edges':
        min_edge = dataframe[community_property].min()
        max_edge = dataframe[community_property].max()
        title = title + '\n Number of edges: Min: ' + str(min_edge) + ' Max: ' + str(max_edge)
    plt.xlabel('Connected component size')
    plt.ylabel(' '.join(community_property.split('_')).capitalize())
    plt.title(title)
    plt.savefig(fig_file_name, bbox_inches="tight")
    return

