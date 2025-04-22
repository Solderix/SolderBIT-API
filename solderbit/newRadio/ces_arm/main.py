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
    for num in range(410):
        #servo.turn(3, num, True)
        servo.turn(5, 90+num, False)
        sleep(5)
    sleep(1000)
    for num in range(410):
        #servo.turn(3, 180-num, True)
        servo.turn(5, 500-num, False)
        sleep(5)
    sleep(1000)