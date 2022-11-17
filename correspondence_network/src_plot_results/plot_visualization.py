import matplotlib.pyplot as plt
import powerlaw as pl
import numpy as np
import matplotlib as mpl
import matplotlib.font_manager as fm
from scipy.stats import gaussian_kde
import pandas as pd
import matplotlib.offsetbox as offsetbox
import scipy.stats as stats


uzh_color_map = ['#0028a5', '#dc6027', '#91c34a', '#fede00', '#a3adb7', '#0b82a0', '#2a7f62', # FULL
                 '#667ec9', '#eaa07d', '#bfdf94', '#fcec7c', '#c8ced4', '#6bb7c7', '#80b6a4', # 60%
                 '#3353b7', '#e38052', '#aad470', '#fbe651', '#b5bdc5', '#3c9fb6', '#569d85', # 80%
                 '#99a9db', '#f1bfa9', '#d5e9b7', '#fdf3a8', '#dadee2', '#9ed0d9', '#abcec2', # 40%
                 '#ccd4ed', '#f8dfd4', '#eaf4db', '#fef9d3', '#edeff1', '#cfe8ec', '#d5e7e1'] # 20%


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
    plt.clf()
    return


def plotPowerLaw_superimpose(df1, df2, cur, heuristic1, heuristic2, fig_file_name, xmin= None, xmax = None):
    plt.figure(figsize=(8,8))
    fit1 = pl.Fit(df1 , xmin, xmax = xmax)
    fit2 = pl.Fit(df2 , xmin, xmax = xmax)
    alpha1 = fit1.power_law.alpha
    xmin1 = fit1.power_law.xmin
    alpha2 = fit2.power_law.alpha
    xmin2 = fit2.power_law.xmin
    xmax1 = max(df1)
    xmax2 = max(df2)
    fig1 = fit1.plot_ccdf()
    fit1.power_law.plot_ccdf( color= 'r',linestyle='--',ax=fig1, label= heuristic1)
    fig2 = fit2.plot_ccdf()
    fit2.power_law.plot_ccdf( color= 'g',linestyle='-.',ax=fig2, label= heuristic2)
    plt.xscale('log')
    plt.yscale('log')
    plt.ylabel('Complementary cumulative distribution function 1 - P(c)')
    plt.xlabel('Connected component size c')
    # plt.xlabel('\nNumber of addresses\nfit.distribution_compare(power_law, lognormal): '+ str(fit.distribution_compare('power_law', 'lognormal')), fontsize = 14)
    plt.title('PowerLaw Plot for: ' + ' '.join(cur.split('_')).capitalize() + ' ' + cur.capitalize() + 
                '\n' + r'$\alpha$' + ' = %f for'%(alpha1)+ ' ' + heuristic1+' in range [xmin, xmax] = [%.0f, %.0f]'%(xmin1,xmax1)+ 
                ' ' + 'and \n' + r'$\alpha$' + ' = %f for'%(alpha2)+ " " + heuristic2+ " " + 'in range [xmin, xmax] = [%.0f, %.0f]'%(xmin2,xmax2))
    plt.legend()
    plt.savefig(fig_file_name, bbox_inches="tight")
    plt.clf()
    return


def plot_modularity_graph(dataframe, community_property, title, fig_file_name):
    plt.figure(figsize = (8,8))
    plt.scatter(x = dataframe["component_size"], y = dataframe[community_property])
    plt.xscale("log")
    prop_name = ' '.join(community_property.split('_')).capitalize()
    min_val_comp = dataframe['component_size'].min()
    max_val_comp = dataframe['component_size'].max()
    title = title + '\n Component Size: Min: ' + str(min_val_comp) + ' Max: ' + str(max_val_comp)
    if not (community_property=="modularity"): plt.yscale("log") 
    if community_property != 'modularity':
        min_val = dataframe[community_property].min()
        max_val = dataframe[community_property].max()
        title = title + '\n'+ prop_name + ': Min: ' + str(min_val) + ' Max: ' + str(max_val)
    if community_property == 'num_of_communities':
        X = np.array(np.log(dataframe['component_size']))
        Y = np.array(np.log(dataframe['num_of_communities']))
        slope, intercept  = np.polyfit(X, Y, 1)
        title = title + '\n' + ' Slope: ' + str(round(slope, 2)) + ' Intercept: ' + str(round(intercept, 2))
    plt.xlabel('Connected component size')
    plt.ylabel(prop_name)
    plt.title(title)
    plt.savefig(fig_file_name, bbox_inches="tight")
    plt.clf()
    return


def plot_gaussian(x, y, cur, xlabel, ylabel, fig_file_name):
    fig = plt.figure(figsize = (8,8))
    xy = np.vstack([x,y])
    z = gaussian_kde(xy)(xy)
    fig, ax = plt.subplots()
    ax.scatter(x, y, c=z, s=30) 
    min_val = y.min()
    max_val = y.max()
    min_val_comp = x.min()
    max_val_comp = x.max()
    title = ' '.join(cur.split('_')).capitalize() + '\n ' + xlabel + ': Min: ' + str(min_val_comp) + ' Max: ' + str(max_val_comp)
    title = title + '\n '+ ylabel + ': Min: ' + str(min_val) + ' Max: ' + str(max_val)
    sm = plt.cm.ScalarMappable(cmap = plt.cm.get_cmap('viridis'))
    fig.colorbar(sm)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.xscale("log") 
    plt.yscale("log") 
    plt.savefig(fig_file_name, bbox_inches="tight")
    plt.clf()
    return


def plot_find_slope(dataframe, prop, title, fig_file_name):
    plt.figure(figsize = (8,8))
    x = dataframe["component_size"]
    y = dataframe[prop]
    # plt.scatter(x,y)
    X = np.array(np.log(x))
    Y = np.array(np.log(y))
    plt.scatter(X,Y)
    slope, intercept  = np.polyfit(X, Y, 1)
    xseq = np.linspace(0, max(X)-1, num=10)
    plt.plot(xseq, slope * xseq + intercept, color='r')
    prop_name = ' '.join(prop.split('_')).capitalize()
    min_val_comp = dataframe['component_size'].min()
    max_val_comp = dataframe['component_size'].max()
    title = title + '\n Component Size: Min: ' + str(min_val_comp) + ' Max: ' + str(max_val_comp)
    min_val = dataframe[prop].min()
    max_val = dataframe[prop].max()
    title = title + '\n'+ prop_name + ': Min: ' + str(min_val) + ' Max: ' + str(max_val)
    title = title + '\n' + ' Slope: ' + str(round(slope, 2)) + ' Intercept: ' + str(round(intercept, 2))
    # plt.xscale('log')
    # plt.yscale('log')
    plt.xlabel('Connected component size (log value)')
    plt.ylabel(prop_name + ' (log value)') 
    plt.title(title)
    plt.savefig(fig_file_name, bbox_inches="tight")
    plt.clf()
    return


def plot_probability(df, xlabel, fig_file_name, cur, heuristic):
    plt.figure(figsize=(8,8))
    val_counts = df.value_counts(normalize=True)
    plt.scatter(val_counts.index, val_counts)
    plt.xscale('log')
    plt.yscale('log')                            
    plt.xlabel('Connected component size')
    plt.ylabel('Probability')
    title = ' '.join(cur.split('_')).capitalize() + ' ' + heuristic
    min_val_comp = df.min()
    max_val_comp = df.max()
    min_prob = round(val_counts.min(), 5)
    max_prob = round(val_counts.max(), 5)
    title = title + '\n Component Size: Min: ' + str(min_val_comp) + ' Max: ' + str(max_val_comp)
    title = title + '\n Probability: Min: ' + str(min_prob) + ' Max: ' + str(max_prob)
    plt.title(title)
    plt.savefig(fig_file_name, bbox_inches="tight")
    plt.clf()
    return


def plot_density_graph(df, xlabel, fig_file_name, cur, heuristic):
    plt.figure(figsize=(8,8))
    bins_num = np.logspace(np.log10(min(df)), np.log10(max(df)+1),30)
    plt.hist(df, bins = bins_num, density = True, edgecolor='White')
    plt.xscale('log')
    plt.yscale('log')                            
    plt.xlabel('Connected component size')
    plt.ylabel('Probability Density')
    title = ' '.join(cur.split('_')).capitalize() + ' ' + heuristic
    min_val_comp = df.min()
    max_val_comp = df.max()
    title = title + '\n Component Size: Min: ' + str(min_val_comp) + ' Max: ' + str(max_val_comp)
    plt.title(title)
    plt.savefig(fig_file_name, bbox_inches="tight")
    plt.clf()
    return


def plot_pdf(df, xlabel, fig_file_name, cur, heuristic):
    plt.figure(figsize=(8,8))
    df_plot = df.copy().sort_values()
    df_mean = np.mean(df_plot)
    df_std = np.std(df_plot)
    pdf = stats.norm.pdf(df_plot, df_mean, df_std)
    plt.scatter(df_plot, pdf)
    plt.xscale('log')
    plt.yscale('log')                            
    plt.xlabel('Connected component size')
    plt.ylabel('Probability Density')
    title = ' '.join(cur.split('_')).capitalize() + ' ' + heuristic
    min_val_comp = df_plot.min()
    max_val_comp = df_plot.max()
    min_prob = round(pdf.min(), 5)
    max_prob = round(pdf.max(), 5)
    title = title + '\n Component Size: Min: ' + str(min_val_comp) + ' Max: ' + str(max_val_comp)
    title = title + '\n Probability Density: Min: ' + str(min_prob) + ' Max: ' + str(max_prob)
    plt.title(title)
    plt.savefig(fig_file_name, bbox_inches="tight")
    plt.clf()
    return


# def plot_densitygraph_vertical(df1, df2, prop, fig_file_name, cur, heuristic1, heuristic2):
#     fig, axs = plt.subplots(2)
#     import scipy.stats as stats
#     df1_plot = df1[prop].copy().sort_values()
#     df2_plot = df2[prop].copy().sort_values()
#     df1_mean = np.array(np.mean(df1_plot, axis=0))
#     df1_std = np.array(np.std(df1_plot, axis=0))
#     pdf1 = stats.norm.pdf(df1_plot, df1_mean, df1_std)
#     df2_mean = np.mean(df2_plot)
#     df2_std = np.std(df2_plot)
#     pdf2 = stats.norm.pdf(df2_plot, df2_mean, df2_std)
#     axs[0].scatter(df1_plot, pdf1)
#     axs[1].scatter(df2_plot, pdf2) 
#     plt.xscale('log')
#     plt.yscale('log')                            
#     plt.xlabel('Connected component size')
#     plt.ylabel('Probability Density')  
#     axs[0].set_title(' '.join(cur.split('_')).capitalize() + ' ' + heuristic1)
#     axs[1].set_title(' '.join(cur.split('_')).capitalize() + ' ' + heuristic2)
#     plt.title(' '.join(cur.split('_')).capitalize())
#     plt.savefig(fig_file_name, bbox_inches="tight")
#     plt.clf()
#     return

 
