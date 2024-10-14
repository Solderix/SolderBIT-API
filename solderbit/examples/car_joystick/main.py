#Paketi potrebni za rad skripte
from solderbit import *
from radio import *
import vehicle
import controller

#Palimo radio u periferalnom načinu rada. Ovaj način rada javlja drugim uređajima da ima servis koji nudi.
radio.on(PERIPHERAL_MODE)

#Omogućuje rad elektromotora na uređaju
vehicle.engine_start()
#postavljanje maksimalne akceleracije
vehicle.set_acceleration(0.4)
#Postavljanje maksimalne brzine
vehicle.set_speed(1.0)

#Postavljanje početnih vrijednosti za trubu i svijetlo
horn = False
light = False

while True:
    data = controller.data_decode(radio.receive_bytes())
    
    if data != None:
        x = data[controller.inputs.JOY_X2[0]]
        y = data[controller.inputs.JOY_Y1[0]]
        light = data[controller.inputs.R1_BTN[0]]
        horn = data[controller.inputs.L1_BTN[0]]
        vehicle.move(x, y)

    if horn == True:
        vehicle.horn(1)
    else:
        vehicle.horn(0)

    if light == True:
        vehicle.set_outputs(connect=1)
    else:
        vehicle.set_outputs(connect=0)
    
    if radio.connection() == False:
        vehicle.move(0, 0)
