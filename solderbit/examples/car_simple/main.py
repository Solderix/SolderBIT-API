from microbit import *
import radio
import vehicle
import srt as controller

radio.config(group=8)
radio.on()   

vehicle.acceleration = 1.0
vehicle.speed = 1
vehicle.deadzone = 100


vehicle.set_outputs(l0=True, connect = True)
vehicle.set_outputs(l0=True, connect = True)
vehicle.set_outputs(l0=True, connect = True)
vehicle.set_outputs(l0=True, connect = True)
vehicle.set_outputs(l0=False, connect = True)
vehicle.set_outputs(l0=True, connect = True)
vehicle.set_outputs(l0=True, connect = True)

while True:
    data = controller.data_decode(radio.receive_bytes(True))

    if radio.check_connection() == False:
        vehicle.move(0, 0)

    if data == None:
        continue
    
    vehicle.move(x = data[controller.JOY_X2], y = data[controller.JOY_Y1])
    vehicle.horn(data[controller.L1_BTN] or data[controller.X_BTN])
