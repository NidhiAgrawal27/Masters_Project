import matplotlib.pyplot as plt
import powerlaw
from scipy.special import factorial
import numpy as np



def plot_density_graph(df, xlabel, fig_file_name, cur):
    plt.figure(figsize=(8,8))
    bins_num = np.logspace(np.log10(min(df)), np.log10(max(df)+1),30)
    plt.hist(df, bins = bins_num, density = True, edgecolor='White')
    plt.xscale('log')
    plt.yscale('log')                            
    plt.xlabel(xlabel, fontsize=14)
    plt.title("Distribution of addresses for " + cur.capitalize() ,fontsize=15)
    plt.savefig(fig_file_name, bbox_inches="tight")
    return


def distributions(avgDeg, degSpacing):
    
    poissonList = []
    expList = []
    kList = []
    
    for k in sorted(degSpacing):
        poisson = ((avgDeg**k)/factorial(k))*np.exp(-avgDeg) # Poisson Distribution
        poissonList.append(poisson)
        exp = (avgDeg**(-1))*np.exp(-k/avgDeg) # Exponential Distribution
        expList.append(exp)
        kList.append(k)
    
    plt.xscale('log')
    plt.yscale('log')
    plt.ylim(10**(-8), 10) # Fix the y limits to fit all the points
    plt.plot(kList, poissonList, color = 'lime', label = 'Poisson')
    plt.plot(kList, expList, color = 'violet', label = 'Exponential')
    

def plotPowerLaw(degreeArray, degSpacing, avgDeg, fig_file_name, cur): 
    
    fit = powerlaw.Fit(degreeArray, discrete=True)    # fit  P(k)
    alpha = fit.power_law.alpha        # power-law exponent
    sigma = fit.power_law.sigma        # standard error
    
    
    print('Power-law exponent for '+ cur + ' network: alpha = ', round(alpha,3))
    print('Corresponding error '+ cur + ' network: sigma = ', round(sigma,3))
    print('\n')
    
    plt.figure(figsize=(9,6))

    distributions(avgDeg, degSpacing) # call method to plot poisson and exponential distributions

    fit.power_law.plot_pdf(color='r', label = 'pdf - fitted')                          # Plot P(k) - fitted
    powerlaw.plot_pdf(degreeArray, color='b', marker='o', label = 'pdf - not fitted')  # Plot P(k) - not fitted

    plt.plot(degSpacing, degSpacing**(-alpha), color = 'darkgreen', label = '(kˆ(-alpha) vs k')

    plt.xlabel('Degree (k)', fontsize = 16)
    plt.ylabel('P(k): Probability of degree k', fontsize = 16)
    plt.title(cur, fontsize = 16)
    plt.legend(fontsize = 12)
    plt.savefig(fig_file_name, bbox_inches="tight")
    