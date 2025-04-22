from microbit import *


def lux():
    i2c.write(0x60, bytearray([0x00, 0b01000000, 0x00]), True)
    i2c.write(0x60, bytearray([0x09]), False)
    data = i2c.read(0x60, 2, True)

    if data != None:
        return (data[0] | data[1] << 8) * 0.05
    else:
        return None
    
def detect():
    i2c.write(0x60, bytearray([0x03, 0b00000100, 0x00]), True)
    i2c.write(0x60, bytearray([0x08]), False)
    data = i2c.read(0x60, 2, True)

    if data != None:
        return (data[0] | data[1] << 8)
    else:
        return None