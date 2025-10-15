from microbit import *

images = [Image.HEART, "Hello!", Image.HAPPY, "World!", Image.DUCK, "Have a nice day!", Image.SILLY]

while True:
    display.show(images, delay=500)