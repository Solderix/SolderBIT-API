from microbit import *
import radio
import controller

radio.config(group=7)
radio.on()   

while True:
    radio.send_bytes(controller.read_encoded())
    sleep(50)
