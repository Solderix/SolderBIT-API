import sdcard
from machine import *
import vfs
from microbit import *
import radio
import controller

p = PWM(Pin(40))
p.freq(440)        
p.duty_u16(32768) 
sleep(500)
p.duty_u16(0)   
sleep(500)

spi = SPI(1,sck=machine.Pin(36), mosi=Pin(35), miso=Pin(37))
sd = sdcard.SDCard(spi, cs=Pin(42))
vfs.mount(sd,'/sd')

try:
    with open('/sd/test.txt', 'w') as f:
        f.write('Hello, SD Card!')
    display.show("SDW", delay=0)
    sleep(1000)

    with open('/sd/test.txt', 'r') as f:
        content = f.read()
        display.show(content, delay=0)
        sleep(1000)

except Exception as e:
    print("Error:", e)

spi.deinit()

while button_a.is_pressed() == False:
    display.fb.fill(0)
    (display.fb).large_text("x:" + str(accelerometer.get_x()),0,0,1,(Image.RED))
    (display.fb).large_text("y:" + str(accelerometer.get_y()),0,10,1,(Image.RED))
    (display.fb).large_text("z:" + str(accelerometer.get_z()),0,20,1,(Image.RED))
    (display.fb).large_text(accelerometer.current_gesture(), 0,30,1,(Image.RED))
    display.show(display.buffer, delay=0)
    sleep(50)


while button_a.is_pressed():
   pass

display.show("Press B", delay=0)
while not button_b.is_pressed():
   pass

display.show("B", delay=0)
sleep(250)

radio.on()

while True:
  pin15 = MicroBitPin(35)
  radio.config(group=8)
  radio.check_connection()
  radio.send_bytes(controller.read_encoded())
  radio.config(group=7)
  radio.receive_video()