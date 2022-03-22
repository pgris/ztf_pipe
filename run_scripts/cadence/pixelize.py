from ztf_pipeutils.ztf_pipeutils.ztf_util import make_dict_from_config, make_dict_from_optparse
import ztf_cadence as cadence_input
from ztf_cadence.ztf_cadence.pixelize import Pixelize_sky
from optparse import OptionParser
import pandas as pd

# get all possible simulation parameters and put in a dict
path = cadence_input.__path__
confDict = make_dict_from_config(path[0], 'script_input/config_pixelize.txt')

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

# instance of pixelize

pixelize_it = Pixelize_sky(params['nside'])

# now process

dfOut = pixelize_it(df_obs[:100])

print(dfOut)
