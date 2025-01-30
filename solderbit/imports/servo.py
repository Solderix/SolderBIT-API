from microbit import *

_MODE1_REG = (0x00)
_MODE2_REG = (0x01)
_LED0_REG = (0x06)
_PRE_SCALE_REG = (0xFE)

data = bytearray([_MODE1_REG, 0b00110001])
i2c.write(64,data)
data = bytearray([_PRE_SCALE_REG, 131])
i2c.write(64,data)
data = bytearray([_MODE1_REG, 0b00100001])
i2c.write(64,data)
data = bytearray([_MODE2_REG, 0b00001101])
i2c.write(64,data)

def turn(servo, value, convert=True):
    if convert == True:
        value = int(scale(value, (0.0,180.0), (90.0,500.0)))
    data = bytearray([_LED0_REG+(0x04*servo), 0x00, 0x00, value&0xFF, (value>>8)&0xFF])
    i2c.write(64,data)

