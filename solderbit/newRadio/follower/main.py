from microbit import *
import vehicle




while True:
  vehicle.move(0,1000)
  sleep(100)
  vehicle.move(0,-1000)
  sleep(100)