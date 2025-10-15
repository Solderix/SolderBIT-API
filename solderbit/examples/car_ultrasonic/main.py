from microbit import *
import radio
import vehicle
import srt as controller
import ultrasonic

radio.config(group=8)
radio.on()   

vehicle.acceleration = 1.0
vehicle.speed = 1
vehicle.deadzone = 100

_auto_flag = False

while True:
    data = controller.data_decode(radio.receive_bytes())

    if button_a.is_pressed():
        vehicle.move(0, 1000)
        continue

    if radio.check_connection() == False:
        vehicle.move(0, 0)

    if _auto_flag:
        if ultrasonic.distance() < 15:
            vehicle.move(x = 500, y = 0)
            sleep(300)
        else:
            vehicle.move(x = 0, y = 250)

    if data == None:
        continue
    
    if data[controller.Y_BTN]:
        sleep(100)
        _auto_flag = not _auto_flag

    vehicle.move(x = data[controller.JOY_X2], y = data[controller.JOY_Y1])
    vehicle.horn(data[controller.L1_BTN] or data[controller.X_BTN])
