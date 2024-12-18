from microbit import *
import radio
import controller

controller.init()

group = 5

radio.config(group=group)
radio.on()   

while True:
    controller.oled.fill(0)
    controller.oled.text("Current group:", 10, 0)
    controller.oled.text(f"{group}", 60, 15)
    controller.oled.show()

    inputs = controller.read_all_inputs()
    data = controller.read_encoded()
    right = inputs[controller.inputs.R1_BTN[0]]
    left = inputs[controller.inputs.L1_BTN[0]]
    if right == True:
        group += 1
        radio.config(group=group)

    if left == True:
        group -= 1
        radio.config(group=group)

    radio.send_bytes(data)
    sleep(100)
