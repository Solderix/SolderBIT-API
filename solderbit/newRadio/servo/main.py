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
__blink_period = 0
_blink_flag = 0
_turning = 0

vehicle.set_outputs(connect=1, l6=0, l5=0, l4=0, l3=0, l2=0, l1=0, l0=1)

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

        if(y < -10):
            vehicle.set_outputs(l4=1)
        else:
            vehicle.set_outputs(l4=0)

        if __blink_period < running_time():
            __blink_period = running_time() + 250
            _blink_flag = not _blink_flag

            if _blink_flag == 1:
                if((_turning == 0) and (y > 100 or y < -100)):
                    vehicle.set_outputs(l2=0, l1=0)
                elif(x < -100):
                    vehicle.set_outputs(l2=1, l1=0)
                    _turning = 1
                elif(x > 100):
                    vehicle.set_outputs(l2=0, l1=1)
                    _turning = 1
                else:
                    vehicle.set_outputs(l2=0, l1=0)
                    _turning = 0
            else:
                vehicle.set_outputs(l2=0, l1=0)

    if _next_check < running_time():
        servo.turn(3, scale(0, (-500, 500), (65,113)), True)
        vehicle.move(0, 0)
