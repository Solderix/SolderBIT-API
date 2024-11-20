from microbit import *

_MODE1_REG = (0x00)
_MODE2_REG = (0x01)
_LED0_REG = (0x06)
_LED1_REG = (0x0A)
_LED2_REG = (0x0E)
_LED3_REG = (0x12)
_LED4_REG = (0x16)
_LED5_REG = (0x1A)
_LED6_REG = (0x1E)
_LED7_REG = (0x22)
_LED8_REG = (0x26)
_LED9_REG = (0x2A)
_LED10_REG = (0x2E)
_LED11_REG = (0x32)
_LED12_REG = (0x36)
_LED13_REG = (0x3A)
_LED14_REG = (0x3E)
_LED15_REG = (0x42)
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

