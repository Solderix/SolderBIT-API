from microbit import *
import radio
import vehicle
import srt as controller
import servo

radio.config(group=6)
radio.on()   

vehicle.acceleration = 1.0
vehicle.speed = 1.0

_next_check = 0
_check_period = 250

vehicle.set_outputs(connect=1, l6=1, l5=1, l4=1, l3=1, l2=1, l1=1, l0=1)

while True:
    data = controller.data_decode(radio.receive_bytes())

    if data != None:
        print(data)
        x = data[controller.JOY_X2]
        y = data[controller.JOY_Y1]
        if x < 100 and x > -100:
            x = 0
        servo.turn(3, scale(x, (-500, 500), (65,113)), True)
        _next_check = running_time() + _check_period
        vehicle.move(0, y)

    if _next_check < running_time():
        servo.turn(3, scale(0, (-500, 500), (65,113)), True)
        vehicle.move(0, 0)
