from microbit import *
import radio
import vehicle
import srt as controller
import servo

radio.config(group=8)
radio.on()   

vehicle.acceleration = 1.0
vehicle.speed = 1.0

_next_check = 0
_check_period = 250

x_pev = 0
while True:
    data = controller.data_decode(radio.receive_bytes())

    if data != None:
        print(data)
        x = data[controller.JOY_X2]
        y = data[controller.JOY_Y1]
        
        if x < 100 and x > -100:
            x = 0

        if y < 20 and y > -20:
            y = 0
        
        servo.turn(servo.front, scale(x, (-500, 500), (70,108)), True)
        _next_check = running_time() + _check_period
        vehicle.move(0, y)

    if _next_check < running_time():
        servo.turn(servo.front, scale(0, (-500, 500), (65,113)), True)
        vehicle.move(0, 0)
