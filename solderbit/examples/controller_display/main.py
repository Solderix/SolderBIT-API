from microbit import *
import radio
import controller

radio.config(group=7)
radio.on()

while True:
    radio.check_connection()
    radio.config(group=7) #Group for camera
    radio.receive_video()

    radio.config(group=8) #Group for car
    radio.send_bytes(controller.read_encoded())