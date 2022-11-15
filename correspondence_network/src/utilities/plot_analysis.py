import matplotlib.pyplot as plt
import powerlaw as pl
import numpy as np
import matplotlib as mpl
import matplotlib.font_manager as fm
import mpl_scatter_density # adds projection='scatter_density'
from scipy.stats import gaussian_kde
import pandas as pd

mona_uwt_h0 = pd.read_csv('/Users/sanjanawarambhey/Downloads/Github/monacoin_logs/unweighted/h0/generated_files/monacoin_h0_components.csv')
mona_uwt_h0_h1 = pd.read_csv('/Users/sanjanawarambhey/Downloads/Github/monacoin_logs/unweighted/h0_h1/generated_files/monacoin_h0_h1_components.csv')
mona_wt_h0 = pd.read_csv('/Users/sanjanawarambhey/Downloads/Github/monacoin_logs/weighted/monacoin_h0_wt_components.csv')
mona_wt_h0_h1 = pd.read_csv('/Users/sanjanawarambhey/Downloads/Github/monacoin_logs/weighted/monacoin_h0_h1_wt_components.csv')

def plotPowerLaw_impose(df1, df2, cur, heuristic1, heuristic2, type_of_file, fig_file_name, xmin= None, xmax = None):
    plt.figure(figsize=(8,8))
    fit1 = pl.Fit(df1 , xmin, xmax = xmax)
    fit2 = pl.Fit(df2 , xmin, xmax = xmax)
    alpha1 = fit1.power_law.alpha
    xmin1 = fit1.power_law.xmin
    alpha2 = fit2.power_law.alpha
    xmin2 = fit2.power_law.xmin
    xmax1 = max(df1)
    xmax2 = max(df2)
    fig = fit1.plot_ccdf()
    fit1.power_law.plot_ccdf( color= 'r',linestyle='--',ax=fig, label= heuristic1)
    fig2 = fit2.plot_ccdf()
    fit2.power_law.plot_ccdf( color= 'b',linestyle='-.',ax=fig, label= heuristic2)
    plt.xscale('log')
    plt.yscale('log')
    plt.ylabel('Complementary cumulative distribution function 1 - P(c)', fontsize = 14)
    plt.xlabel('\nConnected component size c', fontsize = 14)
    # plt.xlabel('\nNumber of addresses\nfit.distribution_compare(power_law, lognormal): '+ str(fit.distribution_compare('power_law', 'lognormal')), fontsize = 14)
    plt.title('PowerLaw Plot for: ' + type_of_file.capitalize() + " " + cur.capitalize() + '\n\u03B1 = %f for'%(alpha1)+ " " + heuristic1+ " " + 'in range [xmin, xmax] = [%.0f,%.0f]'%(xmin1,xmax1)+ " " + 'and \n\u03B1 = %f for'%(alpha2)+ " " + heuristic2+ " " + 'in range [xmin, xmax] = [%.0f,%.0f]'%(xmin2,xmax2))
    plt.legend()
    plt.show()
    plt.savefig(fig_file_name, bbox_inches="tight")
    return


def plot_heatmap(dataframe, title, fig_file_name):
    fig = plt.figure(figsize = (8,8))
    x = dataframe["component_size"]
    y = dataframe["num_of_edges"]
    xy = np.vstack([x,y])
    z = gaussian_kde(xy)(xy)
    fig, ax = plt.subplots()
    ax.scatter(x, y, c=z, s=100) 
    min_edge = dataframe["num_of_edges"].min()
    max_edge = dataframe["num_of_edges"].max()
    title = title + '\n Number of edges: Min: ' + str(min_edge) + ' Max: ' + str(max_edge)
    sm = plt.cm.ScalarMappable(cmap = plt.cm.get_cmap('viridis'))
    fig.colorbar(sm)
    plt.xlabel('Connected component size')
    plt.ylabel(' '.join("num_of_edges".split('_')).capitalize())
    plt.title(title)
    plt.xscale("log") 
    plt.yscale("log") 
    plt.show()
    plt.savefig(fig_file_name, bbox_inches="tight")
    return


# plotPowerLaw_impose(mona_wt_h0['num_of_addrs'],mona_wt_h0_h1['num_of_addrs'], "Monacoin", 'h0', 'h0_h1', 'weighted', 'Monacoin_powerlaw', xmax=None, xmin=None)
plot_heatmap(mona_wt_h0,'Monacoin','Monacoin_powerlaw')




