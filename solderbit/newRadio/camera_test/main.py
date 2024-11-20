from microbit import *

addr = 77

RHR_THR_REG = 0x00
IEF_REG = 0x01
FCR_IIR_REG = 0x02
LCR_REG = 0x03
MCR_REG = 0x04
LSR_REG = 0x05
MSR_REG = 0x06
SPR_REG = 0x07
TXLVL_REG = 0x08
RXLVL_REG = 0x09
IODIR_REG = 0x0a
IOSTATE_REG = 0x0b
IOINTENA_REG = 0x0c
IOCONTROL_REG = 0x0e
EFCR_REG = 0x0f

DLL_REG = 0x00
DLH_REG = 0x01

reg = lambda x: (x<<3)

data = bytearray([reg(LCR_REG), 0x80])
i2c.write(addr,data)
sleep(1)

data = bytearray([reg(DLH_REG), 0])
i2c.write(addr,data)
sleep(1)

data = bytearray([reg(DLL_REG), 6])
i2c.write(addr,data)
sleep(1)

data = bytearray([reg(FCR_IIR_REG), 0x07])
i2c.write(addr,data)

data = bytearray([reg(LCR_REG), 0x00000011])
i2c.write(addr,data)
sleep(1)


bruh = 0
while True:
    bruh += 1
    i2c.write(77, bytearray([reg(RHR_THR_REG), bruh]), False)
    sleep(1)

    i2c.write(77, bytearray([reg(FCR_IIR_REG)]), True)
    sleep(1)
    data = i2c.read(77, 1)
    print(bin(data[0]))
    sleep(1000)