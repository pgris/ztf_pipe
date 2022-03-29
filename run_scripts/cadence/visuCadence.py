import matplotlib.pyplot as plt
import ztf_cadence_input as cadence_input
from ztf_pipeutils.ztf_util import make_dict_from_config
from ztf_cadence.plot_cadence import PlotNights
from optparse import OptionParser
import pandas as pd
import healpy as hp


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
confDict = make_dict_from_config(path[0], 'config_visucadence.txt')

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

# load observations

df = pd.read_hdf(opts.obsFile)

plot_nights = PlotNights(df, opts.nside, opts.outDir)

plot_nights(opts.displaytype)
