import numpy as np
import pandas as pd

data = np.loadtxt("uvjoutput_dblplaw_passivetest.csv", delimiter=',',usecols = (0,55,56,57))
IDs = data[:,0]
RA = data[:,1]
Dec = data[:,2]
passive = data[:,3]

mask = (passive != 0.)
ID_passive = IDs[mask]
RA = RA[mask]
Dec = Dec[mask]

array = np.array([RA, Dec]).T
columns = ['RA','Dec']
frame = pd.DataFrame(array, columns=columns, index=ID_passive)
frame.to_csv(path_or_buf='radec_passive.csv', index_label='#ID')
