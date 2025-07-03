import sdcard
from machine import *
import os
import vfs

spi = SPI(1,sck=Pin(36), mosi=Pin(35), miso=Pin(37))
sd = sdcard.SDCard(spi, cs=Pin(42))
vfs.mount(sd,'/sd')

while True:
    try:
        with open('/sd/test.txt', 'w') as f:
            f.write('Hello, SD Card!')
        print("SD Card write successful")
        
        with open('/sd/test.txt', 'r') as f:
            content = f.read()
        print("SD Card read successful:", content)
        
    except Exception as e:
        print("Error:", e)
    sleep(5000)  # Wait before the next iteration
    