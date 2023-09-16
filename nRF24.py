from machine import Pin, SPI
from struct import unpack
import time


class nRF24:
    '''
    Interface nRF24 module
    '''
    def __init__(self):

        # seting up the spi module and pins
        self.led = Pin(25, Pin.OUT)

        self.spi = SPI(0, baudrate=400000, sck=Pin(18), mosi=Pin(19), miso=Pin(16))

        self.CE = Pin(21, Pin.OUT)  # chip enable pin
        self.CE(0)  # chip disabled

        self.CSN = Pin(20, Pin.OUT)  # self.spi chip select pin
        self.CSN(1)  # self.spi enable is active low, disabled by default

        # Module SPI init Routine
        #TODO: 


    def unfiltered_read(self, address):
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
            self.CSN(0)
            rxdata = self.spi.read(2, address)
        finally:
            self.CSN(1)

        return unpack('<H', rxdata)[0]

    def read(self, address):
        '''
        nRF24 READ command followed by the argument address given
        :return: the one byte data read
        '''
        try:
            self.CSN(0)
            rxdata = self.spi.read(2, address)
        finally:
            self.CSN(1)

        return unpack('<H', rxdata)[0] >> 8

    def write(self, address, data):
        '''
        calls the nRF24 READ command followed by the address argument given
        Then followed by the data given as BYTEARRAY, e.g- b'\x01\x02'

        :return: None
        '''
        read_command = address | 0b00100000  # adding read command to address
        complete_data_int = (read_command << 8) | data
        complete_data_bytes = complete_data_int.to_bytes(2, 'big')

        try:
            self.CSN(0)
            self.spi.write(complete_data_bytes)
        finally:
            self.CSN(1)

    def test_module(self):
        '''
        tests if the nRF24 is responsive by reading register 0x04
        then writing 204 or 3 depending opposite of the read value
        whether it is 204 or 3
        '''
        self.led.on()

        address = 0x04

        print(f'Default value of Register: 0x{address} is: ', end='')
        value = self.read(address)  # the default value is 0b00000011
        print(value, hex(value))

        # writing to register SETUP_RETR address 0x04 (which is integer 4 too) now the complete command should be 00100100 which is 0x24
        # writing data 204 which is 0b11001100
        data_to_be_written = 204 if value == 0b00000011 else 0b00000011
        print(f"Writing to Address: 0x{address} value of {data_to_be_written}")
        self.write(0x04, data_to_be_written) 

        print(f'New value of Register: 0x{address} is: ', end='')
        value = self.read(0x04)
        print(value, hex(value))

        time.sleep(0.5)
        self.led.off()


def setMode(mode):
    '''
    :param mode: integer deciding which mode to be in
        0: Power Down
        1: Standby-I
        2: Standby-II

    '''
    pass
    
nrf = nRF24()
