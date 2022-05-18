import glob
import os
from optparse import OptionParser

parser = OptionParser()

parser.add_option('--obsDir', type=str, default='/sps/ztf/users/gris/pixelized_newformat',
                  help='dir with observations [%default]')

opts, args = parser.parse_args()


fis = glob.glob('{}/data*.hdf5'.format(opts.obsDir))
for fi in fis:
    obsFile = fi.split('/')[-1]
    cmd = 'python batch_scripts/patch_simu.py'
    cmd += ' --obsFile {}'.format(obsFile)

    print(cmd)
    os.system(cmd)
