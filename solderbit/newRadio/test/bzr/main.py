from microbit import *
import controller
import music

while True:  
    music.play("a", pin=controller.buzzer)
    sleep(1000)