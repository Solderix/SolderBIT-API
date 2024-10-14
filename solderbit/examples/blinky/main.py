from solderbit import *
import vehicle

while True:
    vehicle.set_outputs(connect = 1)
    sleep(1000)
    vehicle.set_outputs(connect = 0)
    sleep(1000)
