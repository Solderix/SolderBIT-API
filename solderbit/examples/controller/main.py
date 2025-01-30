from microbit import *
import radio
import controller


radio.config(group=5)
radio.on()   

while True:
    data = controller.read_encoded()
    radio.send_bytes(data)
    print(data)
    sleep(100)
