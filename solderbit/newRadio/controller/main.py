from microbit import *
import radio
import controller

group = 6

radio.config(group=group)
radio.on()   

while True:
    controller.oled.fill(0)
    controller.oled.text("Current group:", 10, 0)
    controller.oled.text(f"{group}", 60, 15)
    controller.oled.show()

    inputs = controller.read_all_inputs()
    data = controller.read_encoded()
    right = inputs[controller.R1_BTN]
    left = inputs[controller.L1_BTN]

    radio.send_bytes(data)
    sleep(50)
