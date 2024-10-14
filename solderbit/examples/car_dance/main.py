from solderbit import *
from radio import *
import vehicle
import controller

devices = radio.on(PERIPHERAL_MODE)

vehicle.engine_start()
vehicle.set_acceleration(0.4)
vehicle.set_speed(1.0)

while True:
    data = None
    data = controller.data_decode(radio.receive_bytes())

    if data != None:
        up = data[controller.inputs.LEFT_UP_BTN[0]]
        down = data[controller.inputs.LEFT_DOWN_BTN[0]]
        left = data[controller.inputs.LEFT_LEFT_BTN[0]]
        right = data[controller.inputs.LEFT_RIGHT_BTN[0]]

        if up == True:
          vehicle.move(0, 30000, 500)
          vehicle.move(0, 0, 500)
          vehicle.move(0, -30000, 500)
          vehicle.move(0, 0, 500)
        elif down == True:
          vehicle.move(30000, 0, 500)
          vehicle.move(0, 0, 500)
          vehicle.move(-30000, 0, 500)
          vehicle.move(0, 0, 500)    
        elif left == True:
          vehicle.move(30000, 30000, 500)
          vehicle.move(0, 0, 500)
          vehicle.move(30000, -30000, 500)
          vehicle.move(0, 0, 500)
        elif right == True:
          vehicle.move(0, 30000, 500)
          vehicle.move(0, 0, 500)
          vehicle.move(30000, 0, 500)
          vehicle.move(0, 0, 500)
          vehicle.move(0, -30000, 500)
          vehicle.move(0, 0, 500)
          vehicle.move(-30000, 0, 500)
          vehicle.move(0, 0, 500)     

    if radio.connection() == False:
        vehicle.move(0, 0)
