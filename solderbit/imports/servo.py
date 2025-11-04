from microbit import *

def init():
    data = bytearray([0x00, 0b00110001])
    i2c.write(64,data)
    data = bytearray([0xFE, 131])
    i2c.write(64,data)
    data = bytearray([0x00, 0b00100001])
    i2c.write(64,data)
    data = bytearray([0x01, 0b00001101])
    i2c.write(64,data)

front = 21
back = 20

pin11.set_analog_period(20) 
pin12.set_analog_period(20)

def turn(servo, value, convert=True):
    if convert == True:
        value = int(scale(value, (0.0,180.0), (90.0,500.0)))

    if servo == back:
        if convert == False:
            value = int(scale(value, (0.0,180.0), (90.0,500.0)))
        value = int(scale(value, (90.0,500.0), (20,125)))
        pin11.write_analog(value)
        return

    if servo == front:
        if convert == False:
            value = int(scale(value, (0.0,180.0), (90.0,500.0)))
        value = int(scale(value, (90.0,500.0), (20,125)))
        pin12.write_analog(value)
        return
    
    value = int(value)
    data = bytearray([0x06+(0x04*servo), 0x00, 0x00, value&0xFF, (value>>8)&0xFF])
    i2c.write(64,data)

init()

