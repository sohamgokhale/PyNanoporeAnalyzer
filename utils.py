
def ParseInput(path):

    block_configuration = []
    connection_configuration = []

    # Read the input text file
    with open(path,'r') as file:
        lines = file.readlines()

    # Process the lines to obtain block and connection configurations
    block_definition_mode = False
    
    for line in lines:
        line = line.strip()

        if line.startswith('#'):
            continue

        if line.startswith('BLOCK'):
            block_definition_mode = True
            block_data = {'name': line.split()[1]}
            continue

        if line.startswith('CONNECT'):
            block_definition_mode = False
            connection_data = {'block': line.split()[1], 'inputs': line.split()[3:]}
            connection_configuration.append(connection_data)
            continue

        if block_definition_mode:
            if line.startswith('TYPE'):
                block_data['type'] = str(line.split()[1])
            elif line.startswith('PARAMS'):
                block_data['params'] = line.split()[1:]
                block_configuration.append(block_data)

    # Print the obtained block configuration and connection configuration
    print("Block Configuration:")
    for block in block_configuration:
        print(block)

    print("\nConnection Configuration:")
    for connection in connection_configuration:
        print(connection)

    return block_configuration, connection_configuration