from microbit import *
import radio
import vehicle
import servo
import oled

led = radio.connected_led
radio.on()
radio.config(group=8)

i = 0
while True:
    radio.check_connection()
    radio.send_bytes(b'Hello from SolderBIT!')
    radio.receive_bytes(True)

    if button_a.is_pressed():
        led.write_digital(1)

    if button_b.is_pressed():
        led.write_digital(1)
    
    vehicle.move(0,200)
    sleep(100)
    vehicle.move(0,-200)
    sleep(100)
    vehicle.move(0,0)

    servo.turn(servo.front, 90, False)
    servo.turn(servo.back, 90, False)  
    sleep(500)
    servo.turn(servo.front, 0, False)
    servo.turn(servo.back, 0, False)
    sleep(500)

    vehicle.set_outputs(connect = 0, l0 = 1)
    sleep(200)
    vehicle.set_outputs(connect = 1, l0 = 0)
    sleep(200)
    vehicle.set_outputs(connect = 0, l0 = 0)

    oled.screen.show(i, delay=100)
    i = i +1
    
    vehicle.horn(True)
    sleep(200)
    vehicle.horn(False)
    sleep(200)