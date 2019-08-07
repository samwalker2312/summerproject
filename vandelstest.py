import numpy as np

specIDs = np.loadtxt('observed_targets.cat', usecols = (0), skiprows=1079,max_rows=551, dtype='str')
photIDs = np.loadtxt('uvjoutput_dblplaw_passivetest.csv',delimiter=',', usecols = (0,57),skiprows=1, dtype='str')
passivity = photIDs[:,1]
photIDs = photIDs[:,0]
photIDs = photIDs[passivity != '0.0']
for i in range(specIDs.shape[0]):
    specIDs[i] = specIDs[i][9:14]
photIDs = photIDs.astype(float)
specIDs = specIDs.astype(float)
print(specIDs[np.isin(specIDs,photIDs)])
