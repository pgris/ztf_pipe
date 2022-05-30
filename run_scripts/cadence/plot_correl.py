from optparse import OptionParser
from ztf_metrics import plt
from ztf_metrics.plotUtils import loadData, binnedData
import numpy as np
import pandas as pd

parser = OptionParser()

parser.add_option('--cadenceDir', type=str, default='../metricOutput/cadenceMetric',
                  help='cadence metric directory files [%default]')
parser.add_option('--zcompleteDir', type=str, default='metricOutput/zcomplete',
                  help=' zcomplete metric directory files [%default]')

opts, args = parser.parse_args()

cadenceDir = opts.cadenceDir
zcompDir = opts.zcompleteDir

cadenceData = loadData(cadenceDir)
zcompData = loadData(zcompDir)
print(cadenceData)
print(zcompData)

dataCorr = zcompData.merge(cadenceData, left_on=[
                           'healpixID', 'season'], right_on=['healpixID', 'season'])

idx = dataCorr['zlim'] > 0.
idx &= dataCorr['cad_all'] <= 5.
dataCorr = dataCorr[idx]
print(dataCorr.columns)


io = dataCorr['nb_obs_ztfi'] < 1
sela = dataCorr[io]
selb = dataCorr[~io]

bins = np.arange(0.75, 5.25, 0.5)

bba = binnedData(sela, bins, 'cad_all', 'zlim')
bbb = binnedData(selb, bins, 'cad_all', 'zlim')

fig, ax = plt.subplots(figsize=(10, 8))

ax.plot(bba['cad_all'], bba['zlim'], color='k',
        marker='o', mfc='None', label='$gr$')
ax.fill_between(bba['cad_all'], bba['zlim']+bba['zlim_std'],
                bba['zlim']-bba['zlim_std'], color='gray', alpha=0.5)
ax.plot(bbb['cad_all'], bbb['zlim'], color='k',
        marker='o', lineStyle='dashed', mfc='None', label='$gri$')
ax.fill_between(bbb['cad_all'], bbb['zlim']+bbb['zlim_std'],
                bbb['zlim']-bbb['zlim_std'], color='yellow', alpha=0.5)
ax.grid()
ax.set_xlim([0.9, 4])
ax.set_xlabel('cadence [days]')
ax.set_ylabel('<$z_{complete}$>')
ax.legend(frameon=False)
plt.show()
