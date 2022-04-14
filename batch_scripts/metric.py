from optparse import OptionParser
from ztf_pipeutils.ztf_util import checkDir
from ztf_pipeutils.ztf_batch import BatchIt
import glob

parser = OptionParser()


parser.add_option('--input_dir', type=str, default='/sps/ztf/users/gris/pixelized_newformat',
                  help='folder directory name [%default]')
parser.add_option('--output_dir', type=str, default='/sps/ztf/users/gris/metricOutput/cadenceMetric',
                  help='output directory [%default]')
parser.add_option('--metric', type=str, default='CadenceMetric',
                  help='metric name [%default]')
parser.add_option('--nproc', type=int, default=8,
                  help='number of procs for multiprocessing [%default]')

opts, args = parser.parse_args()

input_dir = opts.input_dir
output_dir = opts.output_dir
metric_name = opts.metric
nproc = opts.nproc

checkDir(output_dir)

fis = glob.glob('{}/*.hdf5'.format(input_dir))

print(fis)

thescript = 'run_scripts/cadence/metric.py'
for fi in fis:
    procName = '.'.join(fi.split('/')[-1].split('.')[:-1])
    print(procName,fi.split('/')[-1])
    bb = BatchIt(processName=procName)
    params = {}
    params['fileName'] = fi.split('/')[-1]
    params['input_dir'] = input_dir
    params['outName'] =  fi.split('/')[-1].replace('data',metric_name.split('Metric')[0].lower())
    params['output_dir'] = output_dir
    params['metric'] = metric_name
    params['nproc'] = nproc
    bb.add_batch(thescript,params)
    bb.go_batch()
