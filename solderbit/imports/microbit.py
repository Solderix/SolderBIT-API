import machine
import esp
import time
import math
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

import framebuf2 as framebuf

try:
    import st7789
    tft = st7789.ST7789(
        machine.SPI(2, baudrate=60_000_000, sck=machine.Pin(18), mosi=machine.Pin(14)),
        128,
        160,
        reset=machine.Pin(46, machine.Pin.OUT),
        cs=machine.Pin(39, machine.Pin.OUT),
        dc=machine.Pin(16, machine.Pin.OUT),
        backlight=machine.Pin(47, machine.Pin.OUT),
        color_order=st7789.RGB,
        rotation=1,
        inversion=False)
    
    tft.init()
    tft.offset(1,2)
    tft.fill(st7789.BLACK)
except:
    tft = None
    print("TFT not found")


def swap_rgb565(color):
    return ((color & 0xFF) << 8) | ((color >> 8) & 0xFF)

class Image:
    def __init__(self,width=None, height=None, buffer=None):
        if isinstance(width, str):
            rows = width.split(':')
            self.height = len(rows)
            self.width = len(rows[0])
            self.buffer = [int(c) for row in width.split(':') for c in row]
    
    def width(self):
        return self.width
    
    def height(self):
        return self.height
    
    def set_pixel(self, x, y, value):
        return
    
    def get_pixel(self, x, y):
        return self.buffer[y*self.width + x]
    
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


Image.HEART = Image("09090:99999:99999:09990:00900")
Image.HEAERT_SMALL = Image("00000:09090:09990:00900:00000")
Image.HAPPY = Image("00000:09090:00000:90009:09990")
Image.SAD = Image("00000:09090:00000:09990:90009")
Image.CONFUSED = Image("00000:09090:00000:09090:90909")
Image.ANGRY = Image("90009:09090:00000:99999:90909")
Image.ASLEEP = Image("00000:99099:00000:09990:00000")
Image.SUPRISED = Image("09090:00000:00900:09090:00900")
Image.SILLY = Image("90009:00000:99999:00909:00999")
Image.FABULUS = Image("99999:99099:00000:09090:09990")
Image.MEH = Image("09090:00000:00090:00900:09000")
Image.YES = Image("00000:00009:00090:90900:09000")
Image.NO = Image("90009:09090:00900:09090:90009")
Image.CLOCK12 = Image("00900:00900:00900:00000:00000")
Image.CLOCK11 = Image("09000:09000:00900:00000:00000")
Image.CLOCK10 = Image("00000:99000:00900:00000:00000")
Image.CLOCK9 = Image("00000:00000:99900:00000:00000")
Image.CLOCK8 = Image("00000:00000:00900:99000:00000")
Image.CLOCK7 = Image("00000:00000:00900:09000:09000")
Image.CLOCK6 = Image("00000:00000:00900:00900:00900")
Image.CLOCK5 = Image("00000:00000:00900:00090:00090")
Image.CLOCK4 = Image("00000:00000:00900:00099:00000")
Image.CLOCK3 = Image("00000:00000:00999:00000:00000")
Image.CLOCK2 = Image("00000:00099:00900:00000:00000")
Image.CLOCK1 = Image("00090:00090:00900:00000:00000")
Image.ARROW_N= Image("00900:09990:90909:00900:00900")
Image.ARROW_NE= Image("00999:00099:00909:09000:90000")
Image.ARROW_E= Image("00900:00090:99999:00090:00900")
Image.ARROW_SE= Image("90000:09000:00909:00099:00999")
Image.ARROW_S= Image("00900:00900:90909:09990:00900")
Image.ARROW_SW= Image("00009:00090:90900:99000:99900")
Image.ARROW_W= Image("00900:09000:99999:09000:00900")
Image.ARROW_NW= Image("99900:99000:90900:00090:00009")
Image.TRIANGLE= Image("00000:00900:09090:99999:00000")
Image.TRIANGLE_LEFT= Image("90000:99000:90900:90090:99999")
Image.CHESSBOARD= Image("09090:90909:09090:90909:09090")
Image.DIAMOND= Image("00900:09090:90009:09090:00900")
Image.DIAMOND_SMALL= Image("00000:00900:09090:00900:00000")
Image.SQUARE= Image("99999:90009:90009:90009:99999")
Image.SQUARE_SMALL= Image("00000:09990:09090:09990:00000")
Image.RABBIT= Image("90900:90900:99990:99090:99990")
Image.COW= Image("90009:90009:99999:09990:00900")
Image.MUSIC_CROTCHET= Image("00900:00900:00900:99900:99900")
Image.MUSIC_QUAVER= Image("00900:00990:00909:99900:99900")
Image.MUSIC_QUAVERS= Image("09999:09009:09009:99099:99099")
Image.PITCHFORK= Image("90909:90909:99999:00900:00900")
Image.XMAS= Image("00900:09990:00900:09990:99999")
Image.PACMAN= Image("09999:99090:99900:99990:09999")
Image.TARGET= Image("00900:09990:99099:09990:00900")
Image.TSHIRT= Image("99099:99999:09990:09990:09990")
Image.ROLLERSKATES= Image("00099:00099:99999:99999:09090")
Image.DUCK= Image("09900:99900:09999:09990:00000")
Image.HOUSE= Image("00900:09990:99999:09990:09090")
Image.TORTOISE= Image("00000:09990:99999:09090:00000")
Image.BUTTERFLY= Image("99099:99999:00900:99999:99099")
Image.STICKFIGURE= Image("00900:99999:00900:09090:90009")
Image.GHOST= Image("99999:90909:99999:99999:90909")
Image.SWORD= Image("00900:00900:00900:09990:00900")
Image.GIRAFFE= Image("99000:09000:09000:09990:09090")
Image.SKULL= Image("09990:90909:99999:09990:09990")
Image.UMBRELLA= Image("09990:99999:00900:90900:09900")
Image.SNAKE= Image("99000:99099:09090:09990:00000")
Image.SCISSORS= Image("")

Image.ALL_CLOCKS = [Image.CLOCK12, Image.CLOCK11, Image.CLOCK10, Image.CLOCK9, Image.CLOCK8, Image.CLOCK7, Image.CLOCK6, Image.CLOCK5, Image.CLOCK4, Image.CLOCK3, Image.CLOCK2, Image.CLOCK1]
Image.ALL_ARROWS = [Image.ARROW_N, Image.ARROW_NE, Image.ARROW_E, Image.ARROW_SE, Image.ARROW_S, Image.ARROW_SW, Image.ARROW_W, Image.ARROW_NW]

Image.BLACK = 0x0000
Image.WHITE = 0xFFFF
Image.RED =  0xF800
Image.GREEN = 0x07E0
Image.BLUE = 0x001F
Image.YELLOW = 0xFFE0
Image.CYAN = 0x07FF
Image.MAGENTA = 0xF81F
Image.ORANGE = 0xFD20
Image.PINK = 0xF81F

class DisplayLED:
    def __init__(self, width=160, height=128, depth=2, additional_bytes=0, pages=1):
        self.my_cb = None
        self.width = width
        self.height = height
        self.buffer = bytearray( (self.width * int(self.height//pages) * depth) + additional_bytes)
        if depth == 1:
            self.fb = framebuf.FrameBuffer(self.buffer, self.width, self.height, framebuf.MONO_VLSB)
        elif depth == 2:
            self.fb = framebuf.FrameBuffer(self.buffer, self.width, self.height, framebuf.RGB565)
        
    def get_pixel(self,x,y):
        return self.fb.pixel(x,y)
        
    def set_pixel(self,x,y):
        return
        
    def clear(self):
        self.fb.fill(0)
        return
        
        
    def show(self, iterable, delay=400, wait=True, loop=False, clear=True, width=0, height=0, x=0, y=0, color=Image.BLACK):
        if isinstance(iterable, bytearray):
            if width == 0:
                width = 160
            if height == 0:
                height = 128
            self._blit_cb(x, y, width, height)
            return

        if isinstance(iterable, (list, tuple)):
            for item in iterable:
                self.show(item, delay=delay, wait=wait, loop=loop, clear=clear, width=width, height=height, x=x, y=y, color=color)
            return

        if clear:
            self.fb.fill(0x0000)

        if isinstance(iterable, Image):
            scale = int((self.height*0.78)/ iterable.width) if iterable.width > iterable.height else int((self.height*0.78)/ iterable.height)
            offset_x = (self.width - (iterable.width * scale)) // 2
            offset_y = (self.height - (iterable.height * scale)) // 2
            color_list = [Image.BLACK, Image.RED, Image.GREEN, Image.BLUE, Image.YELLOW, Image.CYAN, Image.MAGENTA, Image.ORANGE, Image.PINK, Image.WHITE]

            for y in range(iterable.height):
                for x in range(iterable.width):
                    if color != Image.BLACK:
                        color_pix = bool(iterable.get_pixel(x, y)) * swap_rgb565(color)
                    else:
                        color_pix = swap_rgb565(color_list[iterable.get_pixel(x, y)])

                    for dy in range(scale):
                        for dx in range(scale):
                            self.fb.pixel(offset_x + (x * scale + dx),
                                    offset_y + (y * scale + dy),
                                    color_pix)

            self._blit_cb(0, 0, display.height, display.width)
            sleep(delay)
            return
        
        string = str(iterable)
        x = -1
        size = 6
        flag = 0

        while x < 0:
            size -= 1
            x = (self.width/2) - (len(string) * 8 * size) / 2

        if size < 2:
            flag = 1
            size = 2
            x = 0

        y = int((self.height/2) - (8 * size) / 2)
        end = self.width - (len(string) * 8 * size)
        self.fb.large_text(string, int(x), y, size, swap_rgb565(Image.WHITE if color == Image.BLACK else color))
        self._blit_cb(0, 0, display.height, display.width)
        sleep(delay)

        while flag:
            if clear:
                self.fb.fill(0x0000)
            self.fb.large_text(string, int(x), y, size, swap_rgb565(Image.WHITE if color == Image.BLACK else color))
            self._blit_cb(0, 0, display.height, display.width)
            x -= 2
            if x < end:
                return
            sleep(1)


    def scroll(self,string, delay=400, color=Image.WHITE):
        x = self.width
        string = str(string)
        end = -len(string) * 10 * 5 
        while True:
            self.fb.fill(0x0000)                     
            self.fb.large_text(string, x, 48, 5, swap_rgb565(color))
            self._blit_cb()
            x -= 2
            if x < end:           
                return
            sleep(int(delay/10))

    def _set_blit_cb(self, my_cb):
        if my_cb == None:
            return
        self.my_cb = my_cb

    def _blit_cb(self, x, y, width, height):
        if self.my_cb == None:
            return
        self.my_cb(x, y, width, height)


display = DisplayLED()
display._set_blit_cb(lambda x, y, width, height: tft.blit_buffer(display.buffer, x, y, width, height))

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
        
    def write_analog(self, value):
        if self.mode != 2:
            self.pin = machine.PWM(machine.Pin(self.pin_num, machine.Pin.OUT))
            self.mode = 2
            return 
        
        value = int(min(1023, max(0, value)))
        self.pin.duty(value)
        return
    
    def set_analog_period(self, period):
        if self.mode != 2:
            self.pin = machine.PWM(machine.Pin(self.pin_num, machine.Pin.OUT))
            self.mode = 2
        
        freq = int(1000 / period)
        self.pin.freq(freq)
        return
    
    def set_analog_period_microseconds(self, period):
        if self.mode != 2:
            self.pin = machine.PWM(machine.Pin(self.pin_num, machine.Pin.OUT))
            self.mode = 2

        freq = int(1000000 / period)
        self.pin.freq(freq)
        return

    def read_analog(self):
        if self.mode != 1:
            self.pin = machine.ADC(self.pin_num, atten=machine.ADC.ATTN_11DB)
            self.mode = 1
        
        return (self.pin.read_u16() >> 6)   #Scales 16bit value to 10bit value

class MicroBitTouchPin():
    def __init__(self, pin_num):
        self.touch_pin = machine.TouchPad(machine.Pin(pin_num, mode=machine.Pin.IN))
    
    def is_touched(self):
        return True if self.touch_pin.read() < 20 else False
       
pin0 = MicroBitPin(6)
pin1 = MicroBitPin(10)
pin2 = MicroBitPin(2)
pin3 = MicroBitPin(18)
pin4 = MicroBitPin(14)
pin5 = MicroBitPin(13)
pin6 = MicroBitPin(12)
pin7 = MicroBitPin(11)
pin8 = MicroBitPin(9)
pin9 = MicroBitPin(8)
pin10 = MicroBitPin(7)
pin11 = MicroBitPin(17) 
pin12 = MicroBitPin(5)
pin13 = MicroBitPin(36)
pin14 = MicroBitPin(37)
pin15 = MicroBitPin(35)
pin16 = MicroBitPin(1)
pin19 = MicroBitPin(4)
pin20 = MicroBitPin(3)
connected_led = MicroBitPin(CONNECTED_PIN)

sda = MicroBitPin(21)
scl = MicroBitPin(38)

class I2C:
    def __init__(self,freq, sda, scl):
        self.i2c = machine.SoftI2C(machine.Pin(20), machine.Pin(19), freq=100_000)

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


device = 0b1001100
regAddress = 0x0B
TO_READ = 6
buff = bytearray(6)
in_range = lambda val,base,offset: ((base-offset) <= val <= (base+offset))

class ICM:
    def __init__(self,i2c,addr=device):
        self.addr = addr
        self.i2c = i2c
        self.gesture = "face up"
        self.gesture_list = []
        self.bits = 0
        b = bytearray(1)
        b[0] = 0x0F
        try:
            self.i2c.writeto_mem(self.addr, 0x1F, b)
        except:
            self.addr = 104
            self.i2c.writeto_mem(self.addr, 0x1F, b)
        sleep(1)
        b[0] = 0x05
        self.i2c.writeto_mem(self.addr, 0x21, b)

    def get_x(self):
        try:
            buff = self.i2c.readfrom_mem(self.addr,regAddress,TO_READ)
            x = (int(buff[0]) << 8) | buff[1]
            if x > 0x8000:
                x = x - 0x10000
            return x
        except:
            return 0
        
   
    def get_y(self):
        try:
            buff = self.i2c.readfrom_mem(self.addr,regAddress,TO_READ)
            y = (int(buff[2]) << 8) | buff[3]
            if y > 0x8000:
                y = y - 0x10000
            return y
        except:
            return 0
        
        
    def get_z(self): 
        try:
            buff = self.i2c.readfrom_mem(self.addr,regAddress,TO_READ)
            z = (int(buff[4]) << 8) | buff[5]
            if z > 0x8000:
                z = z - 0x10000
            return z
        except:
            return 0
        

    def get_values(self):
        out = (self.get_x(), self.get_y(), self.get_z())
        return out
    

    def get_strength(self):
        out = (self.get_x()**2 + self.get_y()**2 + self.get_z()**2)
        return out
    

    def set_range(self, value):
        values = {2:3, 4:2, 8:1, 16:0}
        self.bits = values.get(value,0)
        self.i2c.writeto_mem(self.addr, 0x21, bytearray([ (self.bits<<5) | 0x05 ]))

           
    def current_gesture(self):
        x = self.get_x(); y = self.get_y(); z = self.get_z()

        one_g = 2000.0 / (1 << self.bits)

        alpha = 0.18            # smoothing
        dom_frac = 0.70         # axis must be > dom_frac * mag
        shake_thresh = 1.4 * one_g
        hist_len = 8
        freefall_thresh = 0.6 * one_g

        # init persistent state
        if not hasattr(self, "_gs_lp"):
            self._gs_lp = ((x*x + y*y + z*z) ** 0.5)
        if not hasattr(self, "_gs_hist"):
            self._gs_hist = []

        # magnitude, smoothing (low-pass) and high-pass
        mag = (x*x + y*y + z*z) ** 0.5
        self._gs_lp += alpha * (mag - self._gs_lp)
        highpass = mag - self._gs_lp

        # history for recent deltas
        h = self._gs_hist
        max_delta = 0.0
        for v in h:
            d = mag - v
            if d < 0: d = -d
            if d > max_delta: max_delta = d
        h.append(mag)
        if len(h) > hist_len:
            h.pop(0)

        # 1) freefall
        if mag < freefall_thresh:
            self.gesture = "freefall"; return self.gesture

        # 2) high-g (check highest first)
        if mag > 9 * one_g:
            self.gesture = "9g"; return self.gesture
        if mag > 6 * one_g:
            self.gesture = "6g"; return self.gesture
        if mag > 3 * one_g:
            self.gesture = "3g"; return self.gesture

        # 3) shake detection (sudden changes)
        if abs(highpass) > shake_thresh or max_delta > shake_thresh:
            self.gesture = "shake"; return self.gesture

        # 4) orientation — require dominant axis
        if mag > 0:
            if abs(z) > dom_frac * mag:
                self.gesture = "face down" if z > 0 else "face up"; return self.gesture
            if abs(y) > dom_frac * mag:
                self.gesture = "up" if y > 0 else "down"; return self.gesture
            if abs(x) > dom_frac * mag:
                self.gesture = "right" if x > 0 else "left"; return self.gesture

        # fallback
        self.gesture = "unknown"
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
    def __init__(self,sda,scl,frq=100000) -> None:
        self.i2c = machine.I2C(1, sda=machine.Pin(sda, machine.Pin.OUT, machine.Pin.PULL_UP), scl=machine.Pin(scl, machine.Pin.OUT, machine.Pin.PULL_UP),freq=frq)
        pass

    def read(self, addr, n, repeat=False):
        try:
            return self.i2c.readfrom(addr,n,repeat)
        except:
            print("I2C failed")
            return 0

    def write(self, addr, buf, repeat=False):
        try:
            self.i2c.writeto(addr,buf,repeat)
        except:
            print("I2C failed")

    def scan(self):
        try:
            return self.i2c.scan()
        except:
            print("I2C failed")
            return 0


button_a = ButtonWrapper(15).attach_interrupt()
button_b = ButtonWrapper(0).attach_interrupt()

i2c_accel = machine.I2C(0, sda=machine.Pin(38), scl=machine.Pin(21))

try:
    accelerometer = ICM(i2c_accel, 105)
    print("Acc ready")
except:
    print("Accelerometer not found!")

accel_int = machine.Pin(48, machine.Pin.IN, machine.Pin.PULL_UP)
compass = Compass()

i2c = SolderI2C(3,4)
#uart = machine.UART(0)