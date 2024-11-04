from microbit import *
import struct

_controller_data_format = "4hi"

JOY_Y = 1
JOY_X = 0
JOY_BTN = 4
A_BTN = 5
B_BTN = 6

_J1X_OFFSET = 0
_J1Y_OFFSET = 0
_offsets = []


class Inputs():
    JOY_X1 = (0b0000, True)
    JOY_Y1 = (0b0001, True)
    JOY_X2 = (0b0010, True)
    JOY_Y2 = (0b0011, True)
    JOY1_BTN = (0b0100, False)
    JOY2_BTN = (0b0101, False)
    R1_BTN = (0b0110, False)
    L1_BTN = (0b0111, False)
    LEFT_UP_BTN = (0b1000, False)
    LEFT_DOWN_BTN = (0b1001, False)
    LEFT_RIGHT_BTN = (0b1010, False)
    LEFT_LEFT_BTN = (0b1011, False)
    RIGHT_UP_BTN = (0b1100, False)
    RIGHT_DOWN_BTN = (0b1101, False)
    RIGHT_RIGHT_BTN = (0b1110, False)
    RIGHT_LEFT_BTN = (0b1111, False)
    controller_inputs = [JOY_X1, JOY_Y1, JOY_X2, JOY_Y2, JOY1_BTN, JOY2_BTN, R1_BTN, L1_BTN, LEFT_UP_BTN, LEFT_DOWN_BTN, LEFT_RIGHT_BTN, LEFT_LEFT_BTN, RIGHT_UP_BTN, RIGHT_DOWN_BTN, RIGHT_RIGHT_BTN, RIGHT_LEFT_BTN]

inputs = Inputs()

def _constrain(val, min_val, max_val) -> int:
    return min(max_val, max(min_val, val))


def init():
    global _J1X_OFFSET
    global _J1Y_OFFSET
    global _offsets
    
    for num in range(10):
        _J1X_OFFSET = _J1X_OFFSET + pin0.read_analog()
        _J1Y_OFFSET = _J1Y_OFFSET + pin1.read_analog()

    _J1X_OFFSET = int(_J1X_OFFSET/10)
    _J1Y_OFFSET = int(_J1Y_OFFSET/10)

    _offsets.append(_J1X_OFFSET)
    _offsets.append(_J1Y_OFFSET)


def read_all_inputs():
    joy_x = pin1.read_analog() - _offsets[0]
    joy_x = _constrain(joy_x, -1023>>1, 1023>>1)
    joy_y = pin0.read_analog() - _offsets[1]
    joy_y = _constrain(joy_y, -1023>>1, 1023>>1)

    joy_btn = not bool(pin13.read_digital())
    a_btn = not bool(pin15.read_digital())
    b_btn = not bool(pin14.read_digital())

    return [-joy_x, joy_y ,-joy_x,joy_y,joy_btn, joy_btn, a_btn, b_btn,False,False,False,False,False,False,False,False,False]


def read_encoded():
    output = bytearray()
    data_tmp = read_all_inputs()
    data = data_tmp[0:4]
    bools = _pack_bools(data_tmp)
    data.append(bools)
    output = struct.pack(_controller_data_format, *data)
    print(data_tmp)
    return output


def data_decode(data):
    if data == None:
        return None
    
    data = list(struct.unpack(_controller_data_format, data))
    decoded_data = data[0:4]
    decoded_data += _unpack_bools(data[4])
    return decoded_data


def _pack_bools(data) -> int:
    output = 0
    for idx, value in enumerate(data[4:]):
        output |= value<<idx 
    return output 


def _unpack_bools(data):
    output = []
    for num in range(12):
        output.append(bool((data>>num)&1))
    return output 