from loaddata import load_goodss
import bagpipes as pipes
import numpy as np

def getfitinstructions():
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

    return fit_instructions

def fitmodel(ID, saveplot=False):
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

    if saveplot==True:
        fig = fit.plot_spectrum_posterior(save=True, show=False) #####doesnt work, unclear why
        fig = fit.plot_sfh_posterior(save=True, show=False)
        fig = fit.plot_corner(save=True, show=False)
        fig = fit.plot_1d_posterior(save=True, show=False)
    else:
        fig = fit.plot_spectrum_posterior(save=False, show=True) #####doesnt work, unclear why
        fig = fit.plot_sfh_posterior(save=False, show=True)
        fig = fit.plot_corner(save=False, show=True)
        fig = fit.plot_1d_posterior(save=False, show=True)

def fitcatmodel(ID, run):
    filt_list = np.loadtxt("filters/goodss_filt_list.txt", dtype="str")

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
    #fit_instructions = getfitinstructions()

    fit_cat = pipes.fit_catalogue(ID, fit_instructions, load_goodss,\
     spectrum_exists=False, cat_filt_list=filt_list, run=run, make_plots=True)
    fit_cat.fit(verbose=False)
