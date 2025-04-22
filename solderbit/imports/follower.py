from microbit import *

i2c.write(72, bytearray([0x01, 0x66, 0x83]), True)

def read(channel):
    i2c.write(72, bytearray([0x01, 0b01000110 | ((channel&3)<<4), 0b11100011]), True)
    sleep(5)
    i2c.write(72, bytearray([0x00]), False)
    data = i2c.read(72,2,True)

    if data == None:
        return None
    
    value = (((data[1] | data[0] << 8)) >> 4)

    if value > 0x800:
        value = (0xFFF - value) * -0.0005
    else:
        value = value * 0.0005
    
    return value
