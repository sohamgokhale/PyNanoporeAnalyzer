import nanoporeData
import filters
import baselineDetect
import eventDetect
import sigUtils
import matplotlib.pyplot as plt
import utils

def setup():
    source = nanoporeData.nanoporeData("Data_interim/Dimer_samples_-300mV.abf")
    Filter = filters.ButterworthLPF(4, 16000, source.samplingFreq)
    Baseline = baselineDetect.BaselineMovMean(10000)
    Sub = sigUtils.SubtractAndFlip(flip=True)
    Events = eventDetect.EventDetect(50, source.samplingTime)
    run(source,Filter,Baseline,Sub,Events)

def run(source,Filter,Baseline,Sub,Events):
    ch = source.getChannel(0)
    filt = Filter.run(ch)
    base = Baseline.run(filt)
    sub = Sub.run(filt,base)
    events = Events.run(sub)

    plt.scatter(events.Amplitudes, events.dwellTimes)
    plt.show()


# Mapping between block types and their corresponding classes
block_classes = {
    'nanoporeData': nanoporeData.nanoporeData,
    'ButterworthLPF': filters.ButterworthLPF,
    'BaselineMovMean': baselineDetect.BaselineMovMean,
    'SubtractAndFlip': sigUtils.SubtractAndFlip,
    'EventDetect': eventDetect.EventDetect,
}


if __name__ == "__main__":
    block_configuration, connection_configuration = utils.ParseInput("testInput.txt")
    blocks = []

    for block_data in block_configuration:
        block_name = block_data['name']
        block_type = block_data['type']
        block_params = block_data['params']

        if(block_type in ('ButterworthLPF')):
            block_params.append(blocks[0].samplingFreq)

        if(block_type in ('EventDetect')):
            block_params.append(blocks[0].samplingTime)

        print(block_type)
        if block_type in block_classes:
            block_class = block_classes[block_type]
            block_instance = block_class(*block_params)
            blocks.append(block_instance)
        else:
            print("Error in Input file")

    
    # Create a dictionary to store the blocks by their names for easy lookup
    block_dict = {block_data['name']: block_instance for block_data, block_instance in zip(block_configuration, blocks)}

    outputs = {}
    outputs["Source"] = blocks[0].getChannel(0)
    # Iterate over the connection configuration and establish the connections
    for connection_data in connection_configuration:
        execution_block = connection_data['block']
        inputList = connection_data['inputs']
        inputs = []

        # Get the block instances involved in the connection
        execution_block_instance = block_dict.get(execution_block)
        if(execution_block != "Source"):
            for input in inputList:
                inputs.append(outputs.get(input))
            outputs[execution_block] = execution_block_instance.run(*inputs)

    
    #setup()