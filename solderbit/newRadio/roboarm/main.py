from microbit import *
import radio
import srt as controller
import servo

servo.turn(3,90, True)
servo.turn(4,90, True)
servo.turn(5,110, True)

radio.config(group=10)
radio.on()

servo3_p = 0
servo3_m = 0

servo4_p = 0
servo4_m = 0

servo5_p = 0
servo5_m = 0

servo6_grip = 0

servo_states = [0,0,0,280,270,480,0]
next_time = 0

while True:
    data = controller.data_decode(radio.receive_bytes())
    
    if data != None:
        print(data)

        servo3_p = data[controller.LEFT_RIGHT_BTN]
        servo3_m = data[controller.LEFT_LEFT_BTN] * (-1)

        servo4_p = data[controller.LEFT_UP_BTN] * (-1)
        servo4_m = data[controller.LEFT_DOWN_BTN] 

        servo5_p = data[controller.RIGHT_UP_BTN] * (-1)
        servo5_m = data[controller.RIGHT_DOWN_BTN]

        if data[controller.RIGHT_RIGHT_BTN]:
            servo6_grip = 1
        elif data[controller.RIGHT_LEFT_BTN]:
            servo6_grip = -1
        else:
            servo6_grip = 0 

        if servo3_p+servo3_m != 0 or servo4_p+servo4_m != 0 or servo5_p+servo5_m != 0:
            next_time = running_time() + 10000 

    servo_states[3] += (servo3_p+servo3_m)
    servo_states[4] += (servo4_p+servo4_m) 
    servo_states[5] += (servo5_p+servo5_m)

    servo_states[3] = max(90, min(servo_states[3], 500))
    servo_states[4] = max(270, min(servo_states[4], 500))
    servo_states[5] = max(270, min(servo_states[5], 500))

    servo.turn(3, servo_states[3], False)
    servo.turn(4, servo_states[4], False)  
    servo.turn(5, servo_states[5], False)

    if servo6_grip == 1: 
        servo.turn(6, 90, False)

    if servo6_grip == -1 or next_time < running_time():
        servo.turn(6, 290, False)
        sleep(80)
        servo.turn(6,0,False)
        next_time = running_time() + 10000    

    sleep(4)  