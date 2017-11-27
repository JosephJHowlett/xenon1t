# Takes in pandas dataframe (cuts applied), makes histogram
# with user set binning in range in whichever space, and
# optionally outputs a bbf-formatted json template

import pandas as pd
import numpy as np
import time
import json
import sys
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
from matplotlib.ticker import LogLocator

input_df_filename = '/project2/lgrandi/feigao/ac_data/SR1/rn220_sr1_df_bandfit_6.8.0.pkl'
output_json_filename = 'ACBackground_Rn_cS1_cS2_SR1.json'
description_string = 'Anomalous flat component, transformed into cs2 vs cs1 space for plotting'
plot = True
save_to_json = False

# set histogram bins and range
xbins = 400
xhrange = [0.0, 100.0]
ybins = 500
yhrange = [0.0, 1.0e4]

# define space
xname = 'cs1'
yname = 'cs2'



x = pd.read_pickle(input_df_filename)


hrange = (xhrange, yhrange)
bins = [xbins, ybins]
xstepsize = (xhrange[1] - xhrange[0])/float(xbins)
ystepsize = (yhrange[1] - yhrange[0])/float(ybins)

fig = plt.figure(figsize=(10,12))
plt.hist2d(x[xname], x[yname], norm=LogNorm(), bins=(xbins, ybins), range=(xhrange, yhrange))

bin_edges = np.array([
                        np.linspace(xhrange[0], xhrange[1], xbins+1),
                        np.linspace(yhrange[0], yhrange[1], ybins+1),
                    ])


plt.hist(x[xname], bins=xbins, range=xhrange, histtype='step', normed=True)
plt.yscale('log')
plt.xlabel(xname)
plt.ylabel(yname)
plt.show()

if plot:
    sys.exit()

hist, xedges, yedges = np.histogram2d(x[xname], x[yname], bins=bins, range=hrange, normed=True)
area = (yedges[1]-yedges[0])*(xedges[1]-xedges[0])
# Normalize hist to unity
hist *= area

# get lowest/highest bin centers for Qing's formatting
xcenterbounds = [xhrange[0] + (xstepsize/2.0), xhrange[1] - (xstepsize/2.0)]
ycenterbounds = [yhrange[0] + (ystepsize/2.0), yhrange[1] - (ystepsize/2.0)]

# dict to go to json
x = {
        'description': description_string,
        'map': hist.tolist(),
        'time': time.time(),
        'name': output_json_filename.split('.json')[0],
        'coordinate_system': [[xname, xcenterbounds + [xbins]], [yname, ycenterbounds + [ybins]]],
    }

if save_to_json:
    with open(output_json_filename, 'w') as f:
        json.dump(x, f)
