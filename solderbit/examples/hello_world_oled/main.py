from microbit import *
import oled

images = [Image.HEART, "Hello!", Image.HAPPY, "World!", Image.DUCK, "Have a nice day!", Image.SILLY]

while True:
    oled.screen.show(images, delay=500)