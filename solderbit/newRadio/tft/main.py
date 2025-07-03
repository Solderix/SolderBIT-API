from machine import Pin, SPI
import st7789
from microbit import *
import radio
import jpeg
import controller

radio.config(group=7)
radio.on()

image_end = bytearray([0xFF,0xFE,0xFE,0xFE])


def handle_image_data(img_data):
    radio.send_bytes(b'\x01')
    _next_check = running_time()

    while True:
        data = radio.receive_bytes()

        if (_next_check + 100) < running_time():
            return

        if data is None:
            continue

        if data[0:4] == image_end:
            break

        _next_check = running_time()
        img_data.extend(data)
        radio.send_bytes(b'\x01')


def config(rotation=0, buffer_size=0, options=0):
    return st7789.ST7789(
        SPI(2, baudrate=60_000_000, sck=Pin(18), mosi=Pin(14)),
        128,
        160,
        reset=Pin(46, Pin.OUT),
        cs=Pin(39, Pin.OUT),
        dc=Pin(16, Pin.OUT),
        backlight=Pin(47, Pin.OUT),
        color_order=st7789.RGB,
        rotation=rotation,
        inversion=False)

tft = config(1)
tft.init()
tft.offset(1,2)
tft.fill(st7789.BLACK)

def load_image():
    decoder = jpeg.Decoder(rotation=0, format="RGB565_BE", block=True)
    img_data = bytearray()
    handle_image_data(img_data)
    try:
        for y in range(4, 121, 8):
            dt = decoder.decode(img_data)
            tft.blit_buffer(dt, 0, y, 160, 120)
    except:
        tft.fill(st7789.BLACK)
        return

while True:
    radio.config(group=7)
    load_image()
    radio.config(group=5)
    radio.send_bytes(controller.read_encoded())