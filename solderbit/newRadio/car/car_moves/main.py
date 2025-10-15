from microbit import *
import radio
import vehicle
import srt as controller
import cam

radio.config(group=8)
radio.on()   

vehicle.acceleration = 1.0
vehicle.speed = 1
vehicle.deadzone = 100

_next_check = 0
_check_period = 250
_auto_flag = False
_movment_cnt = 0
_tick_cnt = 0

controls = [
    [0, 1000, 200],
    [0, 0, 200],
    [1000, 0, 200],
    [0, 0, 200],
]

cam.on()
cam.quality(20)
cam.group(7)

while True:
    data = controller.data_decode(radio.receive_bytes())

    if button_a.is_pressed():
        vehicle.move(0, 1000)
    elif _next_check < running_time():
        vehicle.move(0, 0)

    if _auto_flag:
        vehicle.move(controls[_movment_cnt][0], controls[_movment_cnt][1])
        _tick_cnt = _tick_cnt + 1
        sleep(1)
        if _tick_cnt > controls[_movment_cnt][2]:
            _movment_cnt = (_movment_cnt + 1) % len(controls)
            _tick_cnt = 0

    if data == None:
        continue
    
    if data[controller.Y_BTN]:
        sleep(100)
        _auto_flag = not _auto_flag
        _tick_cnt = 0
        _movment_cnt = 0

    print(data)
    _next_check = running_time() + _check_period
    vehicle.move(x = data[controller.JOY_X2], y = data[controller.JOY_Y1])
    vehicle.horn(data[controller.L1_BTN] or data[controller.X_BTN])
