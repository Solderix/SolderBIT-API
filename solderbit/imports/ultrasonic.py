from microbit import *

def distance():
    data = bytearray([0x01])
    i2c.write(0x57, data, False)
    sleep(10)
    data = i2c.read(0x57, 3, True)
    print(data)