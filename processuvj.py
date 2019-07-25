import matplotlib.pyplot as plt
import numpy as np
from matplotlib import rc
rc('text', usetex=True)
from loaddata import load_goodss
from fitmodeltest import fitmodel
from astropy.constants import M_sun

def plotuvj(uminusv,vminusj,SSFR,title):
    plt.scatter(vminusj,uminusv, s=25., c=SSFR, cmap = "jet_r",edgecolors="black")
    zpt = .49
    xstart = (1.3-zpt)/.88
    xend = 1.6
    plt.plot((-1.,xstart),(1.3,1.3), color="black")
    x = np.linspace(xstart, xend)
    y = .88*x + zpt
    plt.plot(x,y, color="black")
    plt.plot((1.6,1.6),(1.6*.88 + zpt, 3.), color="black")
    #when plotting nicely, remember to limit axes!
    plt.xlabel(r"$\mathbf V - J$")
    plt.ylabel(r"$\mathbf U - V$")
    plt.title(title)
    plt.show()

def main():

    #cosmo = FlatLambdaCDM(H0=70., Om0 = .3)
    #need to check which column to use - massformed, stellar mass or formed mass?????
    #currently implementing formed mass
    data = np.loadtxt("uvjoutput.csv", skiprows=1, usecols = (47,50,0,29,17,26,23,5), delimiter = ",")
    uminusv = data[:,0]
    vminusj = data[:,1]
    #### check that units are all understood correctly
    ID = data[:,2]
    SSFR = data[:,3]
    z = data[:,4]
    SFR = data[:,5]
    mass = data[:,6]
    mass = np.power(10*np.ones_like(mass), mass) #convert log mass into mass
    age = data[:,7]*(10**9) #convert age into yr

    plotuvj(uminusv,vminusj,SSFR,r"\bf UVJ diagram of all galaxies using Williams et al. (2009) $\mathbf z > 1$ constraints for determining quiescence")

    #currently this does nothing to further eliminate values - selection based on Pacifici 2016
    #indices = SSFR < .2/age
    #selection based on thesis normalised SFR
    indices = (z > 2.) & (mass > 10**10) & (age*SFR/mass < .1)
    uminusv = uminusv[indices]
    vminusj = vminusj[indices]
    ID = ID[indices]
    SSFR = SSFR[indices]
    z = z[indices]
    SFR = SFR[indices]
    mass = mass[indices]
    age = age[indices]

    plotuvj(uminusv,vminusj,SSFR,r"\bf UVJ diagram of quiescent galaxies using selection criteria of Carnall et al. 2018")

    mask = (uminusv > 1.3) & (vminusj < 1.6) & (uminusv > .88*vminusj + .49)
    ID = ID[mask]
    ID = list(ID)
    del ID[7]
    print(ID)
    input()
    for i in range(len(ID)):
        fitmodel(ID[i],saveplot=True)

main()
