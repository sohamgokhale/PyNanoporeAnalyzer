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
    'DensityPlot': visualiser.DensityPlot
}
