from loaddata import load_goodss
from loaddata import load_vandels_spec
import bagpipes as pipes
import numpy as np

filt_list = np.loadtxt("filters/goodss_filt_list.txt", dtype="str")

galaxy = pipes.galaxy(14697,load_goodss,spectrum_exists=False,filt_list=filt_list)

dust = {}
dust["type"] = "Cardelli"
dust["Av"] = (0.,2.)

power = {}
power["tau"] = (0., 15.)
power["alpha"] = (.1, 1000.)
power["beta"] = (.1, 1000.)
power["alpha_prior"] = "log_10"
power["beta_prior"] = "log_10"
power["massformed"] = (2., 15.)
power["metallicity"] = (0., 2.5)

secondfit = {}
secondfit["redshift"] = (0.,10.)
secondfit["dblplaw"] = power
secondfit["dust"] = dust
fit = pipes.fit(galaxy, secondfit, run="dblplaw_sfh")
fit.fit(verbose=False)
fig = fit.plot_sfh_posterior(save=False, show=True)
fig = fit.plot_corner(save=False, show=True)
