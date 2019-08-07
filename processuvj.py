import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
from loaddata import load_goodss
from fitmodeltest import fitmodel
import pandas as pd
from fitmodeltest import fitcatmodel
from fitmodeltest import getfitinstructions
#from mpl_toolkits.axes_grid1.inset_locator import zoomed_inset_axes
#from mpl_toolkits.axes_grid1.inset_locator import mark_inset

def plotuvj(uminusv,vminusj,SSFR,title):
    fig,ax=plt.subplots()
    norm = mpl.colors.Normalize(vmin=-12.,vmax=-8)
    if title == "passiveplot_dblplaw":
        scatter = ax.scatter(vminusj,uminusv, s=25., c=SSFR, cmap = "RdYlGn",norm=norm,edgecolors="black",linewidths=.5)
        #axins = zoomed_inset_axes(ax,1.5,loc=4)
        #axins.scatter(vminusj,uminusv, s=25., c=SSFR, cmap = "RdYlGn",norm=norm,edgecolors="black",linewidths=.5)
        #axins.set_xlim(np.amin(vminusj)-.1,np.amax(vminusj)+.1)
        #axins.set_ylim(np.amin(uminusv)-.1,np.amax(uminusv)+.1)
        #mark_inset(ax, axins, loc1=2, loc2=1, fc="none", ec="0.5")
    else:
        scatter = ax.scatter(vminusj,uminusv, s=25., c=SSFR, cmap = "RdYlGn",norm=norm)
    zpt = .69
    xstart = (1.3-zpt)/.88
    xend = 1.6
    line1 = ax.plot((-1.,xstart),(1.3,1.3), color="black")
    x = np.linspace(xstart, xend)
    y = .88*x + zpt
    line2 = ax.plot(x,y, color="black")
    line3 = ax.plot((1.6,1.6),(1.6*.88 + zpt, 5.), color="black")
    #when plotting nicely, remember to limit axes!
    ax.set_xlabel(r"$V - J$")
    ax.set_ylabel(r"$U - V$")
    ax.set_xlim(-1.,6.)
    ax.set_ylim(-1.,5.)
    cbar = plt.colorbar(scatter)
    cbar.ax.set_ylabel(r"$\log_{10} \mathrm{(sSFR)}$")
    ax.annotate("N = " + str(uminusv.shape[0]),xy=(-.5,3.5))
    fig.savefig(title + ".pdf")
    plt.show()

def main():

    merlinlist = [10578,22085,2717,2782,3912,8785,9209,17749,18180,23626,2608,3897,3973,4503,4587]
    merlinlist.extend([5592,6407,7526,7688,8242,9091,10759,12178,15457,16506,19301,19446,19505,22610,26802])
    merlin_allpass = [merlinlist[0],merlinlist[1]]
    merlin_nebularpass = merlinlist[2:10]
    merlin_firstpass = merlinlist[10:]
    #need to check which column to use - massformed, stellar mass or formed mass?????
    #currently implementing formed mass
    dataset = pd.read_csv("uvjoutput_dblplaw.csv", header=0,index_col = "#ID")
    data = dataset.to_numpy()
    #data = np.loadtxt("uvjoutput_5000.csv", skiprows=1, usecols = (47,50,0,29,17,26,23,5), delimiter = ",")
    uminusv = data[:,49]
    vminusj = data[:,52]
    ID = np.loadtxt("uvjoutput_dblplaw.csv",usecols=0,delimiter=',')
    ID = ID.astype(int)
    SSFR = data[:,31]
    z = data[:,19]
    nSFR = data[:,34]
    SFR = data[:,28]
    #nSFR = np.power(10*(nSFR/nSFR),nSFR)
    mass = data[:,25]
    mass = np.power(10*np.ones_like(mass), mass) #convert log mass into mass

    plotuvj(uminusv,vminusj,SSFR,"fullplot_dblplaw")

    #selection based on thesis normalised SFR
    indices = (z > 2.) # & (nSFR < -1)
    uminusv_passive = uminusv[indices]
    vminusj_passive = vminusj[indices]
    ID_passive = ID[indices]
    SSFR_passive = SSFR[indices]
    nSFR_passive = nSFR[indices]

    # do plot for just z>2 as well as passiveplot

    plotuvj(uminusv_passive,vminusj_passive,SSFR_passive,"zgreaterthan2plot_dblplaw")

    indices = nSFR_passive < -1.
    uminusv_passive = uminusv_passive[indices]
    vminusj_passive = vminusj_passive[indices]
    ID_passive = ID_passive[indices]
    SSFR_passive = SSFR_passive[indices]

    plotuvj(uminusv_passive,vminusj_passive,SSFR_passive,"passiveplot_dblplaw")

    #mask = (uminusv_passive > 1.3) & (vminusj_passive < 1.6) & (uminusv_passive > .88*vminusj_passive + .49)
    #ID_passive = ID_passive[mask]
    ID_passive_list = ID_passive.tolist()
    print(ID_passive_list)
    ID_list = ID.tolist()
    columns = ["Passive","Merlin_etal_decision"]
    extracols = pd.DataFrame(np.zeros((ID.shape[0],2)),columns=columns,index=ID)
    for i in range(0,len(ID_passive_list)):
        extracols.loc[[ID_passive_list[i]],["Passive"]] = 1
    for i in range(0,ID.shape[0]):
        if (ID_list[i] in merlin_allpass):
            extracols.loc[[ID_list[i]],["Merlin_etal_decision"]] = 111
        elif (ID_list[i] in merlin_nebularpass):
            extracols.loc[[ID_list[i]],["Merlin_etal_decision"]] = 110
        elif (ID_list[i] in merlin_firstpass):
            extracols.loc[[ID_list[i]],["Merlin_etal_decision"]] = 100

    finalframe = pd.concat([dataset, extracols], axis=1)
    print(finalframe)
    finalframe.to_csv(path_or_buf="uvjoutput_dblplaw_passivetest.csv",index_label='#ID')

    ### talk to Adam about this on Monday
    #ID_passive_list.remove(1039,1557,1910,2283,2682,3284,3312,3497,3818,4079,4334,4587,4624,5420,5527,5544,7526,7688,8785,22805)

    print(ID_passive_list)

    input("Do you want to make plots for passive galaxies in existing catalogue?")
    fitcatmodel(ID_passive_list,"guo_v2")

main()
