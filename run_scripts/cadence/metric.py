import pandas as pd
from optparse import OptionParser
from ztf_metrics.metricWrapper import processMetric_multiproc
from ztf_pipeutils.ztf_util import checkDir

parser = OptionParser()

parser.add_option('--fileName', type=str, default='data_36.0_72.0.hdf5',
                  help='meta data file name [%default]')
parser.add_option('--input_dir', type=str, default='pixelized_newformat',
                  help='folder directory name [%default]')
parser.add_option('--outName', type=str, default='cadenceMetric_36.0_72.0.hdf5',
                  help='output file name [%default]')
parser.add_option('--output_dir', type=str, default='metricOutput/cadenceMetric',
                  help='output directory [%default]')
parser.add_option('--metric', type=str, default='CadenceMetric',
                  help='metric name [%default]')
parser.add_option('--nproc', type=int, default=8,
                  help='number of procs for multiprocessing [%default]')

opts, args = parser.parse_args()

fileName = opts.fileName
input_dir = opts.input_dir
outName = opts.outName
output_dir = opts.output_dir
metric_name = opts.metric
nproc = opts.nproc

df = pd.read_hdf('{}/{}'.format(input_dir, fileName))

resdf = processMetric_multiproc(metric_name, df[:10000], nproc)

checkDir(output_dir)
fName = '{}/{}'.format(output_dir, outName)
resdf.to_hdf(fName, key='metric')
print(resdf)
