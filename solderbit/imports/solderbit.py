import machine
import esp
import time
start_time = time.time_ns()

CONNECTED_PIN = 45

class ButtonWrapper:
    def __init__(self, pin):
        self._button = machine.Pin(pin, machine.Pin.IN)
        self.count = 0
        self.pressed = False
    
    def handle_interrupt(self, pin):
        self.count += 1
        self.pressed = True
        
    def attach_interrupt(self):
        self._button.irq(trigger=machine.Pin.IRQ_RISING, handler = self.handle_interrupt)
        return self

    def is_pressed(self):
        tmp = self._button.value()
        if tmp is 1:
            return False
        else:
            return True
        
    def was_pressed(self):
        tmp = self.pressed
        self.pressed = False
        return tmp
        
    def get_pressed(self):
        tmp = self.count
        self.count = 0
        return tmp
        

class DisplayLED:
    def __init__(self):
        return
        
    def get_pixel(self,x,y):
        return
        
    def set_pixel(self,x,y):
        return
        
    def clear(self):
        return
        
    def show(self,image, delay=0, wait=True, loop=False, clear=False):
        return
        
    def show(self,iterable, delay=400, wait=True, loop=False, clear=False):
        return
        
    def scroll(self,string, delay=400):
        return


class MicroBitPin:
    def __init__(self, pin_num):
        self.pin = None
        self.pin_num = pin_num
        self.mode = 0
        self.pull_mode =  machine.Pin.PULL_UP
        self.is_pwm = False
    
    def read_digital(self):
        if self.mode != 3:
            self.pin = machine.Pin(self.pin_num, machine.Pin.IN, self.pull_mode)
            self.mode = 3
        
        return self.pin.value()
        
    def write_digital(self, value):     
        if self.mode != 4:
            self.pin = machine.Pin(self.pin_num, machine.Pin.OUT)
            self.mode = 4
    
        if value is 0:
            self.pin.off()
        elif value is 1:
            self.pin.on()
            
    def set_pull(self, value):
        self.pull_mode = value
        self.pin.init(self.mode, value)
        
    def get_pull(self):
        return self.pull_mode
        
    def get_mode(self):
        return self.mode
        
    def write_analog(self, value, freq=1000):
        if self.pin == None:
            self.pin = machine.PWM(machine.Pin(self.pin_num, machine.Pin.OUT))
            self.mode = 2
        
        if self.mode != 2:
            return 
        self.pin.duty(value)
        self.pin.freq(freq)
        return

    def read_analog(self):
        if self.mode != 1:
            self.pin = machine.ADC(self.pin_num, atten=machine.ADC.ATTN_11DB)
            self.mode = 1
        
        return self.pin.read_u16()

class MicroBitTouchPin():
    def __init__(self, pin_num):
        self.touch_pin = machine.TouchPad(machine.Pin(pin_num, mode=machine.Pin.IN))
    
    def is_touched(self):
        return True if self.touch_pin.read() < 20 else False
       
pin0 = MicroBitPin(6) #6 change to on new
pin1 = MicroBitPin(10)
pin2 = MicroBitPin(2)
pin3 = MicroBitPin(18)
pin4 = MicroBitPin(14)
pin5 = MicroBitPin(13)
pin6 = MicroBitPin(1)
pin7 = MicroBitPin(11)
pin8 = MicroBitPin(9)
pin9 = MicroBitPin(8)
pin10 = MicroBitPin(7)
pin11 = MicroBitPin(17) #17 change to on new
pin12 = MicroBitPin(5)
pin13 = MicroBitPin(36)
pin14 = MicroBitPin(37)
pin15 = MicroBitPin(35)
pin16 = MicroBitPin(1)
pin19 = MicroBitPin(4)
pin20 = MicroBitPin(3)

class Image:
    def __init__(self,width=None, height=None, buffer=None):
        return
    
    def width(self):
        return
    
    def height():
        return
    
    def set_pixel(self, x, y, value):
        return
    
    def get_pixel(self, x, y):
        return
    
    def shift_left(self, n):
        return
    
    def shift_right(self, n):
        return
    
    def shift_up(self, n):
        return
    
    def shift_down(self, n):
        return
    
    def crop(self,x,y,w,h):
        return
    
    def copy(self):
        return
    
    def invert(self):
        return
    
    def fill(self, value):
        return
    
    def blit(self, src, x, y, w, h, xdest=0, ydest=0):
        return

sda = MicroBitPin(21)
scl = MicroBitPin(38)

class I2C:
    def __init__(self,freq, sda, scl):
        self.i2c = machine.SoftI2C(machine.Pin(20), machine.Pin(19))

    def scan(self):
        return self.i2c.scan()  

    def read(self, addr, n, repeat=False):
        return self.i2c.readfrom(addr, n, repeat)    

    def write(self, addr, buf, repeat=True):
        self.i2c.writeto(addr, buf, repeat) 


def sleep(ms):
    time.sleep_ms(ms)
    

def running_time():
    return int((time.time_ns()-start_time)/1000000)

  
def temperature():
    return esp.raw_temperature()
    
    
def panic(error_code):
    return


def scale(value_to_convert, from_=(0, 100), to=(0, 1)):
    from_min, from_max = from_
    to_min, to_max = to
    scaled_value = (value_to_convert - from_min) * (to_max - to_min) / (from_max - from_min) + to_min
    return scaled_value


def reset():
    machine.reset()


device = 0x53
regAddress = 0x32
TO_READ = 6
buff = bytearray(6)
in_range = lambda val,base,offset: ((base-offset) <= val <= (base+offset))

class ADXL345:
    def __init__(self,i2c,addr=device):
        self.addr = addr
        self.i2c = i2c
        self.gesture = "face up"
        self.gesture_list = []
        b = bytearray(1)
        b[0] = 0
        self.i2c.writeto_mem(self.addr,0x2d,b)
        b[0] = 16
        self.i2c.writeto_mem(self.addr,0x2d,b)
        b[0] = 8
        self.i2c.writeto_mem(self.addr,0x2d,b)

    def get_x(self):
        buff = self.i2c.readfrom_mem(self.addr,regAddress,TO_READ)
        x = (int(buff[1]) << 8) | buff[0]
        if x > 32767:
            x -= 65536
        return x
   
    def get_y(self):
        buff = self.i2c.readfrom_mem(self.addr,regAddress,TO_READ)
        y = (int(buff[3]) << 8) | buff[2]
        if y > 32767:
            y -= 65536
        return y
     
    def get_z(self): 
        buff = self.i2c.readfrom_mem(self.addr,regAddress,TO_READ)
        z = (int(buff[5]) << 8) | buff[4]
        if z > 32767:
            z -= 65536
        return z

    def get_values(self):
        out = (self.get_x(), self.get_y(), self.get_z())
        return out
           
    def current_gesture(self):
        x = self.get_x()
        y = self.get_y()
        z = self.get_z()
        offset = 50

        if in_range(x, 0,offset) and in_range(y, 0,offset) and in_range(z, -210,offset):
            self.gesture = "face up"
        elif in_range(x, -245,offset) and in_range(y, 10,offset) and in_range(z, 10,offset):
            self.gesture = "down"
        elif in_range(x, 270,offset) and in_range(y, 10,offset) and in_range(z, 70,offset):
            self.gesture = "up"
        elif in_range(x, 30,offset) and in_range(y, 260,offset) and in_range(z, 20,offset):
            self.gesture = "right"
        elif in_range(x, 30,offset) and in_range(y, -250,offset) and in_range(z, 30,offset):
            self.gesture = "left"
        elif in_range(x, 15,offset) and in_range(y, 25,offset) and in_range(z, 280,offset):
            self.gesture = "face down"
        #TO DO: add other gestures
            
        self.gesture_list.append(self.gesture)
        return self.gesture
    
    def is_gesture(self, name):
        out = (self.current_gesture() == name)
        return out
    
    def was_gesture(self):
        return self.gesture
    
    def get_gestures(self):
        return tuple(self.gesture_list)
    

class Compass:
    def __init__(self) -> None:
        pass

    def calibrate(self):
        return
    
    def heading(self):
        return
    
    def get_field_strength(self):
        return
    
    def is_calibrated(self):
        return
    
    def clear_calibration(self):
        return


class SolderI2C:
    def __init__(self,sda,scl) -> None:
        self.i2c = machine.I2C(1, sda=machine.Pin(sda), scl=machine.Pin(scl))
        pass

    def read(self, addr, n, repeat=False):
        return self.i2c.readfrom(addr,n,repeat)

    def write(self, addr, buf, repeat=False):
        self.i2c.writeto(addr,buf,repeat)

    def scan(self):
        return self.i2c.scan()


button_a = ButtonWrapper(15).attach_interrupt()
button_b = ButtonWrapper(0).attach_interrupt()
display = DisplayLED()

HEART = Image()
HEAERT_SMALL = Image()
HAPPY = Image()
SAD = Image()
CONFUSED = Image()
ANGRY = Image()
ASLEEP = Image()
SUPRISED = Image()
SILLY = Image()
FABULUS = Image()
MEH= Image()
YES= Image()
CLOCK12= Image()
CLOCK11= Image()
CLOCK10= Image()
CLOCK9= Image()
CLOCK8= Image()
CLOCK7= Image()
CLOCK6= Image()
CLOCK5= Image()
CLOCK4= Image()
CLOCK3= Image()
CLOCK2= Image()
CLOCK1= Image()
ARROW_N= Image()
ARROW_NE= Image()
ARROW_E= Image()
ARROW_SE= Image()
ARROW_S= Image()
ARROW_SW= Image()
ARROW_W= Image()
ARROW_NW= Image()
TRIANGLE= Image()
TRIANGLE_LEFT= Image()
CHESSBOARD= Image()
DIAMOND= Image()
DIAMOND_SMALL= Image()
SQUARE= Image()
SQUARE_SMALL= Image()
RABBIT= Image()
COW= Image()
MUSIC_CROTCHET= Image()
MUSIC_QUAVER= Image()
MUSIC_QUAVERS= Image()
PITCHFORK= Image()
XMAS= Image()
PACMAN= Image()
TARGET= Image()
TSHIRT= Image()
ROLLERSKATES= Image()
DUCK= Image()
HOUSE= Image()
TORTOISE= Image()
BUTTERFLY= Image()
STICKFIGURE= Image()
GHOST= Image()
SWORD= Image()
GIRAFFE= Image()
SKULL= Image()
UMBRELLA= Image()
SNAKE= Image()
SCISSORS= Image()

ALL_CLOCKS = [CLOCK12, CLOCK11, CLOCK10, CLOCK9, CLOCK8, CLOCK7, CLOCK6, CLOCK5, CLOCK4, CLOCK3, CLOCK2, CLOCK1]
ALL_ARROWS = [ARROW_N, ARROW_NE,ARROW_E,ARROW_SE,ARROW_S,ARROW_SW,ARROW_W,ARROW_NW]

i2c_accel = machine.I2C(0, sda=machine.Pin(21), scl=machine.Pin(38))

#accel = ADXL345(i2c_accel, device)
accel_int = machine.Pin(48, machine.Pin.IN, machine.Pin.PULL_UP)
compass = Compass()

i2c = SolderI2C(3,4)
uart = machine.UART(0)

