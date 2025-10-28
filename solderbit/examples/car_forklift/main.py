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
        servo.turn(servo.front, 90, True)
        vehicle.move(0, 0)

    if data != None:
        if data[controller.Z_BTN]:
            vehicle.speed = 1
        elif data[controller.X_BTN]:
            vehicle.speed = 0.3

        if data[controller.UP_BTN]:
            servo.turn(servo.front, 150, True)
        elif data[controller.DOWN_BTN]:
            servo.turn(servo.front, 90, True)

        vehicle.move(data[controller.JOY_X2], data[controller.JOY_Y1])