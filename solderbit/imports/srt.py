from microbit import *
import struct

_controller_data_format = "4hi"

JOY_X1 = 0b0000
JOY_Y1 = 0b0001
JOY_X2 = 0b0010
JOY_Y2 = 0b0011
JOY1_BTN = 0b0100
JOY2_BTN = 0b0101
R1_BTN = 0b0110
L1_BTN = 0b0111
LEFT_UP_BTN = 0b1000
LEFT_DOWN_BTN = 0b1001
LEFT_RIGHT_BTN = 0b1010
LEFT_LEFT_BTN = 0b1011
RIGHT_UP_BTN = 0b1100
RIGHT_DOWN_BTN = 0b1101
RIGHT_RIGHT_BTN = 0b1110
RIGHT_LEFT_BTN = 0b1111

_J1X_OFFSET = 0
_J1Y_OFFSET = 0

for num in range(10):
    _J1X_OFFSET = _J1X_OFFSET + pin0.read_analog()
    _J1Y_OFFSET = _J1Y_OFFSET + pin1.read_analog()

_J1X_OFFSET = int(_J1X_OFFSET/10)
_J1Y_OFFSET = int(_J1Y_OFFSET/10)
    

def read_all_inputs():
    joy_x = min(1023>>1, max(-1023>>1, (pin1.read_analog() - _J1X_OFFSET) ))
    joy_y = min(1023>>1, max(-1023>>1, (pin0.read_analog() - _J1Y_OFFSET) ))
    joy_btn = not bool(pin13.read_digital())
    a_btn = not bool(pin15.read_digital())
    b_btn = not bool(pin14.read_digital())
    return [-joy_x, joy_y ,-joy_x,joy_y,joy_btn, joy_btn, a_btn, b_btn,False,False,False,False,False,False,False,False,False]


def read_encoded():
    output = bytearray()
    data_tmp = read_all_inputs()
    data = data_tmp[0:4]
    bools = 0
    for idx, value in enumerate(data_tmp[4:]):
        bools |= value<<idx 
    data.append(bools)
    output = struct.pack(_controller_data_format, *data)
    print(data_tmp)
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