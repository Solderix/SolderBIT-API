from microbit import *
import radio
import vehicle
import srt as controller

radio.config(group=6)
radio.on()   

vehicle.engine_start()
vehicle.set_acceleration(1.0)
vehicle.set_speed(1.0)

_next_check = 0
_check_period = 250

while True:
    data = controller.data_decode(radio.receive_bytes())
    
    if data != None:
        print(data)
        x = data[controller.inputs.JOY_X2[0]]
        y = data[controller.inputs.JOY_Y1[0]]
        _next_check = running_time() + _check_period
        vehicle.move(x, y)

    if _next_check < running_time():
        vehicle.move(0, 0)
