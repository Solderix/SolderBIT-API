
from microbit import *
import radio
import srt as controller

radio.config(group=5)
radio.on()

while True:
    radio.send_bytes(controller.read_encoded())
    sleep(100)