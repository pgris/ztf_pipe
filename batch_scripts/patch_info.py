import glob
import os
from optparse import OptionParser

parser = OptionParser()

parser.add_option('--script', type=str, default='run_scripts/info/run_info.py',
                  help='script to run [%default]')
parser.add_option('--nproc', type=int, default=8,
                  help='number of procs for multiprocessing [%default]')
parser.add_option('--metaDir', type=str, default='dataLC',
                  help='metadata dir[%default]')
parser.add_option('--outputDirInfo', type=str, default='infoLC',
                  help='output dir for processed data[%default]')
parser.add_option('--metaPrefix', type=str, default='meta_36.0_72.0',
                  help='prefix for metadata files[%default]')

opts, args = parser.parse_args()

script = 'python {}'.format(opts.script)

metaDir = opts.metaDir
outputDirInfo = opts.outputDirInfo
meta_prefix = opts.metaPrefix
nproc = opts.nproc


fis = glob.glob('{}/{}*.hdf5'.format(metaDir, meta_prefix))

for fi in fis:
    metaFile = fi.split('/')[-1]
    infoFile = metaFile.replace('meta', 'meta_info')
    cmd = '{}'.format(script)
    cmd += ' --metaDir {}'.format(metaDir)
    cmd += ' --metaFile {}'.format(metaFile)
    cmd += ' --infoFile {}'.format(infoFile)
    cmd += ' --outputDirInfo {}'.format(outputDirInfo)
    cmd += ' --nproc {}'.format(nproc)
    print(cmd)
    os.system(cmd)
