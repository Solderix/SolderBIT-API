from microbit import *
import follower
import vehicle

while not button_a.is_pressed():
    print("Press button A to start")
    sleep(1000)
    
vehicle.move(x=0, y=300)

while True:
    direction = 0
    if follower.read(0) < 0.01:
        direction = -1
    elif follower.read(3) < 0.01:
        direction = 1

    vehicle.move(x=direction*500, y=300)