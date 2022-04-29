from ztf_simfit_plot.plot_histo import Histo
from optparse import OptionParser
from bokeh.plotting import figure, output_file, save, show
import matplotlib.pylab as plt

parser = OptionParser()

parser.add_option('--meta_fileName', type=str, default='Meta_fit.hdf5',
                  help='meta data file name [%default]')
parser.add_option('--input_dir', type=str, default='dataLC',
                  help='folder directory name [%default]')
parser.add_option('--var', type=str, default='z',
                  help='Variable whose histogram you want to see [%default]')
parser.add_option('--bins', type=int, default=60,
                  help='bins for the histogram [%default]')
parser.add_option('--plot_width', type=int, default=800,
                  help='histo width [%default]')
parser.add_option('--plot_height', type=int, default=600,
                  help='histo height [%default]')
parser.add_option('--x_range_min', type=float, default=0.0,
                  help='x range min [%default]')
parser.add_option('--x_range_max', type=float, default=0.2,
                  help='x range max [%default]')
parser.add_option('-v', action="store_true", dest="verbose",
                  default=True, help='plot histo with matplotlib [%default]')
parser.add_option("-q", action="store_false", dest="verbose",
                  help='plot histo with bokeh [%default]')

opts, args = parser.parse_args()

meta_fileName = opts.meta_fileName
input_dir = opts.input_dir
var = opts.var
bins = opts.bins
plot_width = opts.plot_width
plot_height = opts.plot_height
x_range_min = opts.x_range_min
x_range_max = opts.x_range_max

cl = Histo(metaFitInput=meta_fileName, inputDir=input_dir)

if opts.verbose:
    print('Plot with matplotlib')
    cl.histo_plt(x=var, bins=bins, range=(x_range_min, x_range_max))
    plt.show()
else:
    print('Plot with bokeh')
    output_file(filename="histo.html", title='histo')
    pl = cl.histo_bokeh(x=var, bins=bins, density=True, plot_width=plot_width, plot_height=plot_height,
                        x_range=(x_range_min, x_range_max))
