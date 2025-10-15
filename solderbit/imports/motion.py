from microbit import *

class ICM_Gyro:
    def __init__(self, i2c, addr=105):
        self.i2c = i2c
        self.addr = addr
        b = bytearray(1)
        b[0] = 0x0F
        try:
            self.i2c.writeto_mem(self.addr, 0x20, b)
        except:
            try:
                self.addr = 104
                self.i2c.writeto_mem(self.addr, 0x6B, bytearray([0x00]))
            except:
                pass

   
    def get_x(self):
        buff = self.i2c.readfrom_mem(self.addr,0x11,TO_READ)
        x = (int(buff[0]) << 8) | buff[1]
        if x > 0x8000:
            x = x - 0x10000
        return x
   

    def get_y(self):
        buff = self.i2c.readfrom_mem(self.addr,0x11,TO_READ)
        y = (int(buff[2]) << 8) | buff[3]
        if y > 0x8000:
            y = y - 0x10000
        return y
   
     
    def get_z(self): 
        buff = self.i2c.readfrom_mem(self.addr,0x11,TO_READ)
        z = (int(buff[4]) << 8) | buff[5]
        if z > 0x8000:
            z = z - 0x10000
        return z
    

    def get_values(self):
        out = (self.get_x(), self.get_y(), self.get_z())
        return out
    

    def set_range(self, value):
        values = {250:3, 500:2, 1000:1, 2000:0}
        self.bits = values.get(value,0)
        self.i2c.writeto_mem(self.addr, 0x21, bytearray([ (self.bits<<5) | 0x05 ]))

try:
    acceleration = ICM(i2c.i2c, 105)
except:
    pass

rotation = ICM_Gyro(i2c.i2c, 105)