from loaddata import load_goodss
from loaddata import load_vandels_spec
import bagpipes as pipes
import numpy as np

filt_list = np.loadtxt("filters/goodss_filt_list.txt", dtype="str")

exp = {}
exp["age"] = (0.1,15.)
exp["tau"] = (0.3, 12.)
exp["massformed"] = (2., 15.)
exp["metallicity"] = (0.01, 2.5)

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
fit_instructions["dblplaw"] = dblplaw
fit_instructions["dust"] = dust
fit_instructions["t_bc"] = 0.01
fit_instructions["nebular"] = nebular

IDs = np.arange(1, 6001)
fit_cat = pipes.fit_catalogue(IDs, fit_instructions, load_goodss,\
 spectrum_exists=False, cat_filt_list=filt_list, run="guo_v2")
fit_cat.fit(verbose=False)
