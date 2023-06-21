import nanoporeData, filters, eventDetect, baselineDetect
import utils, sigUtils
import inspect

# Mapping between block types and their corresponding classes
block_classes = {
    'nanoporeData': nanoporeData.nanoporeData,
    'ButterworthLPF': filters.ButterworthLPF,
    'BaselineMovMean': baselineDetect.BaselineMovMean,
    'SubtractAndFlip': sigUtils.SubtractAndFlip,
    'EventDetect': eventDetect.EventDetect,
}

blockConfig = utils.ParseYAML("input.yaml")
blocks = {}

for blockData in blockConfig:
    blockName = blockData.get('name')
    blockType = blockData.get('type')
    blockClass = blockData.get('class')
    blockParams = blockData.get('parameters')
    for i, param in enumerate(blockParams):
        if str(param)[0] == '$':
            source_name, source_function = param[1:].split('.')
            source_instance = blocks.get(source_name)
            attr = getattr(source_instance,source_function) 
            if attr is not None:
                if inspect.isfunction(attr):
                    blockParams[i] = attr()
                else:
                    blockParams[i] = attr

    if blockClass in block_classes:
        blockCls = block_classes[blockClass]
        blockInstance = blockCls(*blockParams)
        blocks.update({blockName:blockInstance})
    else:
        print("Error in Input File")

outputs ={}

for blockData in blockConfig:
    inputList = []
    if blockData.get('type') != 'Source':
        blockInputs = blockData.get('inputs')
        for i, input in enumerate(blockInputs):
            if str(input)[0] == '$':
                source_name, source_function = input[1:].split('.')
                source_instance = blocks.get(source_name)
                attr = getattr(source_instance,source_function)
                if attr is not None:
                    if inspect.ismethod(attr):
                        inputList.append(attr())
                    else:
                        inputList.append(attr)
            else:
                inputList.append(outputs.get(input))
        print(inputList)
        block_instance = blocks.get(blockData.get('name'))
        output = block_instance.run(*inputList)
        outputs.update({blockData.get('name'):output})
