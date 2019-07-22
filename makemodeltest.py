#test for bagpipes to mess around with basic functions & get to grips with it

#import modules
import bagpipes as pipes
import numpy as np
import random

#import filters
filt_list = np.loadtxt("filters/goodss_filt_list.txt", dtype="str")

#set up dictionary for use
model_components = {}
model_components["redshift"] = .4
#model_components["t_bc"] = 0.01
#model_components["veldisp"] = 0.

i = 0
while i == 0:
    modeltype = str(input("Input the type of model you wish to run: "))
    if modeltype == "constant":
        constant = {}
        constant["age_max"] = 6.
        constant["age_min"] = 4.
        constant["massformed"] = 1.
        constant["metallicity"] = 0.0001
        model_components["constant"] = constant
        i +=1
    elif modeltype == "burst":
        burst = {}
        burst["age"] = 6.
        burst["massformed"] = 1.
        burst["metallicity"] = 0.0001
        model_components["burst"] = burst
        i +=1
    elif modeltype == "exp":
        exp = {}
        exp["age"] = 6.
        exp["tau"] = 4.
        exp["massformed"] = 1.
        exp["metallicity"] = 0.0001
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
#model_components["dust"] = dust

print(model_components)

model = pipes.model_galaxy(model_components, filt_list=filt_list)
print(model.photometry)
fig = model.sfh.plot()
fig = model.plot()
