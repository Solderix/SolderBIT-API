from microbit import *

addr = 0x70  
i2c.write(addr, bytearray([0x00]), False)

def address(bit0, bit1, bit2):
    global addr
    addr = 0b111000 | (bit2 << 2) | (bit1 << 1) | bit0 

def select(channel):
    i2c.write(addr, bytearray([0x04 | (channel&3)]), True)

def off():
    i2c.write(addr, bytearray([0x00]), True)