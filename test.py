from machine import Pin
import time


def blink_pico():

    led = Pin('LED', Pin.OUT)

    for _ in range(10):
        led.on()
        time.sleep(0.5)
        led.off()
        time.sleep(0.5)



def blink_pico_w():

    led = Pin('LED', Pin.OUT)

    for _ in range(10):
        led.on()
        time.sleep(0.5)
        led.off()
        time.sleep(0.5)


blink_pico_w()


