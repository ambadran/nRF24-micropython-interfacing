"""
Main Routine
"""
from micropython import const
from machine import Pin, SPI
from nrf24l01 import NRF24L01
from time import sleep_ms, sleep_us
import _thread


class state:
    RECEIVER = 0
    TRANSMITTER = 1

class Station:
    '''
    Abstraction for Station that will send commands and receive data
    '''
    SPI_HARDWARE_INDEX = const(0)
    DEFAULT_PAYLOAD_SIZE = const(32)
    CHANNEL = const(46)
    PIPES = (b"\xe1\xf0\xf0\xf0\xf0", b"\xd2\xf0\xf0\xf0\xf0")  # Addresses are in little-endian format. They correspond to big-endian
    RX_POLL_DELAY = const(15)

    def __init__(self, dev):

        if dev == 'pico':
            # Pico pinout
            self.SCK_PIN = const(18)
            self.MOSI_PIN = const(19)
            self.MISO_PIN = const(16)
            self.CSN_PIN = const(21)
            self.CE_PIN = const(20)

        elif dev == 'zero':
            # raspberry pi zero pinout
            self.SCK_PIN = const(2)
            self.MOSI_PIN = const(3)
            self.MISO_PIN = const(4)
            self.CSN_PIN = const(8)
            self.CE_PIN = const(14)

        else:
            raise ValueError("unsupported platform")

        self.spi = SPI(self.SPI_HARDWARE_INDEX, sck=Pin(self.SCK_PIN), mosi=Pin(self.MOSI_PIN), miso=Pin(self.MISO_PIN))
        self.csn = Pin(self.CSN_PIN, mode=Pin.OUT, value=1)
        self.ce = Pin(self.CE_PIN, mode=Pin.OUT, value=0)

        self.nrf = NRF24L01(self.spi, self.csn, self.ce, payload_size=self.DEFAULT_PAYLOAD_SIZE)

        self.nrf.open_tx_pipe(self.PIPES[0])
        self.nrf.open_rx_pipe(1, self.PIPES[1])
        self.nrf.start_listening()
        
        self.state = state.RECEIVER

        _thread.start_new_thread(self.keep_receiving, ())

    def receive(self) -> str:
        '''
        listens, prints if received and saves values in internal attributes
        '''
        if self.state == state.RECEIVER:
            if self.nrf.any():
                while self.nrf.any():
                    buf = self.nrf.recv()
                    print(buf.decode(), end="")

    def keep_receiving(self):
        '''
        
        '''
        try:
            while True:
                self.receive()
                sleep_us(self.RX_POLL_DELAY)
        except KeyboardInterrupt:
            pass

    def send(self, string=""):
        '''
        sends enter
        '''
        self.state = state.TRANSMITTER
        self.nrf.send_ascii(string)
        self.state = state.RECEIVER

    def print_nrf_registers(self):
        '''

        '''
        self.state = state.TRANSMITTER
        self.nrf.print_registers()
        self.state = state.RECEIVER



