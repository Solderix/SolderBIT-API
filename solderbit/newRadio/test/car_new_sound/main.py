from microbit import *
import radio
import vehicle
import srt as controller
import music

radio.config(group=10)
radio.on()   

vehicle.acceleration = 1.0
vehicle.speed = 1
vehicle.deadzone = 100

_next_check = 0
_check_period = 250


while True:
    data = controller.data_decode(radio.receive_bytes())

    if _next_check < running_time():
        vehicle.move(0, 0)

    if data == None:
        continue

    _next_check = running_time() + _check_period
    sound = (((abs(data[controller.JOY_Y1]) if abs(data[controller.JOY_Y1]) > 120 else 120)-120)/500)*6000+750
    
    vehicle.move(x = data[controller.JOY_X2], y = data[controller.JOY_Y1])
    
    if data[controller.L1_BTN]:
        music.pitch(int(sound), 50)
    else:
        music.stop(vehicle._buzz)
