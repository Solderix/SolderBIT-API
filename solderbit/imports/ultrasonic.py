from microbit import *

def distance():
    data = bytearray([0x01])
    try:
        data = bytearray([0x01])
        i2c.write(0x57, data, False)
        sleep(10)
        data = list(i2c.read(0x57, 3, True))
        ret = ( (data[0] << 16) + (data[1] << 8) + data[2] ) / 10000.0
    except:
        ret = 200.0
    return ret