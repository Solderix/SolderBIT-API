from microbit import *
import music

_shift_output = [0, 0, 0, 0, 0, 0, 0, 0]

acceleration = 1.0
speed = 1.0
vertical_direction = 0
horizontal_direction = 0
deadzone = 20

horn_pin = pin8

def move(x,y, delay=0):
    global acceleration
    global speed
    global vertical_direction
    global horizontal_direction

    x = 0 if abs(x) < deadzone else (x*2)
    y = 0 if abs(y) < deadzone else (y*2*speed)
    
    duration = running_time() + delay
    while duration > running_time() or delay == 0:
        vertical_direction = ((vertical_direction*0.3) + (-x*0.7))
        horizontal_direction =  ((horizontal_direction*(1.0-acceleration)) + (y*(acceleration))) 

        motor_a = int(min(511, max(-511, vertical_direction - horizontal_direction)))*2
        motor_b = int(min(511, max(-511, vertical_direction + horizontal_direction)))*2

        #MOT_A_BACK = pin13   MOT_A_FRONT = pin14   MOT_B_BACK = pin15   MOT_B_FRONT = pin16
        pin13.write_analog(max(0, motor_a))
        pin14.write_analog(max(0, -motor_a))
        pin15.write_analog(max(0, motor_b))
        pin16.write_analog(max(0, -motor_b))
        delay = 1


def set_outputs(connect=None, l6=None, l5=None, l4=None, l3=None, l2=None, l1=None, l0=None):
    #clock = pin0   data = pin1   strobe = pin8
    global _shift_output
    values = [connect, l6, l5, l4, l3, l2, l1,l0]

    for idx, value in enumerate(values):
        if value != None:
            pin1.write_digital(value&1)
            _shift_output[idx] = value
        else:
            pin1.write_digital(_shift_output[idx])   

        pin0.write_digital(1)
        pin0.write_digital(0)

    pin8.write_digital(1)
    pin8.write_digital(0) 


def horn(state):
    if state:
        music.pitch(245, 5000, pin=horn_pin, wait=False)
    else:
        music.stop(horn_pin)