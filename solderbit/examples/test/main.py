from microbit import *
import radio

radio.config(group=5)
radio.on()

while True:
    msg = radio.receive()
    if msg:
        print(msg)
