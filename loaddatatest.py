from loaddata import load_goodss
from loaddata import load_vandels_spec
import bagpipes as pipes
import numpy as np

filt_list = np.loadtxt("filters/goodss_filt_list.txt", dtype="str")

photogalaxy = pipes.galaxy("14697", load_goodss, spectrum_exists=False, filt_list=filt_list)
fig1 = photogalaxy.plot()

specgalaxy = pipes.galaxy("017433", load_vandels_spec, photometry_exists = False)
fig2 = specgalaxy.plot()
