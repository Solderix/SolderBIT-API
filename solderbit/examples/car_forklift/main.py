from microbit import *
import radio
import vehicle
import srt as controller
import servo

radio.config(group=7)
radio.on()   

vehicle.acceleration = 1.0
vehicle.speed = 1.0

_next_check = 0
_check_period = 250

while True:
    up = False
    down = False
    data = controller.data_decode(radio.receive_bytes())

    if data != None:
        x = data[controller.JOY_X2]
        y = data[controller.JOY_Y1]
        up = data[controller.UP_BTN]
        down = data[controller.DOWN_BTN]
        fast = data[controller.Z_BTN]
        slow = data[controller.X_BTN]

        if fast == True:
            vehicle.speed = 1
        elif slow == True:
            vehicle.speed = 0.3

        _next_check = running_time() + _check_period
        vehicle.move(x, y)

    if up == True:
        servo.turn(3, 150, True)
    elif down == True:
        servo.turn(3, 90, True)

    if _next_check < running_time():
        servo.turn(3, 90, True)
        vehicle.move(0, 0)
