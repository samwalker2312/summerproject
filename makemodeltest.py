#test for bagpipes to mess around with basic functions & get to grips with it

#import modules
import bagpipes as pipes
import numpy as np
import random

#import filters
filt_list = np.loadtxt("filters/goodss_filt_list.txt", dtype="str")

#set up dictionary for use
model_components = {}
model_components["redshift"] = random.uniform(0.3, 10.)
model_components["t_bc"] = 0.01
model_components["veldisp"] = 0.

i = 0
while i == 0:
    modeltype = str(input("Input the type of model you wish to run: "))
    if modeltype == "constant":
        #creates history component (tophat formation from 10.7gyr-6.4gyr)
        constant = {}
        constant["age_max"] = 10.7
        constant["age_min"] = 6.4
        constant["massformed"] = 8.7
        constant["metallicity"] = 0.3
        model_components["constant"] = constant
        i +=1
    elif modeltype == "burst":
        burst = {}
        burst["age"] = 8.3
        burst["massformed"] = 8.7
        burst["metallicity"] = 0.3
        model_components["burst"] = burst
        i +=1
    elif modeltype == "exp":
        exp = {}
        exp["age"] = 3.
        exp["tau"] = 0.75
        exp["massformed"] = 9.
        exp["metallicity"] = 0.5
        model_components["exponential"] = exp
        i +=1
    elif modeltype == "delay":
        delayed = {}
        delayed["age"] = 6.
        delayed["tau"] = 0.69
        delayed["massformed"] = 9.
        delayed["metallicity"] = 0.5
        model_components["delayed"] = delayed
        i +=1
    elif modeltype == "log":
        lognormal = {}
        lognormal["tmax"] = 8.6
        lognormal["fwhm"] = 2.
        lognormal["massformed"] = 9.
        lognormal["metallicity"] = 0.3
        model_components["lognormal"] = lognormal
        i +=1
    elif modeltype == "power":
        dblplaw = {}
        dblplaw["alpha"] = 1.3
        dblplaw["beta"] = 0.8
        dblplaw["tau"] = 7.
        dblplaw["massformed"] = 9.
        dblplaw["metallicity"] = 0.5
        model_components["dblplaw"] = dblplaw
        i +=1
    else:
        print("Error! Please input one of the recognised SFH shapes.")

dust = {}
dust["type"] = "Cardelli"
dust["Av"] = 0.3
model_components["dust"] = dust

model = pipes.model_galaxy(model_components, filt_list=filt_list)
fig = model.plot()
fig = model.sfh.plot()
