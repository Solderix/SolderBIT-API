from microbit import *

INPUT = 1
OUTPUT = 0
LOW = 0
HIGH = 1

i2c.write(33, bytearray([ 0x0A, 0]), True)

def mode(pin,mode):
    port = 0x01
    if pin >= 8:
        pin = pin-8
        port = 0x00
    
    i2c.write(33, bytearray([port]), True)
    modes = bytearray(i2c.read(33, 1, True))
    try:
        modes[0] = int(modes[0]) & ~(1<<pin) if mode == OUTPUT else int(modes[0]) | (1<<pin) 
        i2c.write(33, bytearray([port]) + modes, True)
    except:
        pass
    return pin, port


def read(pin):
    pin, port = mode(pin, INPUT)
    i2c.write(33, bytearray([0x12+port]), True)
    states = i2c.read(33, 1, True)
    return (states[0]>>pin)&1

    
def write(pin, state):
    pin, port = mode(pin, OUTPUT)
    i2c.write(33, bytearray([0x14+port]), True)
    states = bytearray(i2c.read(33, 1, True))
    try:
        states[0] = int(states[0]) & ~(1<<pin) if state == LOW else int(states[0]) | (1<<pin) 
        i2c.write(33, bytearray([0x14+port]) + states, True)
    except:
        pass