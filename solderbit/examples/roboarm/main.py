from microbit import *
from ble import *
import controller
import servo

devices = radio.on(PERIPHERAL_MODE)

servos = [3,4,5]
servo_vals = [90,90,150]
is_moved = False
next_time = 0
speed = 10

servo.init()
servo.set(servos, servo_vals)
servo.turn(3,90, True)
servo.turn(4,90, True)
servo.turn(5,110, True)

def joint_move(joint, direction, is_moving):
    if is_moving == False:
        return
    
    global is_moved
    global servos
    global servo_vals

    servo_vals[joint] = servo_vals[joint] + direction
    if servo_vals[joint] < 0:
        servo_vals[joint] = 0
    elif servo_vals[joint] > 180:
        servo_vals[joint] = 180

    is_moved = True
    servo.set([servos[joint]], [servo_vals[joint]])


def move_speed(value,is_moving):
    if is_moving == False:
        return
    
    global speed

    speed = speed + value
    if speed < 1:
        speed = 1
    elif speed > 20:
        speed = 20


while True:
    data = controller.data_decode(radio.receive_bytes())
    if data != None:
        move_speed(1,data[controller.inputs.RIGHT_LEFT_BTN[0]])
        move_speed(-1,data[controller.inputs.RIGHT_RIGHT_BTN[0]])

        joint_move(1, speed, data[controller.inputs.LEFT_LEFT_BTN[0]])
        joint_move(1,-speed, data[controller.inputs.LEFT_RIGHT_BTN[0]])

        joint_move(0, speed, data[controller.inputs.LEFT_DOWN_BTN[0]])
        joint_move(0,-speed, data[controller.inputs.LEFT_UP_BTN[0]])

        joint_move(2, speed, data[controller.inputs.RIGHT_DOWN_BTN[0]])
        joint_move(2,-speed, data[controller.inputs.RIGHT_UP_BTN[0]])

        if is_moved == True:
            is_moved = False
            next_time = running_time() + 10000

        if data[controller.inputs.R1_BTN[0]] == True:
            servo.turn(6, 0, True)
            next_time = running_time() + 10000

        if data[controller.inputs.L1_BTN[0]] == True or next_time < running_time():
            servo.turn(6, 100, True)
            sleep(50)
            servo.write(6,0)
            next_time = running_time() + 10000

    servo.move_servos(servos, 5)