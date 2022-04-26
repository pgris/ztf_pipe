from optparse import OptionParser
from ztf_pipeutils.ztf_util import make_dict_from_config, make_dict_from_optparse
import ztf_simfit_input as simfit_input
import pandas as pd
import os


def loadData(theDir, theFile):
    """
    function to load data

    Parameters
    ---------------
    theDir: str
      location dir of the data
    theFile: str
      name of the file to load

    Returns
    ----------
    pandas df of the data


    """

    fullPath = os.path.join(theDir, theFile)
    data = pd.read_hdf(fullPath)

    return data


# get all possible simulation parameters and put in a dict
path = list(simfit_input.__path__)
confDict = make_dict_from_config(path[0], 'config_simu_pixels.txt')

parser = OptionParser()
# parser : 'dynamical' generation
for key, vals in confDict.items():
    vv = vals[1]
    if vals[0] != 'str':
        vv = eval('{}({})'.format(vals[0], vals[1]))
    parser.add_option('--{}'.format(key), help='{} [%default]'.format(
        vals[2]), default=vv, type=vals[0], metavar='')

opts, args = parser.parse_args()

# load observations
cadData = loadData(opts.cadDir, opts.cadFile)

# load observations
obsData = loadData(opts.obsDir, opts.obsFile)

print(cadData)
print(obsData)

# loop on pixels

for i, selcad in cadData.iterrows():
    hpix = int(selcad['healpixID'])
    time_min = selcad['time_min']
    time_max = selcad['time_max']
    print('hello', str(hpix))
    # select observations for this pixel
    seldata = obsData[obsData['healpixID'].str.contains(str(hpix))]
    print(len(seldata))
    # select obs corresponding to (time_min, time_max)
    idx = seldata['time'] >= time_min
    idx &= seldata['time'] <= time_max
    seldata = seldata[idx]
    print(len(seldata))
    break
