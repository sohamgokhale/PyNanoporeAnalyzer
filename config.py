import nanoporeData, filters, eventDetect, baselineDetect, sigUtils
# Mapping between block types and their corresponding classes
block_classes = {
    'nanoporeData': nanoporeData.nanoporeData,
    'ButterworthLPF': filters.ButterworthLPF,
    'BaselineMovMean': baselineDetect.BaselineMovMean,
    'SubtractAndFlip': sigUtils.SubtractAndFlip,
    'EventDetect': eventDetect.EventDetect,
}
