from optparse import OptionParser
from ztf_util import make_dict_from_config, make_dict_from_optparse
from ztf_simu import Simul_lc
from ztf_hdf5 import Write_LightCurve
from ztf_util import multiproc, dump_in_yaml, checkDir
from astropy.table import Table, vstack


def simu(index, params, j=0, output_q=None):

    params['ntransient'] = index[0]
    params['seed'] += j

    # lc simulation
    lc = Simul_lc(**params)()
    if output_q is not None:
        return output_q.put({j: lc})
    else:
        return 0


# get all possible simulation parameters and put in a dict
#path = simu_fit.__path__
confDict = make_dict_from_config('ztf_stage/script/simu', 'config_simu.txt')

parser = OptionParser()
# parser : 'dynamical' generation
for key, vals in confDict.items():
    vv = vals[1]
    if vals[0] != 'str':
        vv = eval('{}({})'.format(vals[0], vals[1]))
    parser.add_option('--{}'.format(key), help='{} [%default]'.format(
        vals[2]), default=vv, type=vals[0], metavar='')

opts, args = parser.parse_args()

print('Start processing...')

# load the new values
params = {}
for key, vals in confDict.items():
    newval = eval('opts.{}'.format(key))
    #params[key] = (vals[0], newval)
    params[key] = newval
print(params)

ntransient = params['ntransient']
nproc = params['nprocSimu']
params['z_range'] = (params['zmin'], params['zmax'])
params['ra_range'] = (params['ramin'], params['ramax'])
params['dec_range'] = (params['decmin'], params['decmax'])
outputDir = params['outputDirSimu']
lcName = params['lcName']
metaName = params['metaName']
path_prefix = params['path_prefix']

# dump script parameters in yaml file
checkDir(outputDir)
nameOut = metaName.replace('.hdf5', '.yaml')
dump_in_yaml(opts, confDict, outputDir, nameOut, 'simu')

if __name__ == '__main__':
    step = int(ntransient/nproc)
    ffi = [step]*nproc
    lc_dict = multiproc(ffi, params, simu, nproc, gather=False)

    # write LC and metadata
    Write = Write_LightCurve(
        outputDir=outputDir, file_data=lcName, file_meta=metaName, path_prefix=path_prefix)
    rlc = []
    meta_rejected = Table()
    for i, lcl in lc_dict.items():
        if lcl.meta_rejected is not None:
            meta_rejected = vstack([meta_rejected, Table(lcl.meta_rejected)])
        for lc in lcl:
            rlc.append(lc)

    data = Write.write_data(rlc, meta_rejected)
