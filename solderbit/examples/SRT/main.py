
from microbit import *
from ble import *
import srt as controller

radio.on(CENTRAL_MODE)
controller.init()

device = []
while device == []:
    device = radio.get_devices()
radio.connect(device[0])

while True:
    radio.send_bytes(controller.read_encoded())
    sleep(100)