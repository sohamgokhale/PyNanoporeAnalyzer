import matplotlib as mpl
from Blocks import baseline, event, load_data, filters, signal_utils, visualiser
# Mapping between block types and their corresponding classes
block_classes = {
    'nanoporeData': load_data.ABF_Data,
    'ButterworthLPF': filters.ButterworthLPF,
    'BesselLPF': filters.BesselLPF,
    'BaselineMovMean': baseline.BaselineMovMean,
    'SubtractAndFlip': signal_utils.SubtractAndFlip,
    'EventDetect': event.EventDetect,
    'Scatterplot': visualiser.Scatterplot,
    'TimePlot': visualiser.TimePlot,
    'FFTPlot': visualiser.FFTPlot,
    'Histogram': visualiser.Histogram,
    'SigFFT': signal_utils.sigFFT,
    'DensityPlot': visualiser.DensityPlot,
    'ContourPlot': visualiser.ContourPlot
}


# Colourblind barrier-free palette - 
# Masataka Okabe, Kei Ito (2008) [https://jfly.uni-koeln.de/color/]

colors = {
    'blue': (0, 114, 178),
    'orange': (230, 159, 0),
    'sky_blue': (86, 180, 233),
    'green': (0, 158, 115),
    'yellow': (240, 228, 66),
    'red': (213, 94, 0),
    'purple': (204, 121, 167),
    'black': (0, 0, 0)
}

# Convert the RGB values to the range [0, 1]
colors = {name: (r / 255, g / 255, b / 255)
          for name, (r, g, b) in colors.items()}

# Set the color cycle for line and marker colors
mpl.rcParams['axes.prop_cycle'] = mpl.cycler(color=colors.values())
