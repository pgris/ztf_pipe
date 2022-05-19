import glob
import os
from optparse import OptionParser

parser = OptionParser()

parser.add_option('--obsDir', type=str, default='/sps/ztf/users/gris/pixelized_newformat',
                  help='dir with observations [%default]')
parser.add_option('--outputDirSimu',type=str,default='/sps/ztf/users/gris/dataLC', help='output dir for simulation [/%default]')

opts, args = parser.parse_args()


fis = glob.glob('{}/data*.hdf5'.format(opts.obsDir))
for fi in fis:
    obsFile = fi.split('/')[-1]
    cmd = 'python batch_scripts/patch_simu.py'
    cmd += ' --obsFile {}'.format(obsFile)
    cmd += ' --outputDirSimu {}'.format(opts.outputDirSimu)

    print(cmd)
    os.system(cmd)
