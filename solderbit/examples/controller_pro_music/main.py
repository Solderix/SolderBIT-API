from microbit import *
import controller
import music

while True:
  data = controller.read_all_inputs()

  if data[controller.UP_BTN]:
    music.pitch(440, pin=controller.buzzer, duration=300, wait=False)
  elif data[controller.RIGHT_BTN]:
    music.pitch(493, pin=controller.buzzer, duration=300, wait=False)
  elif data[controller.DOWN_BTN]:
    music.pitch(523, pin=controller.buzzer, duration=300, wait=False)
  elif data[controller.LEFT_BTN]:
    music.pitch(587, pin=controller.buzzer, duration=300, wait=False)
  elif data[controller.Z_BTN]:
    music.pitch(659, pin=controller.buzzer, duration=300, wait=False)
  elif data[controller.Y_BTN]:
    music.pitch(698, pin=controller.buzzer, duration=300, wait=False)
  elif data[controller.X_BTN]:
    music.pitch(739, pin=controller.buzzer, duration=300, wait=False)
  elif data[controller.W_BTN]:
    music.pitch(880, pin=controller.buzzer, duration=300, wait=False)
  else:
    music.stop(pin=controller.buzzer)
