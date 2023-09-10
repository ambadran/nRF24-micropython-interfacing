





def read(byte):
    '''
    read command is 000A AAAA
    where the As are the address of the wanted register in the register map

    :param byte: one byte of data as int

    :return: read data from nRF24
    '''
    
    txdata = str(byte).encode()
    rxdata = bytearray(len(txdata))

    try:
        CSN(0)
        spi.write_readinto(txdata, rxdata)  
    finally:
        CSN(1)

    return rxdata



def write(address, data):
    '''
    write command is 001A AAAA
    where the As are the address of the wanted register in the register map

    :param byte: one byte of data as int

    :return: read data while writing
    '''
    txdata = str(address + 0b00100000).encode()
    txdata += str(data).encode()
    rxdata = bytearray(len(txdata))

    try:
        CSN(0)                               # Select peripheral.
        spi.write_readinto(txdata, rxdata)  # Simultaneously write and read bytes.
    finally:
        CSN(1)   

    return rxdata



# to parse bytes from one value
byte0 = value >> 8
# byte0 = value & 0xFF00  # note that this will replace the last 8-bit value with zeros but will still have the wanted 8-bit value on top before a zerod 8-bit value
byte1 = value & 0x00FF
print(hex(byte0))
print(hex(byte1))


# put more than one byte of data in the form int and make them a bytearray
print(bytearray([read_command, data]))

# convert 1 byte integer to bytes
print(read_command.to_bytes(1, 'big'))
print(data.to_bytes(1, 'big'))


# putting two bytes of int beside each other and creating a byte string
complete_data = (read_command << 8) | data
print(complete_data.to_bytes(2, 'big'))

