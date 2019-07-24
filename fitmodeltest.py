from loaddata import load_goodss
from loaddata import load_vandels_spec
import bagpipes as pipes
import numpy as np

def fitmodel(ID):
    filt_list = np.loadtxt("filters/goodss_filt_list.txt", dtype="str")

    galaxy = pipes.galaxy(ID,load_goodss,spectrum_exists=False,filt_list=filt_list)

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

    fit = pipes.fit(galaxy, fit_instructions)
    fit.fit(verbose=False)

    print(np.median(fit.posterior.samples["exponential:tau"]))
    print(np.median(fit.posterior.samples["exponential:age"]))
    fig = fit.plot_spectrum_posterior(save=False, show=True) #####doesnt work, unclear why
    fig = fit.plot_sfh_posterior(save=False, show=True)
    fig = fit.plot_corner(save=False, show=True)

def fitcatmodel(ID, run):
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

    fit_cat = pipes.fit_catalogue(ID, fit_instructions, load_goodss,\
     spectrum_exists=False, cat_filt_list=filt_list, run=run)
    fit_cat.fit(verbose=False)
    fig= fit_cat.plot_spectrum_posterior(save=False, show=True)
    fig = fit_cat.plot_sfh_posterior(save=False, show=True)
    fig = fit_cat.plot_corner(save=False, show=True)
