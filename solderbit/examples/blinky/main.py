from microbit import *
import radio

led = radio.connected_led

while True:
    led.write_digital(1)
    sleep(1000)
    led.write_digital(0)
    sleep(1000)