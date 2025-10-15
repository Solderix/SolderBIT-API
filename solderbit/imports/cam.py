from microbit import *


def on():
    i2c.write(20, bytearray([0x01]), True)


def off():
    i2c.write(20, bytearray([0x02]), True)


def quality(q):
    i2c.write(20, bytearray([0x07, q&0xFF]), True)


def saturation(sat):
    i2c.write(20, bytearray([0x04, sat]), True)


def contrast(con):
    i2c.write(20, bytearray([0x05, con]), True)


def bright(br):
    i2c.write(20, bytearray([0x06, br]), True)


def group(gr):
    i2c.write(20, bytearray([0x03, gr]), True)


def detect():
    i2c.write(20, bytearray([0x08]), True)


def result():
    print( i2c.read(20, 1) )