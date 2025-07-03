from microbit import *
import radio
import vehicle
import srt as controller
import servo

radio.config(group=5)
radio.on()   

vehicle.acceleration = 1.0
vehicle.speed = 1.0

_next_check = 0
_check_period = 250

servo_4 = scale(0, (-500, 500), (150,450))
servo_5 = scale(0, (500, -500), (100,480))
servo_4_set = servo_4
servo_5_set = servo_5

while True:
    data = controller.data_decode(radio.receive_bytes())

    if data != None:
        print(data)
        x2 = data[controller.JOY_X1]
        y2 = data[controller.JOY_Y1]
        x1 = data[controller.JOY_X2]
        y1 = data[controller.JOY_Y2]
        x2_pev = x2
        y2_pev = y2

        if x1 < 100 and x1 > -100:
            x1 = 0
        
        servo.turn(3, scale(x1, (-500, 500), (70,108)), True)
        _next_check = running_time() + _check_period
        vehicle.move(0, y1)

        servo_4_set =  scale(x2, (500, -500), (90,470))
        servo_5_set =  scale(y2, (-500, 500), (90,470))

    if _next_check < running_time():
        servo_4 = scale(0, (500, -500), (90,470))
        servo_5 = scale(0, (-500, 500), (90,470))
        servo.turn(3, scale(0, (-500, 500), (65,113)), True)
        vehicle.move(0, 0)

    
    if servo_4 < servo_4_set:
        servo_4 = servo_4 + 1
    elif servo_4 > servo_4_set:
        servo_4 = servo_4 - 1 

    if servo_5 < servo_5_set:
        servo_5 = servo_5 + 1
    elif servo_5 > servo_5_set:
        servo_5 = servo_5 - 1
        

    servo.turn(5, servo_5, False)
    servo.turn(4, servo_4, False)
    sleep(2)
