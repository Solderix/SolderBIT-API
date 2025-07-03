from microbit import *
import controller

while True:
    data = controller.read_all_inputs()

    #print out few values
    print(data[controller.LEFT_LEFT_BTN], data[controller.LEFT_RIGHT_BTN], data[controller.LEFT_UP_BTN], data[controller.LEFT_DOWN_BTN])
    #or print the entire list
    print(data)

    sleep(1000)

