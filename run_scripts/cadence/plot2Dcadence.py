import pandas as pd
from optparse import OptionParser
import matplotlib.pylab as plt
import matplotlib as mpl
import os
from ztf_cadence.ztf_metrics.plot_metric_for_cadence import PlotCAD
import numpy as np
import matplotlib.colors as colors

parser = OptionParser()

parser.add_option('--nside', type=int, default=128)
parser.add_option('--outDir', type=str, default='plot_cadence/2D_map/cadence',
                  help='output directory name [%default]')

parser.add_option('--input_dir', type=str, default='ztf_pixelized',
                  help='folder directory name [%default]')

parser.add_option('--title', type=str, default='', help='title [%default]')
parser.add_option('--inum', type=int, default=1)

opts, args = parser.parse_args()

nside = opts.nside
outDir = opts.outDir

input_dir = opts.input_dir
title = opts.title
inum = opts.inum

tab = pd.DataFrame()
for filename in os.listdir(input_dir):
    print(filename)
    tab_file = pd.read_hdf('{}/{}'.format(input_dir, filename))
    tab = pd.concat([tab, tab_file])
    
tab = tab[tab['ebvofMW']<0.25]

clnm = ['cad_all','cad_ztfg','cad_ztfr','cad_ztfi']

min_tab = [0.001 ]*len(clnm)
var = list(tab['season'].unique())
var.append('all')

cl = PlotCAD(outDir=outDir)

for c in clnm: 
    print(c)
    fig1 = cl.visu(tab=tab, vardisp=c, healpixId='healpixID', title=c, inum=inum, save=False, cbar=False)
    for i in range(1, len(var)):
        print('S_',i)
        fig2 = cl.visu(tab=tab[tab['season']==i], vardisp=c, healpixId='healpixID', title=c+' S{}'.format(i), 
                       inum=inum, save=False, cbar=False)
      
    




