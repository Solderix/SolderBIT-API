
       
from solderbit import *
from radio import *
import controller

radio.on(CENTRAL_MODE)

def search_for_devices():
    device = None
    while device == None:
        device = controller.show_devices(radio.get_devices())
        controller.power_down()
    radio.connect(device)
    sleep(2000)    

def controller_logic():
    if radio.connection() == False:
        search_for_devices()
    else:
        #print(controller.read_all_inputs())
        radio.send_bytes(controller.read_encoded())
        if controller.power_button.read_digital() == True:
            radio.disconnect()
        sleep(100)
        controller.power_down()

controller.init()
while True:
    controller_logic()
