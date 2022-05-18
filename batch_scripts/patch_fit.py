import glob
import os
from optparse import OptionParser
import warnings
warnings.filterwarnings("ignore", category=RuntimeWarning)

parser = OptionParser()

parser.add_option('--script', type=str, default='run_scripts/fit_lc/run_fit_lc.py',
                  help='script to run [%default]')
parser.add_option('--nproc', type=int, default=8,
                  help='number of procs for multiprocessing [%default]')
parser.add_option('--metaDirInput', type=str, default='infoLC',
                  help='metadata dir input[%default]')
parser.add_option('--metaDirOutput', type=str, default='fitLC',
                  help='output dir for processed data[%default]')
parser.add_option('--metaPrefix', type=str, default='meta_info_36.0_72.0',
                  help='prefix for metadata files[%default]')

opts, args = parser.parse_args()

script = 'python {}'.format(opts.script)

metaDirInput = opts.metaDirInput
metaDirOutput = opts.metaDirOutput
meta_prefix = opts.metaPrefix
nproc = 8

search_path = '{}/{}*.hdf5'.format(metaDirInput, meta_prefix)
print(search_path)
fis = glob.glob(search_path)

for fi in fis:
    metaFileInput = fi.split('/')[-1]
    metaFileOutput = metaFileInput.replace('info', 'fit')
    cmd = '{}'.format(script)
    cmd += ' --metaDirInput {}'.format(metaDirInput)
    cmd += ' --metaFileInput {}'.format(metaFileInput)
    cmd += ' --metaDirOutput {}'.format(metaDirOutput)
    cmd += ' --metaFileOutput {}'.format(metaFileOutput)
    cmd += ' --nprocFit {}'.format(nproc)
    print(cmd)
    os.system(cmd)
