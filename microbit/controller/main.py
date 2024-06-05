# Imports go at the top
from microbit import *
import radio

radio.on()
radio.config(group=42)

# Code in a 'while True:' loop repeats forever
while True:
    vertical = accelerometer.get_y()
    horizontal = button_a.is_pressed() + (button_b.is_pressed()*(-1))
    
    if vertical < 300 and vertical >= 0:
        vertical = 0
    elif vertical > -300 and vertical < 0:
        vertical = 0

    message = "{}/{}".format(vertical, horizontal)
    print(message)
    radio.send(message)  # Ensure the message is sent over the radio

    sleep(150)
    
