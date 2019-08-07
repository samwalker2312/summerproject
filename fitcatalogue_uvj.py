from loaddata import load_goodss
import bagpipes as pipes
import numpy as np
import pandas as pd

filt_list = np.loadtxt("filters/goodss_filt_list.txt", dtype="str")
exp = {}
exp["age"] = (0.1,15.)
exp["tau"] = (0.3, 12.)
exp["massformed"] = (2., 15.)
exp["metallicity"] = (0., 2.5)
dust = {}
#dust["type"] = "Cardelli"
#dust["Av"] = (0.,2.)

dblplaw = {}
dblplaw["tau"] = (0., 15.)
dblplaw["alpha"] = (0.01, 1000.)
dblplaw["beta"] = (0.01, 1000.)
dblplaw["alpha_prior"] = "log_10"
dblplaw["beta_prior"] = "log_10"
dblplaw["massformed"] = (1., 13.)
dblplaw["metallicity"] = (0.01, 2.5)
dblplaw["metallicity_prior"] = "log_10"

dust = {}
dust["type"] = "Calzetti"
dust["Av"] = (0.,8.)
dust["eta"] = 2.

nebular = {}
nebular["logU"] = -3.

fit_instructions = {}
fit_instructions["redshift"] = (0., 10.)
#fit_instructions["exponential"] = exp
fit_instructions["dust"] = dust
fit_instructions["dblplaw"] = dblplaw
fit_instructions["t_bc"] = 0.01
fit_instructions["nebular"] = nebular

IDs = np.arange(1, 6001)
IDs = IDs.tolist()
merlinlist = [10578,22085,2717,2782,3912,8785,9209,17749,18180,23626,2608,3897,3973,4503,4587]
merlinlist.extend([5592,6407,7526,7688,8242,9091,10759,12178,15457,16506,19301,19446,19505,22610,26802])
IDs.extend(merlinlist)
IDs = np.array(IDs)
IDs = np.unique(IDs)
columns = ["uminusv_16","uminusv_50","uminusv_84","vminusj_16","vminusj_50","vminusj_84","RA","Dec"]
frame = pd.DataFrame(np.zeros((IDs.shape[0],8)), columns = columns, index = IDs)
cat = np.loadtxt("hlsp_candels_hst_wfc3_goodss-tot-multiband_f160w_v1-1photom_cat.txt",
                 usecols=(2,3))

def save_uvj(fit):
    ID = int(fit.galaxy.ID)
    fit.posterior.get_advanced_quantities()
    uvj = fit.posterior.samples["uvj"]
    uminusv = np.percentile(uvj[:, 0] - uvj[:, 1], (16,50,84))
    vminusj = np.percentile(uvj[:, 1] - uvj[:, 2], (16,50,84))
    frame.loc[[ID],["uminusv_16"]] = uminusv[0]
    frame.loc[[ID],["uminusv_50"]] = uminusv[1]
    frame.loc[[ID],["uminusv_84"]] = uminusv[2]
    frame.loc[[ID],["vminusj_16"]] = vminusj[0]
    frame.loc[[ID],["vminusj_50"]] = vminusj[1]
    frame.loc[[ID],["vminusj_84"]] = vminusj[2]
    coords = getcoords(ID)
    frame.loc[[ID],["RA"]] = coords[0]
    frame.loc[[ID],["Dec"]] = coords[1]

def getcoords(ID):
    row = int(ID) - 1
    coords = cat[row,:]
    return coords

fit_cat = pipes.fit_catalogue(IDs, fit_instructions, load_goodss,\
 spectrum_exists=False, cat_filt_list=filt_list, run="guo_v2", analysis_function=save_uvj)
fit_cat.fit(verbose=False)
frame = frame.sort_index()
dataset = pd.read_csv("pipes/cats/guo_v2.cat", delim_whitespace = True, header=0,index_col = "#ID")
dataset = dataset.sort_index()
finalframe = pd.concat([dataset, frame], axis=1)
print(finalframe)
input("Looking good? Want to save?")
finalframe.to_csv(path_or_buf="uvjoutput_dblplaw.csv", index_label="#ID")
