import matplotlib.pyplot as plt
from ztf_pipeutils.ztf_util import make_dict_from_config, make_dict_from_optparse
import ztf_cadence_input as cadence_input
from ztf_cadence.pixelize import Pixelize_sky, pixels, Pixel2Obs
from ztf_cadence.align_quadrant import align_quad
from ztf_pipeutils.ztf_util import multiproc
from optparse import OptionParser
import pandas as pd
import numpy as np
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

    print('result', dfOut)
    if output_q is not None:
        return output_q.put({j: dfOut})
    else:
        return 0


def pixel_to_obs(healpixels, nside, data, width_ra, width_dec, raCol, decCol, nproc):

    params['nside'] = nside
    params['data'] = data
    params['width_ra'] = width_ra
    params['width_dec'] = width_dec
    params['raCol'] = raCol
    params['decCol'] = decCol

    print('total to process per proc', len(healpixels)/nproc)
    res = multiproc(healpixels[:400], params, multipixel_obs, nproc)

    return res


def multipixel_obs(ppix, params={}, j=0, output_q=None):

    nside = params['nside']
    df_obs = params['data']
    width_ra = params['width_ra']
    width_dec = params['width_dec']
    raCol = params['raCol']
    decCol = params['decCol']

    print('to process', len(ppix))
    ppo = Pixel2Obs(nside, df_obs, width_ra,
                    width_dec, raCol=raCol, decCol=decCol)
    import time
    dtot = pd.DataFrame()
    time_ref = time.time()
    for ih, healpix in enumerate(ppix):
        dp = ppo(healpix)
        dtot = pd.concat((dtot, dp))

        if ih % 10 == 0:
            print('processed', ih, time.time()-time_ref)

    print('pproc', time.time()-time_ref)

    if output_q is not None:
        return output_q.put({j: dtot})
    else:
        return dtot


def get_min_max(dd, what):

    return dd[what].min(), dd[what].max()


def alignquads(df):

    pp = {}
    pp['obs'] = df
    # align quadrants
    dfo = multiproc(df['field'].unique(), pp, align_quad, opts.nproc)
    print('aligned', len(dfo))
    dfo = dfo.sort_values(by=['time'])
    return dfo


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

ra_min, ra_max = get_min_max(df_obs, 'ra')
dec_min, dec_max = get_min_max(df_obs, 'dec')
delta_dec = dec_max-dec_min
print(ra_min, ra_max, dec_min, dec_max)

ra_min = 0.
ra_max = 36.
delta_ra = ra_max-ra_min

width_ra = 0.854
width_dec = 0.854
idx = df_obs['ra'] >= ra_min-1.05*width_ra
idx = df_obs['ra'] < ra_max+1.05*width_ra

"""
# get obs in this window
df_obs = df_obs[idx]

# get pixels in this window
ppix = pixels(opts.nside, np.mean([ra_min, ra_max]), np.mean(
    [dec_min, dec_max]), delta_ra, delta_dec)

print(ppix, len(ppix))
"""

# re-align quadrant centers - if requested

if opts.alignquads:
    df_obs = alignquads(df_obs)

 # get pixels in this window
"""
ppix = pixels(opts.nside, np.mean([ra_min, ra_max]), np.mean(
    [dec_min, dec_max]), delta_ra, delta_dec)

df = pixel_to_obs(ppix, opts.nside, df_obs, width_ra,
                  width_dec, 'ra_quad', 'dec_quad', opts.nproc)
"""
"""
pixel_to_obs = Pixel2Obs(opts.nside, df_obs, width_ra,
                         width_dec, raCol='ra_quad', decCol='dec_quad')
import time
for healpix in ppix:

    time_ref = time.time()
    dp = pixel_to_obs(healpix)
    print('pproc', healpix, time.time()-time_ref)
"""


params = {}
params['nside'] = opts.nside
params['raCol'] = 'ra'
params['decCol'] = 'dec'

if opts.alignquads:
    params['raCol'] = 'ra_quad'
    params['decCol'] = 'dec_quad'


# pixelize the data
import time
time_ref = time.time()
dfOut = multiproc(df_obs[:40000], params, multipix, opts.nproc)

print('processed', time.time()-time_ref)
#dfOut.to_hdf(opts.outFile, key='obs')
dfOut.to_parquet('df.parquet.gzip', compression='gzip')
