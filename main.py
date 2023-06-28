import utils
import config
import argparse
import matplotlib.pyplot as plt


def setup(blockConfig):
    blocks = {}
    for blockData in blockConfig:
        blockName = blockData.get('name')
        blockClass = blockData.get('class')
        blockParams = utils.decodeParams(blockData, blocks)

        if blockClass in config.block_classes:
            blockCls = config.block_classes[blockClass]
            blockInstance = blockCls(*blockParams)
            blocks.update({blockName: blockInstance})
        else:
            print("Error in Input File")
    return blocks


def run(blockConfig, blocks):
    outputs = {}
    for blockData in blockConfig:
        inputList = []
        if blockData.get('type') != 'Source':
            inputList = utils.decodeInputs(blockData, blocks, outputs)
            block_instance = blocks.get(blockData.get('name'))
            output = block_instance.run(*inputList)
            outputs.update({blockData.get('name'): output})

    plt.show()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", type=str,
                        help="Path to input file (yaml)", required=True)
    args = parser.parse_args()

    blockConfig = utils.ParseYAML(args.file)
    blocks = setup(blockConfig)
    run(blockConfig, blocks)


if __name__ == "__main__":
    main()
