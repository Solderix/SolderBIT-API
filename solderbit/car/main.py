

from solderbit import *
from radio import *
import vehicle
import controller

devices = radio.on(PERIPHERAL_MODE)

vehicle.engine_start()
vehicle.set_acceleration(0.4)
vehicle.set_speed(1.0)

while True:
    data = controller.data_decode(radio.receive_bytes())

    if data != None:
        vehicle.move(data[2], data[1])

    if radio.connection() == False:
        vehicle.move(0, 0)
