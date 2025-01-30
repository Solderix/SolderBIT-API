from microbit import *
import radio
import vehicle
import srt as controller

radio.config(group=6)
radio.on()   

vehicle.acceleration = 1
vehicle.speed = 0.4

_next_check = 0
_check_period = 250

vehicle.set_outputs(connect=1, l6=1, l5=1, l4=1, l3=1, l2=1, l1=1, l0=1)

while True:
    data = controller.data_decode(radio.receive_bytes())
    if data != None:
        print(data)
        x = data[controller.JOY_X2]
        y = data[controller.JOY_Y1]
        _next_check = running_time() + _check_period
        vehicle.move(x, y)

    if _next_check < running_time():
        vehicle.move(0, 0)