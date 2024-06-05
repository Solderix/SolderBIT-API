from microbit import *
import radio
import vehicle

radio.on()
radio.config(group=42)

vehicle.engine_start()
vehicle.set_acceleration(0.2)
vehicle.set_speed(0.5)

previous_time = 0

while True:
    data = radio.receive()
    
    if data != None:
        previous_time = running_time() + 400
        controls = data.split('/')
        vehicle.move(int(controls[1])*65535, int(controls[0])*62)

    if running_time() > previous_time:
        vehicle.move(0, 0)
