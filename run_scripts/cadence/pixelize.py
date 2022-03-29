import matplotlib.pyplot as plt
from ztf_pipeutils.ztf_util import make_dict_from_config, make_dict_from_optparse
import ztf_cadence_input as cadence_input
from ztf_cadence.pixelize import Pixelize_sky
from ztf_cadence.align_quadrant import align_quad
from ztf_pipeutils.ztf_util import multiproc
from optparse import OptionParser
import pandas as pd


def multipix(data, params={}, j=0, output_q=None):
    """
    Function to perfom sky pixelizing
    with the possibility to use multiprocessing

    Parameters
    ----------------
    data : astropy table
       array of data to process
    params: dict
      parameters of the function
    j: int, opt
      tag for multiprocessing (default: 0)
    output_q: multiprocessing.queue,opt
      queue for multiprocessing

    Returns
    ----------
    resfit: astropy table
      result of the fit
    """
    pixelize_it = Pixelize_sky(
        params['nside'], raCol=params['raCol'], decCol=params['decCol'])

    # now process

    print('processing', j, len(data))
    dfOut = pixelize_it(data)

    if output_q is not None:
        return output_q.put({j: dfOut})
    else:
        return 0


# get all possible simulation parameters and put in a dict
path = list(cadence_input.__path__)
confDict = make_dict_from_config(path[0], 'config_pixelize.txt')

parser = OptionParser()
# parser : 'dynamical' generation
for key, vals in confDict.items():
    vv = vals[1]
    if vals[0] != 'str':
        vv = eval('{}({})'.format(vals[0], vals[1]))
    parser.add_option('--{}'.format(key), help='{} [%default]'.format(
        vals[2]), default=vv, type=vals[0], metavar='')

opts, args = parser.parse_args()

# load the new values
params = {}
for key, vals in confDict.items():
    newval = eval('opts.{}'.format(key))
    params[key] = newval

print(params)

# get log of observations
logObs = params['logObs']
print('loading', logObs)
df_obs = pd.read_csv(logObs)

# first thing to do : re-align quadrant centers
pp = {}
pp['obs'] = df_obs


# align quadrants
df_obs_quad = multiproc(df_obs['field'].unique(), pp, align_quad, opts.nproc)

params = {}
params['nside'] = opts.nside
params['raCol'] = 'ra_quad'
params['decCol'] = 'dec_quad'

# pixelize the data
dfOut = multiproc(df_obs_quad[:90000], params, multipix, opts.nproc)

dfOut.to_hdf(opts.outFile, key='obs')
