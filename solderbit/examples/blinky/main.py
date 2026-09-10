from microbit import *


while True:
  connected_led.write_digital(1)
  sleep(100)
  connected_led.write_digital(0)
  sleep(100)
