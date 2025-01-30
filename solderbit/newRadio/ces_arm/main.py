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
    servo.turn(3, 280, False)
    servo.turn(4, 270, False)  
    servo.turn(5, 480, False)
    servo.turn(6,0,False)
    sleep(10000)
    servo.turn(3, 90, False)
    servo.turn(4, 270, False)  
    servo.turn(5, 480, False)
    servo.turn(6,0,False)
    sleep(2000)
    servo.turn(3, 90, False)
    servo.turn(4, 450, False)  
    servo.turn(5, 330, False)
    servo.turn(6,0,False)
    sleep(2000)
    servo.turn(6,90,False)
    sleep(2000)
    servo.turn(3, 480, False)
    servo.turn(4, 270, False)  
    servo.turn(5, 480, False)
    sleep(2000)
    servo.turn(3, 480, False)
    servo.turn(4, 450, False)  
    servo.turn(5, 320, False)
    sleep(2000)
    servo.turn(6,290,False)
    sleep(1000)