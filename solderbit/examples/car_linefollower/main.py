from microbit import *
import follower
import vehicle

while not button_a.was_pressed():
    print("Press button A to start")
    sleep(1000)
    
vehicle.move(x=0, y=0)

trigger_value = 0.012

while True:
    direction = 0
    if follower.read(0) < trigger_value:
        direction = 1
    elif follower.read(3) < trigger_value:
        direction = -1
    print(follower.read(0))
    vehicle.move(x=direction*300, y=0)