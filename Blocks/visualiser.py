import matplotlib.pyplot as plt
from Blocks import signal_utils
import numpy as np
from scipy.stats import kde
import seaborn as sns
from palettable.scientific.sequential import Devon_20 as theme
import matplotlib.colors as colors

class Figure:
    def __init__(self) -> None:
        self.figOpt = {}
    
    def decodeOptions(self):
        for opt, val in self.figOpt.items():
            try:
                getattr(plt, opt)(val)
            except:
                print(f"Warning: Unknown option '{opt}'")


class Scatterplot(Figure):
    def __init__(self,figure_options : dict) -> None:
        self.figOpt = figure_options

    def run(self,xAxis,yAxis) -> None:
        plt.figure()
        plt.scatter(xAxis,yAxis,alpha=0.8,marker='.')
        self.decodeOptions()

class TimePlot(Figure):
    def __init__(self,figure_options : dict) -> None:
        self.figOpt = figure_options

    def run(self,xAxis,yAxis) -> None:
        plt.figure()
        plt.plot(xAxis,yAxis)
        self.decodeOptions()

class FFTPlot(Figure):
    def __init__(self,samplingTime, figure_options : dict) -> None:
        self.fft = signal_utils.sigFFT(samplingTime)
        self.figOpt = figure_options

    def run(self,signal) -> None:
        plt.figure()
        xAxis, yAxis = self.fft.run(signal)
        plt.plot(xAxis,yAxis)
        self.decodeOptions()

class Histogram(Figure):
    def __init__(self,binSize, figure_options : dict) -> None:
        self.binSize = binSize
        self.figOpt = figure_options

    def run(self,data) -> None:
        plt.figure()
        plt.hist(data, bins=np.arange(min(data), max(data) + self.binSize, self.binSize))
        self.decodeOptions()

class DensityPlot(Figure):
    def __init__(self, resolution, figure_options : dict) -> None:
        self.bins = resolution
        self.figOpt = figure_options
        
    def run(self, xAxis, yAxis):
        xAxis = np.array(xAxis)
        yAxis = np.array(yAxis)
        k = kde.gaussian_kde([xAxis , yAxis])
        xi, yi = np.mgrid[xAxis.min():xAxis.max():self.bins*1j,yAxis.min():yAxis.max():self.bins*1j]
        zi = k(np.vstack([xi.flatten(), yi.flatten()]))

        plt.figure()
        plt.pcolormesh(xi, yi, zi.reshape(xi.shape), shading='nearest', cmap=theme.mpl_colormap.reversed())
        plt.colorbar()
        self.decodeOptions()

class ContourPlot(Figure):
    def __init__(self, figure_options : dict) -> None:
        self.figOpt = figure_options
        
    def run(self, xAxis, yAxis):
        xAxis = np.array(xAxis)
        yAxis = np.array(yAxis)
        sns.kdeplot(x=xAxis, y=yAxis, cmap=theme.mpl_colormap.reversed(), fill=True)
        self.decodeOptions()