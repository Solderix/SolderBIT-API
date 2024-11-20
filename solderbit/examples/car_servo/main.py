from solderbit import *
from ble import *
import vehicle
import controller
import servo

devices = radio.on(PERIPHERAL_MODE)

vehicle.engine_start()
vehicle.set_acceleration(1.0)
vehicle.set_speed(1.0)
servo.init()

horn = False

while True:
    data = controller.data_decode(radio.receive_bytes())

    if data != None:
        vehicle.move(data[1], 0)
        horn = data[controller.inputs.L1_BTN[0]]
        servo.turn(3, scale(data[2], (-65535, 65535), (35,135)), True)

    if horn == True:
        vehicle.horn(1)
    else:
        vehicle.horn(0)

    if radio.connection() == False:
        vehicle.move(0, 0)
