#test for bagpipes, to mess around with basic functionality & get to grips with the software

#import modules
import bagpipes as pipes
import numpy as np
import random

#import filters
filt_list = np.loadtxt("filters/goodss_filt_list.txt", dtype="str")

#set up dictionary for use
model_components = {}
model_components["redshift"] = random.uniform(0.3, 0.9)
model_components["t_bc"] = 0.01
model_components["veldisp"] = 0.

#creates history component (tophat formation from 10.7gyr-6.4gyr)
constant = {}
constant["age_max"] = 10.7
constant["age_min"] = 6.4
constant["massformed"] = 8.7
constant["metallicity"] = 0.3
model_components["constant"] = constant

dust = {}
dust["type"] = "Cardelli"
dust["Av"] = 0.3
model_components["dust"] = dust

model = pipes.model_galaxy(model_components, filt_list=filt_list)
fig = model.plot()
fig = model.sfh.plot()
