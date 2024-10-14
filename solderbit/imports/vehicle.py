from micropython import const
from solderbit import *

_engine_started = False
_vertical_direction = 0
_horizontal_direction = 0
_shift_output = 0b00000000

MOT_A_BACK = pin13
MOT_A_FRONT = pin14
MOT_B_BACK = pin15
MOT_B_FRONT = pin16

MOTOR_OFF = const(0)
MOTOR_ON = const(1)

_ACCELERATION_RATE = 1.0
_SPEED_MAX = 1.0

_buzz = pin8

def _constrain(val, min_val, max_val) -> int:
    return min(max_val, max(min_val, val))


def _get_sign(value):
    if value < 0:
        return True
    else:
        return False


def engine_stop():
    global _engine_started
    _engine_started = False
    return


def engine_start():
    global _engine_started
    _engine_started = True
    return


def set_acceleration(acceleeration):
    global _ACCELERATION_RATE
    if(acceleeration > 1.0):
        _ACCELERATION_RATE = 1.0
        return
    _ACCELERATION_RATE = acceleeration


def set_speed(speed):
    global _SPEED_MAX
    if(speed > 1.0):
        _SPEED_MAX = 1.0
        return
    _SPEED_MAX = speed


def move(x,y, delay=0):
    if _engine_started is False:
        return
    
    global _vertical_direction
    global _horizontal_direction

    limits = 6000

    if x < limits and x > -limits:
        x = 0

    if y < limits and y > -limits:
        y = 0

    x = scale(x, (-65535, 65535), (-2000*_SPEED_MAX, 2000*_SPEED_MAX))
    y = scale(y, (-65535, 65535), (-2000*_SPEED_MAX, 2000*_SPEED_MAX))
    
    duration = running_time() + delay
    first_loop = True
    motor_a = 0
    motor_b = 0
    while duration > running_time() or first_loop == True:
        delta_regulator = lambda d_curr,d_prev: abs(1.3-abs((d_curr-d_prev)/1000.0))
        
        _vertical_direction = ((_vertical_direction*0.3) + (-x*delta_regulator(-x,_vertical_direction)*0.7))
        _horizontal_direction =  ((_horizontal_direction*(1.0-_ACCELERATION_RATE)) + (y*delta_regulator(y,_horizontal_direction)*(_ACCELERATION_RATE))) 

        motor_a = int(_constrain(_vertical_direction - _horizontal_direction, -1000, 1000))
        motor_b = int(_constrain(_vertical_direction + _horizontal_direction, -1000, 1000))

        MOT_A_BACK.write_analog(MOTOR_OFF if _get_sign(motor_a) else  abs(motor_a))
        MOT_A_FRONT.write_analog(abs(motor_a) if _get_sign(motor_a) else  MOTOR_OFF) 
        MOT_B_BACK.write_analog(MOTOR_OFF if _get_sign(motor_b) else  abs(motor_b))
        MOT_B_FRONT.write_analog(abs(motor_b) if _get_sign(motor_b) else  MOTOR_OFF)
        first_loop = False

    return motor_a, motor_b


def set_outputs(connect=None, l6=None, l5=None, l4=None, l3=None, l2=None, l1=None, l0=None):
    global _shift_output
    values = [connect, l6, l5, l4, l3, l2, l1,l0]

    clock = pin0
    data = pin1
    strobe = pin2

    for idx, value in enumerate(values):
        if value != None:
            value = value&1
            data.write_digital(value)
            _shift_output =  _shift_output | ((1)<<idx) if value is 1 else _shift_output & ~((1)<<idx)
        else:
            data.write_digital((_shift_output>>idx)&1)   
        sleep(1)
        clock.write_digital(1)
        sleep(1)
        clock.write_digital(0)

    strobe.write_digital(0) 
    sleep(1)
    strobe.write_digital(1)
    sleep(1) 
    strobe.write_digital(0) 

    data.write_digital(0)


_horn_prev = 0
_buzzcnt=1
def horn(on=0):
    global _horn_prev
    global _buzzcnt
    
    if running_time() < _horn_prev:
        return
     
    _horn_prev = running_time() + 10
    if on != 0:
        _buzzcnt = (1+_buzzcnt*2)%30 
        _buzz.write_analog(20, (500+_buzzcnt))
    else:
        _buzz.write_analog(0, 1000)


def get_output(input: str=None):
    pass


