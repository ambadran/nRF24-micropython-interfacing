from machine import Pin, SPI
from struct import unpack
import time

class Mode:
    RX = 0
    TX = 1


class nRF24:
    '''
    Interface nRF24 module
    '''
    R_REGISTER = 0x00  
    W_REGISTER = 0x20  

    # Argument commands
    R_RX_PAYLOAD = 0x61  
    W_TX_PAYLOAD = 0xA0  

    # No Argument commands
    FLUSH_TX = 0xE1  
    FLUSH_RX = 0xE2  
    REUSE_TX_PL = 0xE3  
    NOP = 0xFF

    MEM_READ = {'CONFIG': R_REGISTER | 0x00,
        'EN_AA': R_REGISTER | 0x01,
        'EN_RXADDR': R_REGISTER | 0x02,
        'SETUP_AW': R_REGISTER | 0x03,
        'SETUP_RETR': R_REGISTER | 0x04,
        'RF_CH': R_REGISTER | 0x05,
        'RF_SETUP': R_REGISTER | 0x06,
        'STATUS': R_REGISTER | 0x07,
        'OBSERVE_TX': R_REGISTER | 0x08,
        'CD': R_REGISTER | 0x09,
        'RX_ADDR_P0': R_REGISTER | 0x0A,
        'RX_ADDR_P1': R_REGISTER | 0x0B,
        'RX_ADDR_P2': R_REGISTER | 0x0C,
        'RX_ADDR_P3': R_REGISTER | 0x0D,
        'RX_ADDR_P4': R_REGISTER | 0x0E,
        'RX_ADDR_P5': R_REGISTER | 0x0F,
        'TX_ADDR': R_REGISTER | 0x10,
        'RX_PW_P0': R_REGISTER | 0x11,
        'RX_PW_P1': R_REGISTER | 0x12,
        'RX_PW_P2': R_REGISTER | 0x13,
        'RX_PW_P3': R_REGISTER | 0x14,
        'RX_PW_P4': R_REGISTER | 0x15,
        'RX_PW_P5': R_REGISTER | 0x16,
        'FIFO_STATUS': R_REGISTER | 0x17,
        'DYNPD': R_REGISTER | 0x1C,
        'FEATURE': R_REGISTER | 0x1D }

    MEM_WRITE = {'CONFIG': W_REGISTER | 0x00,
        'EN_AA': W_REGISTER | 0x01,
        'EN_RXADDR': W_REGISTER | 0x02,
        'SETUP_AW': W_REGISTER | 0x03,
        'SETUP_RETR': W_REGISTER | 0x04,
        'RF_CH': W_REGISTER | 0x05,
        'RF_SETUP': W_REGISTER | 0x06,
        'STATUS': W_REGISTER | 0x07,
        'OBSERVE_TX': W_REGISTER | 0x08,
        'CD': W_REGISTER | 0x09,
        'RX_ADDR_P0': W_REGISTER | 0x0A,
        'RX_ADDR_P1': W_REGISTER | 0x0B,
        'RX_ADDR_P2': W_REGISTER | 0x0C,
        'RX_ADDR_P3': W_REGISTER | 0x0D,
        'RX_ADDR_P4': W_REGISTER | 0x0E,
        'RX_ADDR_P5': W_REGISTER | 0x0F,
        'TX_ADDR': W_REGISTER | 0x10,
        'RX_PW_P0': W_REGISTER | 0x11,
        'RX_PW_P1': W_REGISTER | 0x12,
        'RX_PW_P2': W_REGISTER | 0x13,
        'RX_PW_P3': W_REGISTER | 0x14,
        'RX_PW_P4': W_REGISTER | 0x15,
        'RX_PW_P5': W_REGISTER | 0x16,
        'FIFO_STATUS': W_REGISTER | 0x17,
        'DYNPD': W_REGISTER | 0x1C,
        'FEATURE': W_REGISTER | 0x1D }

    # Constants
    mode_values = {Mode.RX: 0x0B, Mode.TX: 0x0A}
    PAYLOAD_BYTES = 5

    def __init__(self, mode, rf_channel):

        # Type checking
        if type(mode) != Mode:
            raise ValueError("mode must be of type Mode")

        if type(rf_channel) != int:
            raise ValueError("rf_channel must be an integer")

        # seting up the spi module and pins
        self.led = Pin(25, Pin.OUT)
        self.spi = SPI(0, baudrate=400000, sck=Pin(18), mosi=Pin(19), miso=Pin(16))
        self.CE = Pin(21, Pin.OUT)  # chip enable pin
        self.CSN = Pin(20, Pin.OUT)  # spi chip select pin

        # nRF24 Module SPI init Routine
        self.CSN(0)  # spi enable is active low, disabled by default
        self.CE(0)  # chip disabled
        time.sleep_us(10)

        self.write(nRF24.MEM_WRITE['CONFIG'], 0x0B)
        self.write(nRF24.MEM_WRITE['EN_AA'], 0x00)
        self.write(nRF24.MEM_WRITE['EN_RXADDR'], 0x01)
        self.write(nRF24.MEM_WRITE['SETUP_AW'], 0x03)
        self.write(nRF24.MEM_WRITE['SETUP_AW'], 0x03)
        self.write_buf(nRF24.MEM_WRITE['RX_ADDR_P0'], [0xe1, 0xe1, 0xe1, 0xe1, 0xe1])
        self.write_buf(nRF24.MEM_WRITE['TX_ADDR'], [0xe1, 0xe1, 0xe1, 0xe1, 0xe1])
        self.write(nRF24.MEM_WRITE['SETUP_RETR'], 0x00)
        self.write(nRF24.MEM_WRITE['RF_CH'], rf_channel)
        self.write(nRF24.MEM_WRITE['RF_SETUP'], 0x0f)
        self.write(nRF.MEM_WRITE['RX_PW_P0'], nRF24.PAYLOAD_BYTES)
        time.sleep_us(10)

        self.write(nRF24.MEM_WRITE['CONFIG'], nRF24.mode_values[mode])
        if mode == Mode.RX:
            CE(1)
        elif mode == Mode.TX:
            CE(0)
        time.sleep_us(10)

        if (read(nRF24.MEM_READ['CONFIG']) & 0x08) != 0:
            print("nRF24 Successfully initiated! :D")
        else:
            print("nRF24 Failed to initiate! :(")
        time.sleep_us(100)

    def read(self, address):
        '''
        nRF24 READ command followed by the argument address given
        :return: the one byte data read
        '''
        if address not in nRF24.MEM_READ.values() and address not in [nRF24.R_RX_PAYLOAD, nRF24.W_TX_PAYLOAD]:
            raise ValueError("Unknown Register!")

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
        #TODO: put all other big registers in a list and compare with it instead of making a list every time
        if address not in nRF24.MEM_WRITE.values() and address not in [nRF24.W_TX_PAYLOAD, nRF24.R_RX_PAYLOAD, nRF24.FLUSH_TX, nRF24.FLUSH_RX, nRF24.REUSE_TX_PL, nRF24.NOP]:
            raise ValueError("Unknown Register!") #TODO: improve message

        if address in [nRF24.FLUSH_TX, nRF24.FLUSH_RX, nRF24.REUSE_TX_PL, nRF24.NOP]:
            complete_data_bytes = address.to_bytes(1, 'big')
        else:
            complete_data_int = (address << 8) | data
            complete_data_bytes = complete_data_int.to_bytes(2, 'big')

        try:
            self.CSN(0)
            self.spi.write(complete_data_bytes)
        finally:
            self.CSN(1)

    def write_buf(self, address, data)
        '''

        Writes data list to a buffer register
        '''

        if address not in nRF24.MEM_WRITE.values() and address not in [nRF24.W_TX_PAYLOAD, nRF24.R_RX_PAYLOAD]:
            raise ValueError("Unknown Register to send a buffer to!")

        if type(data) not in [list, tuple]:
            raise ValueError("data should be of type list or tuple")

        data.insert(0, address)
        try:
            self.CSN(0)
            self.spi.write(bytes(data))
        finally:
            self.CSN(1)

    def test_module(self):
        '''
        tests if the nRF24 is responsive by reading register 0x04
        then writing 204 or 3 depending opposite of the read value
        whether it is 204 or 3
        '''
        self.led.on()

        address_read = nRF24.MEM_READ['SETUP_RETR']
        address_write = nRF24.MEM_WRITE['SETUP_RETR']

        print(f'Default value of Register: 0x{address_read} is: ', end='')
        value = self.read(address_read)  # the default value is 0b00000011
        print(value, hex(value))

        # writing to register SETUP_RETR address 0x04 (which is integer 4 too) now the complete command should be 00100100 which is 0x24
        # writing data 204 which is 0b11001100
        data_to_be_written = 204 if value == 0b00000011 else 0b00000011
        print(f"Writing to Address: 0x{address_read} value of {data_to_be_written}")
        self.write(address_write, data_to_be_written) 

        print(f'New value of Register: 0x{address_read} is: ', end='')
        value = self.read(address_read)
        print(value, hex(value))

        time.sleep(0.5)
        self.led.off()

    def sendRF(self, buffer):
        '''
        sends buffer unsigned char[PAYLOAD_BYTES] to air where it should be picked by another nRF24 in the same channel
        '''
        if type(buffer) != list:
            raise ValueError("buffer should be a list of values")

        if len(buffer) > nRF24.PAYLOAD_BYTES:
            raise ValueError("buffer length should be less than nRF24.PAYLOAD_BYTES")

        self.write(nRF24.MEM_WRITE['CONFIG'], nRF24.mode_values[Mode.TX])
        self.write_buf(W_TX_PAYLOAD)
        #TODO: continue here

    def readRF(self):
        #TODO:

    def rf_data_available(self):
        #TODO:

    def flush_tx_rx(self):
        #TODO:

    #TODO: implement a main receiver routine (while(data available) {receive})
   


nrf = nRF24()
