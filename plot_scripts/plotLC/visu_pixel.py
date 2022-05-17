from optparse import OptionParser
from ztf_pipeutils.ztf_hdf5 import Read_LightCurve
import matplotlib.pyplot as plt
import numpy as np

parser = OptionParser()

parser.add_option('--meta_fileName', type=str, default='Meta_fit.hdf5',
                  help='meta data file name [%default]')
parser.add_option('--input_dir', type=str, default='dataLC',
                  help='folder directory name [%default]')

opts, args = parser.parse_args()

metaFileName = opts.meta_fileName
inputDir = opts.input_dir

data = Read_LightCurve(file_name=metaFileName, inputDir=inputDir)
metadata = data.get_table(path='meta')
print(metadata)

idx = metadata['fitstatus'] == 'fitok'
sel = metadata[idx]

print(sel.columns)
for hpix, season in np.unique(sel['healpixID', 'season']):
    ia = sel['healpixID'] == hpix
    ia &= sel['season'] == season
    selb = sel[ia]
    fig, ax = plt.subplots()
    ax.plot(selb['z'], selb['c_err'], 'ko')
    plt.show()
