from microbit import *
import radio
import controller

radio.on()

while True:
  radio.config(group=8)
  radio.check_connection()
  radio.send_bytes(controller.read_encoded())
  radio.config(group=7)
  radio.receive_video()
