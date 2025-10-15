from microbit import *
import radio

led = radio.connected_led

while True:
    led.on()
    sleep(1000)
    led.off()
    sleep(1000)