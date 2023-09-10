'''
Code to transmit data through nRF24
'''
from machine import Pin, SPI
from struct import unpack
import time


########################################################################################################
# low level

def moduleSetup():
    global led
    led = Pin(25, Pin.OUT)
    global spi
    spi = SPI(0, baudrate=400000, sck=Pin(18), mosi=Pin(19), miso=Pin(16))
    global CE
    CE = Pin(21, Pin.OUT)  # chip enable pin
    CE(0)  # chip disabled
    global CSN
    CSN = Pin(20, Pin.OUT)  # SPI chip select pin
    CSN(1)  # spi enable is active low, disabled by default


def unfiltered_read(address):
    '''
    in the oscilloscope i saw 00001110 in miso (with 0xFF in mosi) which is 0e (right in the bytearray)
    the unpack returns the integer value which is correct
    THE ONLY CATCH is that if i read one byte it won't work it must be more than one byte
    it must be 2 or more

    this function is meant to send read command followed by address wanted
    it will read 2 bytes the STATUS byte received in parrallel with
    command byte and the actual data byte followed after
    e.g - send 0x00 
            aka 000 in first which is read command and 0x00 address
            which is the address of the CONFIG register
       (default receive should be)
       '0x80e' which is '0x080e' aka '08' and '0e'
       the 0e received first is the STATUS register default value 00001110
       the 08 recieved after is the CONFIG register default value 00001000


    all rxdata are Highest bit to lowers (7th to 0th)

    :param address: 5-bit INTEGER value put like this 000A AAAA
                    can be put as hex e.g 0x00 reads config register
    '''    
    try:
        CSN(0)
        rxdata = spi.read(2, address)
    finally:
        CSN(1)

    return unpack('<H', rxdata)[0]


def read(address):
    '''
    nRF24 READ command followed by the argument address given
    :return: the one byte data read
    '''
    try:
        CSN(0)
        rxdata = spi.read(2, address)
    finally:
        CSN(1)

    return unpack('<H', rxdata)[0] >> 8


def write(address, data):
    '''
    calls the nRF24 READ command followed by the address argument given
    Then followed by the data given as BYTEARRAY, e.g- b'\x01\x02'

    :return: None
    '''
    read_command = address | 0b00100000  # adding read command to address
    complete_data_int = (read_command << 8) | data
    complete_data_bytes = complete_data_int.to_bytes(2, 'big')

    try:
        CSN(0)
        spi.write(complete_data_bytes)
    finally:
        CSN(1)
########################################################################################################



########################################################################################################
# nRF24 module

# registers
CONFIG = 0x00
EN_AA = 0x01
EN_RXADDR = 0x02
SETUP_AW = 0x03
SETUP_RETR = 0x04
RF_CH = 0x05
RF_SETUP = 0x06
STATUS = 0x07
OBSERVE_TX = 0x08
CD = 0x09
RX_ADDR_P0 = 0x0A
RX_ADDR_P1 = 0x0B
RX_ADDR_P2 = 0x0C
RX_ADDR_P3 = 0x0D
RX_ADDR_P4 = 0x0E
RX_ADDR_P5 = 0x0F
TX_ADDR = 0x10
RX_PW_P0 = 0x11
RX_PW_P1 = 0x12
RX_PW_P2 = 0x13
RX_PW_P3 = 0x14
RX_PW_P4 = 0x15
RX_PW_P5 = 0x16
FIFO_STATUS = 0x17
DYNPD = 0x1C
FEATURE = 0x1D

def test_module():
    '''
    tests if the nRF24 is responsive by reading register 0x04
    then writing 204 or 3 depending opposite of the read value
    whether it is 204 or 3
    '''
    led.on()

    address = 0x04

    print(f'Default value of Register: 0x{address} is: ', end='')
    value = read(address)  # the default value is 0b00000011
    print(value, hex(value))

    # writing to register SETUP_RETR address 0x04 (which is integer 4 too) now the complete command should be 00100100 which is 0x24
    # writing data 204 which is 0b11001100
    data_to_be_written = 204 if value == 0b00000011 else 0b00000011
    print(f"Writing to Address: 0x{address} value of {data_to_be_written}")
    write(0x04, data_to_be_written) 

    print(f'New value of Register: 0x{address} is: ', end='')
    value = read(0x04)
    print(value, hex(value))

    result = 'Passed!' if data_to_be_written == value else 'Failed'
    print(f'\nTest {result}\n')

    time.sleep(0.5)
    led.off()

def nRF24_tx_config():
    '''
    configures nRF24 registers as transmitter
    '''
    write(CONFIG, 0b01111010)  # disable all interrupts, enable CRC at '1' byte encoding scheme, set PWR_UP and PRIM_RX is low
    write(SETUP_AW, 0b00000011)
    write(SETUP_RETR, 0x00)  # disable auto retransmit
    write(RF_CH, 0b00011000)
    write(RF_SETUP, 0b00000110)
    

def nRF24_send(data):
    '''
    sends one packet of data in the TX FIFO
    '''
    pass


####################################################################################################
# Main Routine
moduleSetup()

test_module()



