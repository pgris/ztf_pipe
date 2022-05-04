from optparse import OptionParser
from astropy.table import Table, vstack
from ztf_simfit.ztf_simfit_plot.z_bins import Apply_mask, Z_bins
import matplotlib.pylab as plt

parser = OptionParser()

parser.add_option('--meta_fileName', type=str, default='Meta_fit.hdf5',
                  help='meta data file name [%default]')
parser.add_option('--input_dir', type=str, default='dataLC',
                  help='folder directory name [%default]')
parser.add_option('--output_dir', type=str, default='dataLC',
                  help='folder directory name [%default]')
parser.add_option('--output_fileName', type=str, default='Meta_z_',
                  help='output meta data file name [%default]')
parser.add_option('--zmin', type=float, default=0.01,
                  help='redshift min [%default]')
parser.add_option('--zmax', type=float, default=0.2,
                  help='redshift max [%default]')
parser.add_option('--fontsize', type=int, default=15,
                  help='fontsize for x,y label [%default]')
parser.add_option('-v', action="store_true", dest="verbose",
                  default=True, help='plot by default [%default]')
parser.add_option("-q", action="store_false", dest="verbose",
                  help='other plot [%default]')


"""
Examples
--------
You want to apply a mask to your metadata : mk = metadata['z']<0.5
    So, you put 'z' on var dictionnary.
        you put 'operator.lt' on op dictionary.
        you put '0.5' on lim dictionary.
"""
opts, args = parser.parse_args()

meta_fileName = opts.meta_fileName
output_dir = opts.output_dir
output_fileName = opts.output_fileName
input_dir = opts.input_dir
zmin = opts.zmin
zmax = opts.zmax
fontsize = opts.fontsize

if opts.verbose:
    print('plot by default : $\sigma_{c}$ vs $z$ per bin for all LC')
    CL = Z_bins(metaFitInput=meta_fileName, inputDir=input_dir)
    CL.add_data(output_dir, output_fileName+meta_fileName)
    
else:
    print(
        'other plot : $\sigma_{c}$ vs $z$ per bin for LC with r and g bands and LC with r,g and i bands')
    cl_rg = Apply_mask(metaFitInput=meta_fileName, inputDir=input_dir,
                       var={'sel': 'sel', 'c_err': 'c_err', 'zmin': 'z',
                            'zmax': 'z', 'n_i_band': 'n_i_band', 'chi2': 'chi2'},
                       op={'op sel': 'operator.eq', 'op c_err': 'operator.ne', 'op zmin': 'operator.ge',
                           'op zmax': 'operator.lt', 'op n_i_band': 'operator.eq', 'op_chi2': 'operator.lt'},
                       lim={'lim sel': 1, 'lim c_err': -1, 'lim zmin': 0.01, 'lim zmax': 0.1, 'lim n_i_band': 0,
                            'lim_chi2': 2})

    cl_rgi = Apply_mask(metaFitInput=meta_fileName, inputDir=input_dir,
                        var={'sel': 'sel', 'c_err': 'c_err', 'zmin': 'z',
                             'zmax': 'z', 'n_i_band': 'n_i_band', 'chi2': 'chi2'},
                        op={'op sel': 'operator.eq', 'op c_err': 'operator.ne', 'op zmin': 'operator.ge',
                            'op zmax': 'operator.lt', 'op n_i_band': 'operator.ne', 'op_chi2': 'operator.lt'},
                        lim={'lim sel': 1, 'lim c_err': -1, 'lim zmin': 0.01, 'lim zmax': 0.1, 'lim n_i_band': 0, 'lim_chi2': 2})

    Z_bins_rg = Z_bins(metaFitInput=meta_fileName,
                       inputDir=input_dir, dico=cl_rg.dico)
    Z_bins_rgi = Z_bins(metaFitInput=meta_fileName,
                        inputDir=input_dir, dico=cl_rgi.dico)

    Z_bins_rg.plot_err_c_z(error_bar=True, axhline=True, color='blue')
    Z_bins_rgi.plot_err_c_z(error_bar=True, color='orange')
    plt.show()

    CL = Z_bins(metaFitInput=meta_fileName, inputDir=input_dir)

    CL.plot_err_c_z(error_bar=True, axhline=True)
    plt.show()

    print('TEST HERE')
    CL.plot_interpolation1d(fill=True, add_text=True, axhline=True)
    plt.show()

    

    
