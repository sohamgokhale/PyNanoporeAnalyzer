import utils, config
import inspect
import argparse

def setup(blockConfig):
    blocks = {}
    for blockData in blockConfig:
        blockName = blockData.get('name')
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

        if blockClass in config.block_classes:
            blockCls = config.block_classes[blockClass]
            blockInstance = blockCls(*blockParams)
            blocks.update({blockName:blockInstance})
        else:
            print("Error in Input File")
    return blocks

def run(blockConfig,blocks):
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

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", type= str, help="Path to input file (yaml)", required=True)
    args = parser.parse_args()

    blockConfig = utils.ParseYAML(args.file)
    blocks = setup(blockConfig)
    run(blockConfig,blocks)


if __name__ == "__main__":
    main()
    

