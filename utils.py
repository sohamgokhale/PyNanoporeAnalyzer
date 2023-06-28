import yaml, inspect


def ParseYAML(path):

    with open(path, 'r') as file:
        inputData = yaml.safe_load(file)

    block_configuration = []

    for block in inputData.keys():
        if (block != 'Connections'):
            dict1 = {"name": block}
            dict1.update(dict(inputData[block]))
            block_configuration.append(dict1)

    return (block_configuration)


def decodeParams(blockData: dict, blocks: dict) -> list:
    try:
        blockParams = [*blockData.get('parameters').values()]
    except:
        print("No Parameters found for ",blockData.get('name'))
        return []
    for i, param in enumerate(blockParams):
        if str(param)[0] == '$':
            blk_name, port, attribute = param[1:].split('.')
            blk_instance = blocks.get(blk_name)
            attr = getattr(blk_instance,attribute) 
            if attr is not None:
                if inspect.ismethod(attr):
                    blockParams[i] = attr()
                else:
                    blockParams[i] = attr
            else:
                print("No attibute specified")
    return blockParams

def decodeInputs(blockData: dict, blocks: dict, outputs: dict) -> list:
    try:
        blockInputs = blockData.get('inputs')
    except:
        print("No inputs found for ",blockData.get('name'))
        return []
    for i, param in enumerate(blockInputs):
        attribute = None
        blk_instance = None
        port = None
        if str(param)[0] == '$':
            split_list = param[1:].split('.')
            blk_name = split_list[0] 
            port = split_list[1]
            if len(split_list) > 2: 
                attribute = split_list[2]

            if port == 'attr':
                blk_instance = blocks.get(blk_name)
            elif port == 'output':
                blk_instance = outputs.get(blk_name)
            
            if attribute is None:
                blockInputs[i] = blk_instance
            else:
                attr = getattr(blk_instance,attribute) 
                if attr is not None:
                    if inspect.ismethod(attr):
                        blockInputs[i] = attr()
                    else:
                        blockInputs[i] = attr
                else:
                    print("No attibute specified")
    return blockInputs