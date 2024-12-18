from microbit import *
from ble import *
import vehicle
import controller

devices = radio.on(PERIPHERAL_MODE)

vehicle.engine_start()
vehicle.set_acceleration(1.0)
vehicle.set_speed(1.0)

horn = False
light = False

while True:
    data = controller.data_decode(radio.receive_bytes())
    
    if data != None:
        x = data[controller.inputs.JOY_X2[0]]
        y = data[controller.inputs.JOY_Y1[0]]
        light = data[controller.inputs.R1_BTN[0]]
        horn = data[controller.inputs.L1_BTN[0]]
        vehicle.move(x, y)

    if horn == True:
        vehicle.horn(1)
    else:
        vehicle.horn(0)

    if light == True:
        vehicle.set_outputs(connect=1)
    else:
        vehicle.set_outputs(connect=0)
    
    if radio.connection() == False:
        vehicle.move(0, 0)
