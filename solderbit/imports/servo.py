from microbit import *
import struct
from micropython import const

_MODE1_REG = const(0x00)
_MODE2_REG = const(0x01)
_LED0_REG = const(0x06)
_LED1_REG = const(0x0A)
_LED2_REG = const(0x0E)
_LED3_REG = const(0x12)
_LED4_REG = const(0x16)
_LED5_REG = const(0x1A)
_LED6_REG = const(0x1E)
_LED7_REG = const(0x22)
_LED8_REG = const(0x26)
_LED9_REG = const(0x2A)
_LED10_REG = const(0x2E)
_LED11_REG = const(0x32)
_LED12_REG = const(0x36)
_LED13_REG = const(0x3A)
_LED14_REG = const(0x3E)
_LED15_REG = const(0x42)
_PRE_SCALE_REG = const(0xFE)

_LEDS = [_LED0_REG, _LED1_REG, _LED2_REG, _LED3_REG, _LED4_REG, _LED5_REG, _LED6_REG, _LED7_REG, _LED8_REG, _LED9_REG, _LED10_REG, _LED11_REG, _LED12_REG, _LED13_REG, _LED14_REG, _LED15_REG]

_servo_freq = const(46)
_servo_address = const(64)

_servo_pos = [90] * 16
_servo_next_pos = [90] * 16
_servo_res = 1

_deg2duty = lambda x: scale(x, (0.0,180.0), (90.0,500.0)) 

def init():
    data = bytearray([_MODE1_REG, 0b00110001])
    i2c.write(_servo_address,data)

    _set_freq(_servo_freq)

    data = bytearray([_MODE1_REG, 0b00100001])
    i2c.write(_servo_address,data)

    data = bytearray([_MODE2_REG, 0b00001101])
    i2c.write(_servo_address,data)


def turn(servo, value, convert=False):
    if convert is True:
        value = _deg2duty(value)
        _servo_pos[servo] = value
    write(servo, int(value))


def write(servo, val):
    get_low = lambda x: x&0xFF
    get_high = lambda x: (x>>8)&0xFF

    data = bytearray([_LEDS[servo], 0x00, 0x00, get_low(val), get_high(val)])
    i2c.write(_servo_address,data)


def move(servo, deg, delay):
    duty = _deg2duty(deg)
    if _servo_pos[servo] > duty:
        while _servo_pos[servo] > duty:
            _servo_pos[servo] -= 1
            turn(servo, _servo_pos[servo])
            sleep(delay)
    elif _servo_pos[servo] < duty:
        while _servo_pos[servo] < duty:
            _servo_pos[servo] += 1
            turn(servo, _servo_pos[servo])
            sleep(delay)


def set_raw(servos, raw):
    for idx,servo in enumerate(servos):
        _servo_next_pos[servo] = raw[idx]


def set(servos, degs):
    for idx,servo in enumerate(servos):
        _servo_next_pos[servo] = _deg2duty(degs[idx])


def move_servos(servos, delay):
    servos_moved = False

    for servo in servos:
        if _servo_pos[servo] > _servo_next_pos[servo]:
            _servo_pos[servo] -= _servo_res
            servos_moved = True
        elif _servo_pos[servo] < _servo_next_pos[servo]:
            _servo_pos[servo] += _servo_res
            servos_moved = True

        turn(servo, _servo_pos[servo])
    
    sleep(delay)
    return servos_moved


def resolution(res):
    global _servo_res
    if res <= 0:
        res = 1
    _servo_res = res


def update(servos, delay):
    while move_servos(servos, delay) == True:
        pass
    

def _set_freq(freq):
    prescalar_value = round((25000000)/(4096*freq))-1
    data = bytearray([_PRE_SCALE_REG, prescalar_value])
    i2c.write(_servo_address,data)
