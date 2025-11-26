from microbit import *
import oled

images = None


images = ['Hello World!', Image("00000:09090:00000:90009:09990"), 1234567890]

while True:
  oled.screen.show(images, delay=500)
