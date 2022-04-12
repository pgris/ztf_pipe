import pandas as pd
from optparse import OptionParser

from ztf_metrics.metric import CadenceMetric, read

parser = OptionParser()

parser.add_option('--fileName', type=str, default='data_36.0_72.0.hdf5',
                  help='meta data file name [%default]')
parser.add_option('--input_dir', type=str, default='ztf_pixelized',
                  help='folder directory name [%default]')


opts, args = parser.parse_args()

fileName = opts.fileName
input_dir = opts.input_dir

print(read(input_dir,fileName))