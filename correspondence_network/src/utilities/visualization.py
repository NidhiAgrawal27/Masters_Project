import matplotlib.pyplot as plt
import powerlaw as pl
import numpy as np
import warnings


def plot_density_graph(df, xlabel, fig_file_name, cur, heuristic):
    plt.figure(figsize=(8,8))
    bins_num = np.logspace(np.log10(min(df)), np.log10(max(df)+1),30)
    plt.hist(df, bins = bins_num, density = True, edgecolor='White')
    plt.xscale('log')
    plt.yscale('log')                            
    plt.xlabel(xlabel, fontsize=14)
    plt.title("Distribution of addresses for " + cur.capitalize() + ' ' + heuristic ,fontsize=15)
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
    plt.xlabel('\nfit.distribution_compare(power_law, lognormal): '+ str(fit.distribution_compare('power_law', 'lognormal')), fontsize = 16)
    plt.title(cur.capitalize() + ' ' + heuristic + ': alpha = %f in range [%.0f,%.0f]'%(alpha,xmin,xmax),fontsize=15)
    plt.savefig(fig_file_name, bbox_inches="tight")
    return


def plot_modularity_graph(dataframe, community_property, title, fig_file_name):
    plt.figure(figsize = (8,8))
    plt.bar(x = dataframe["Component_Size"],height = dataframe[community_property])
    plt.xscale("log") 
    if not (community_property=="Modularity"): plt.yscale("log") 
    plt.xlabel("Component Size")
    plt.ylabel(community_property)
    plt.title(title)
    plt.savefig(fig_file_name, bbox_inches="tight")
    return


