from optparse import OptionParser
from ztf_pipeutils.ztf_util import make_dict_from_config, make_dict_from_optparse
import ztf_simfit_input as simfit_input
from ztf_pipeutils.ztf_util import multiproc, dump_in_yaml, checkDir
from ztf_pipeutils.ztf_hdf5 import Write_LightCurve
from ztf_simfit.ztf_simu import Simul_lc
import pandas as pd
import os
import copy
import numpy as np
import numpy.lib.recfunctions as rf


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


def simu(hpixels, params, j=0, output_q=None):

    hpix = hpixels[0]
    healpixID = hpix[0]
    season = hpix[1]

    params['seed'] += j
    obs = params['obsData']
    del params['obsData']
    outputDir = params['outputDirSimu']
    lcName = params['lcName']
    metaName = params['metaName']
    path_prefix = params['path_prefix']
    cadData = params['cadData']

    # lc simulation
    simlc = Simul_lc(**params)

    idx = cadData['healpixID'] == healpixID
    idx &= cadData['season'] == season
    selcad = cadData[idx]
    lc = processPixel(selcad.iloc[0], obs, simlc)

    lcName = lcName.replace('.hdf5', '_{}_{}.hdf5'.format(healpixID, season))
    metaName = metaName.replace(
        '.hdf5', '_{}_{}.hdf5'.format(healpixID, season))

    # write LC and metadata
    Write = Write_LightCurve(
        outputDir=outputDir, file_data=lcName, file_meta=metaName, path_prefix=path_prefix)

    path = '_{}_{}'.format(healpixID, season)
    Write.write_data(lc, lc.meta_rejected, add_meta=dict(
        zip(['healpixID', 'season'], [healpixID, season])), path=path)

    if output_q is not None:
        return output_q.put({j: 1})
    else:
        return 0


def processPixel(selcad, obsData, simlc):
    """
    Function to process (simul LC on) a pixel

    Parameters
    -------------
    selcad: array
      cadence data
    obsData: array
      observations
    simlc: Simul_lc instance

    Returns
    ----------


    """
    hpix = int(selcad['healpixID'])
    time_min = selcad['time_min']
    time_max = selcad['time_max']
    healpixRA = selcad['healpixRA']
    healpixDec = selcad['healpixDec']
    # select observations for this pixel
    seldata = obsData[obsData['healpixID'].str.contains(str(hpix))]
    # select obs corresponding to (time_min, time_max)
    idx = seldata['time'] >= time_min
    idx &= seldata['time'] <= time_max
    seldata = seldata[idx]
    ra_range = (healpixRA, healpixRA)
    dec_range = (healpixDec, healpixDec)
    seldata['ra'] = healpixRA
    seldata['dec'] = healpixDec
    # lc simulation
    lc = simlc(seldata, ra_range, dec_range)
    return lc


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

# load the new values
params = {}
for key, vals in confDict.items():
    newval = eval('opts.{}'.format(key))
    # params[key] = (vals[0], newval)
    params[key] = newval
print(params)

if params['ztfdataDir'] == 'default':
    import ztf_data as ztf_data
    path = list(ztf_data.__path__)
    params['ztfdataDir'] = path[0]

ntransient = params['ntransient']
nproc = params['nprocSimu']
params['z_range'] = (params['zmin'], params['zmax'])
outputDir = params['outputDirSimu']
lcName = params['lcName']
metaName = params['metaName']
path_prefix = params['path_prefix']

# dump script parameters in yaml file
checkDir(outputDir)
nameOut = metaName.replace('.hdf5', '.yaml')
dump_in_yaml(opts, confDict, outputDir, nameOut, 'simu')

# load observations
cadData = loadData(opts.cadDir, opts.cadFile)

# load observations
obsData = loadData(opts.obsDir, opts.obsFile)

print(cadData)
print(obsData)
params['obsData'] = obsData
params['cadData'] = cadData
if __name__ == '__main__':
    ffi = np.unique(cadData[['healpixID', 'season']].to_records(index=False))
    to = list(map(lambda *x: x, *([iter(ffi)] * nproc)))
    for tt in to:
        lc_dict = multiproc(tt, params, simu, nproc, gather=False)
