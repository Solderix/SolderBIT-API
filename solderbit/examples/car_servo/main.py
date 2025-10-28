from microbit import *
import radio
import vehicle
import srt as controller
import servo

radio.config(group=8)
radio.on()   

vehicle.acceleration = 1.0
vehicle.speed = 1.0
vehicle.deadzone = 100

while True:
    data = controller.data_decode(radio.receive_bytes(True))

    if radio.check_connection() == False:
        servo.turn(servo.front, scale(0, (-500, 500), (65,113)), True)
        vehicle.move(0, 0)

    if data != None:
        x = data[controller.JOY_X2]
        
        if x < 100 and x > -100:
            x = 0
        
        servo.turn(servo.front, scale(x, (-500, 500), (70,108)), True)
        vehicle.move(0, data[controller.JOY_Y1])


