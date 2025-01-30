from microbit import *
from ble import *
import vehicle
import controller

devices = radio.on(PERIPHERAL_MODE)

vehicle.acceleration = 1.0
vehicle.speed = 1.0

while True:
    data = controller.data_decode(radio.receive_bytes())
    
    if data != None:
        print(data)
        x = data[controller.JOY_X2]
        y = data[controller.JOY_Y1]
        vehicle.move(x, y)
    
    if radio.connection() == False:
        vehicle.move(0, 0)
