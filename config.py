from Blocks import baseline, event, load_data, filters, signal_utils, visualiser
# Mapping between block types and their corresponding classes
block_classes = {
    'nanoporeData': load_data.ABF_Data,
    'ButterworthLPF': filters.ButterworthLPF,
    'BaselineMovMean': baseline.BaselineMovMean,
    'SubtractAndFlip': signal_utils.SubtractAndFlip,
    'EventDetect': event.EventDetect,
    'Scatterplot': visualiser.Scatterplot
}
