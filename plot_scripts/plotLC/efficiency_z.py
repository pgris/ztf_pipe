from optparse import OptionParser
from astropy.table import Table, vstack
from ztf_simfit_plot.efficiency import Efficiency
import matplotlib.pylab as plt

parser = OptionParser()

parser.add_option('--meta_fileName', type=str, default='Meta_fit.hdf5',
                  help='meta data file name [%default]')
parser.add_option('--input_dir', type=str, default='dataLC',
                  help='folder directory name [%default]')


opts, args = parser.parse_args()

meta_fileName = opts.meta_fileName
input_dir = opts.input_dir

cl = Efficiency(meta_Input=meta_fileName, inputDir=input_dir)
cl.z_efficiency()
plt.show()
