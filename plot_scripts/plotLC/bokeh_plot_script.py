from ztf_simfit_plot.bokeh_plot_test import Bokeh_plot
from optparse import OptionParser
from bokeh.plotting import figure, output_file, save, show

parser = OptionParser()

parser.add_option('--meta_fileName', type=str, default='Meta_fit.hdf5',
                  help='meta data file name [%default]')
parser.add_option('--input_dir', type=str, default='dataLC',
                  help='folder directory name [%default]')
parser.add_option('--xlim', type=float, default=0.0,
                  help='x lim for plot [%default]')
parser.add_option('--ylim', type=float, default=0.1,
                  help='y lim for plot [%default]')
parser.add_option('--y_range_inf', type=float, default=0.0,
                  help='y range inf for figure [%default]')
parser.add_option('--y_range_sup', type=float, default=0.1,
                  help='y range sup for figure [%default]')
parser.add_option('--plot_width', type=int, default=800,
                  help='y range sup for figure [%default]')
parser.add_option('--plot_height', type=int, default=600,
                  help='y range sup for figure [%default]')
parser.add_option('-v', action="store_true", dest="verbose",
                  default=True, help='plot the plot1 [%default]')
parser.add_option("-q", action="store_false", dest="verbose",
                  help='plot the plot2 [%default]')

opts, args = parser.parse_args()

meta_fileName = opts.meta_fileName
input_dir = opts.input_dir
xlim = opts.xlim
ylim = opts.ylim
y_range_inf = opts.y_range_inf
y_range_sup = opts.y_range_sup
plot_width = opts.plot_width
plot_height = opts.plot_height

cl = Bokeh_plot(file_name=meta_fileName, inputDir=input_dir)

if opts.verbose:
    print('You have plotted figure 1')
    output_file(filename="plot1.html", title='$\sigma_{c}$ vs $z$')
    plot1 = cl.plot1()
else:
    print('You have plotted figure 2')
    output_file(filename="plot2.html",
                title='$\sigma_{c}$ vs $z$ for rg ang rgi band')
    plot2 = cl.plot2()
