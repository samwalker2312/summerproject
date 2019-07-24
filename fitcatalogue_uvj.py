from loaddata import load_goodss
from loaddata import load_vandels_spec
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
dust["type"] = "Cardelli"
dust["Av"] = (0.,2.)
fit_instructions = {}
fit_instructions["redshift"] = (0., 10.)
fit_instructions["exponential"] = exp
fit_instructions["dust"] = dust

IDs = np.arange(1, 1932)
columns = ["uminusv_16","uminusv_50","uminusv_84","vminusj_16","vminusj_50","vminusj_84"]
frame = pd.DataFrame(np.zeros((1931,6)), columns = columns, index = IDs)

def save_uvj(fit):
    ID = float(fit.galaxy.ID)
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

fit_cat = pipes.fit_catalogue(IDs, fit_instructions, load_goodss,\
 spectrum_exists=False, cat_filt_list=filt_list, run="guo", analysis_function=save_uvj)
fit_cat.fit(verbose=False)
dataset = pd.read_csv("pipes/cats/guo.cat", delim_whitespace = True, header=0,index_col = "#ID")
finalframe = pd.concat([dataset, frame], axis=1)
finalframe.to_csv(path_or_buf="uvjoutput.csv", index_label="#ID")
