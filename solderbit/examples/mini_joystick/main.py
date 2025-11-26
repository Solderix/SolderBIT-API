from microbit import *
import radio
import srt as controller

radio.config(group=8)
radio.on()

radio._sta.config(txpower=4)   # try 8 dBm (reduce further if needed)

while True:
    radio.check_connection()
    radio.send_bytes(controller.read_encoded())
    sleep(50)