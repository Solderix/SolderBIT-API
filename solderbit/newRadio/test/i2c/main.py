from microbit import *

while True:
    display.fb.large_text("Blombo", 0, 0, 2, 0xFFFFFF)
    display.show(display.buffer, 0)
    sleep(1000)
