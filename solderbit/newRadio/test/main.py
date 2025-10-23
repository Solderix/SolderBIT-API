from microbit import *
import radio
import cam
import vehicle
import srt as controller

data = None


radio.config(group=7)
radio.on()
cam.on()
cam.group(8)

while True:
  if not radio.check_connection():
    vehicle.move(0,0)
  data = controller.data_decode((radio.receive_bytes()))
  if data != None:
    vehicle.move((data[controller.JOY_X2]),(data[controller.JOY_Y1]))
    vehicle.horn((data[controller.X_BTN]))
