
from microbit import *
from ble import *
import controller

radio.on(CENTRAL_MODE)

def search_for_devices():
    device = None
    while device == None:
        device = controller.show_devices(radio.get_devices())
    radio.connect(device)
    sleep(2000)    

def controller_logic():
    if radio.connection() == False:
        search_for_devices()
    else:
        print(controller.read_all_inputs())
        radio.send_bytes(controller.read_encoded())
        if controller.power_button.read_digital() == False:
            radio.disconnect()
        sleep(100)

while True:
    controller_logic()
