import framebuf
from microbit import *

class Config():
    width = 128
    height = 64
    pages = height // 8

config = Config()

temp = bytearray(2)
buffer = bytearray(((config.height // 8) * config.width) + 1)
buffer[0] = 0x40 
framebuf = framebuf.FrameBuffer1(memoryview(buffer)[1:], config.width, config.height)

def poweroff():
    write_cmd(0xae | 0x00)

def contrast(contrast):
    write_cmd(0x81)
    write_cmd(contrast)

def invert(invert):
    write_cmd(0xa6 | (invert & 1))

def show():
    x0 = 0
    x1 = config.width - 1
    if config.width == 64:
        x0 += 32
        x1 += 32
    write_cmd(0x21)
    write_cmd(x0)
    write_cmd(x1)
    write_cmd(0x22)
    write_cmd(0)
    write_cmd(config.pages - 1)
    write_framebuf()

def fill(col):
    framebuf.fill(col)

def pixel(x, y, col):
    framebuf.pixel(x, y, col)

def scroll(dx, dy):
    framebuf.scroll(dx, dy)

def text(string, x, y, col=1):
    framebuf.text(string, x, y, col)

def rotate(rot):
    if rot == 0:
        write_cmd(0xa0)
        write_cmd(0xc0)
    elif rot == 1:
        write_cmd(0xa0)
        write_cmd(0xc8)
    elif rot == 2:
        write_cmd(0xa1)
        write_cmd(0xc8)
    elif rot == 3:
        write_cmd(0xa1)
        write_cmd(0xc0)

def bitmap(buf,x,y,w,h):
    framebuf.blit(framebuf.FrameBuffer1(buf, w,h), x, y)

def line(x1, y1, x2, y2, c):
    framebuf.line(x1, y1, x2, y2, c)

def rect(x, y, w, h, c, fill=False):
    framebuf.rect(x, y, w, h, c, fill)

def circle(x, y, r, c, fill=False):
    framebuf.ellipse(x, y, r, r,c,fill)

def write_cmd(cmd):
    temp[0] = 0x80
    temp[1] = cmd
    i2c.write(0x3c, temp)

def write_framebuf():
    i2c.write(0x3c, buffer)

for cmd in (
    0xae, 0x20, 0x00, 0x40, 0xa1, 0xa8, config.height-1, 0xc8, 0xd3, 0x00, 0xda, 0x12, 0xd5, 0x80, 0xd9, 0xf1, 
    0xdb, 0x30, 0x81, 0xff, 0xa4, 0xa6, 0x8d, 0x14, 0xaf):
    write_cmd(cmd)

fill(0)
show()
rotate(0)