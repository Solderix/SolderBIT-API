from microbit import *
import struct

_controller_data_format = "4hi"

_J1X_OFFSET = 0
_J1Y_OFFSET = 0
_J2X_OFFSET = 0
_J2Y_OFFSET = 0
_offsets = []

JOY_X1 = 0b0000
JOY_Y1 = 0b0001
JOY_X2 = 0b0010
JOY_Y2 = 0b0011
JOY1_BTN = 0b0100
JOY2_BTN = 0b0101
R1_BTN = 0b0110
L1_BTN = 0b0111
UP_BTN = 0b1000
DOWN_BTN = 0b1001
LEFT_BTN = 0b1010
RIGHT_BTN = 0b1011
Z_BTN = 0b1100
X_BTN = 0b1101
W_BTN = 0b1110
Y_BTN = 0b1111

buzzer = pin13
center_button = pin14

def read_input(input, offset=True):
    pin = None
    value = input&1
    pin15.write_digital(value)

    value = (input>>1)&1
    pin8.write_digital(value)

    value = (input>>2)&1
    pin16.write_digital(value)

    value = (input>>3)&1
    #sleep(1)

    if value == 0:
        pin = pin0
    else:
        pin = pin1
    
    if input > 3:
        value =  not pin.read_digital()
    else:
        value = pin.read_analog() if offset is False else (int(pin.read_analog()) - _offsets[input&3])
        value = min(1023>>1, max(-1023>>1, value))

    return value


for num in range(10):
    _J1X_OFFSET = _J1X_OFFSET + read_input(JOY_X1, False)
    _J1Y_OFFSET = _J1Y_OFFSET + read_input(JOY_Y1, False)
    _J2X_OFFSET = _J2X_OFFSET + read_input(JOY_X2, False)
    _J2Y_OFFSET = _J2Y_OFFSET + read_input(JOY_Y2, False)

_J1X_OFFSET = int(_J1X_OFFSET/10)
_J1Y_OFFSET = int(_J1Y_OFFSET/10)
_J2X_OFFSET = int(_J2X_OFFSET/10)
_J2Y_OFFSET = int(_J2Y_OFFSET/10)

_offsets.append(_J1X_OFFSET)
_offsets.append(_J1Y_OFFSET)
_offsets.append(_J2X_OFFSET)
_offsets.append(_J2Y_OFFSET)
    

def read_all_inputs():
    output = []
    for input in range(16):
        output.append(read_input(input))
    return output


def read_encoded():
    output = bytearray()
    data_tmp = read_all_inputs()
    data = data_tmp[0:4]
    bools = 0
    for idx, value in enumerate(data_tmp[4:]):
        bools |= value<<idx 
    data.append(bools)
    output = struct.pack(_controller_data_format, *data)
    #print(data_tmp)
    return output


def data_decode(data):
    if data == None:
        return None
    
    data = list(struct.unpack(_controller_data_format, data))
    decoded_data = data[0:4]

    output = []
    for num in range(12):
        output.append(bool((data[4]>>num)&1))

    decoded_data += output

    return decoded_data


def buzzer_sound(tone, freq=None):
    buzzer.write_analog(tone)







    
