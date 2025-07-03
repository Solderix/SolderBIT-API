from microbit import *
import radio
import vehicle
import srt as controller

radio.config(group=8)
radio.on()   

vehicle.acceleration = 1.0
vehicle.speed = 1

_next_check = 0
_check_period = 250

while True:
    data = controller.data_decode(radio.receive_bytes())

    if _next_check < running_time():
        vehicle.move(0, 0)

    if data == None:
        continue
    
    print(data)
    _next_check = running_time() + _check_period
    vehicle.move(data[controller.JOY_X2], y = data[controller.JOY_Y1])
    vehicle.horn(data[controller.L1_BTN])