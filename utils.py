import yaml

def ParseYAML(path):

    with open(path,'r') as file:
        inputData = yaml.safe_load(file)

    block_configuration = []

    for block in inputData.keys():
        if(block != 'Connections'):
            dict1 ={"name":block}
            dict1.update(dict(inputData[block]))
            try:
                dict1.update({"parameters":decodeParams(dict1)})
            except TypeError:
                print("Could not find parameters for " + dict1.get('name'))
                dict1.update({"parameters":[]})
            block_configuration.append(dict1)

    return (block_configuration)

def decodeParams(block :dict) -> list:
    blockParams = []
    for Params in block.get('parameters'):
        blockParams.append(*Params.values())
    return blockParams
