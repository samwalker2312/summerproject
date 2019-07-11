from loaddata import load_goodss
from loaddata import load_vandels_spec
import bagpipes as pipes
import numpy as np

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

IDs = np.arange(1,6)
fit_cat = pipes.fit_catalogue(IDs, fit_instructions, load_goodss,\
 spectrum_exists=False, cat_filt_list=filt_list, run="guo")
fit_cat.fit(verbose=False)
