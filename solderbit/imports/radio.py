from machine import *
from microbit import *
import struct
import network
import espnow

_bpeer = b'\xff' * 6
_group = 0
_sta = network.WLAN(network.STA_IF)
_e = espnow.ESPNow()
_e.active(True)

connected_led = machine.Pin(CONNECTED_PIN, machine.Pin.OUT)
connected_led.off()

_esp_buffer = []
_esp_buffer_max = 15
_esp_buffer_counter = 0

_next_check = 0

mac_base = b'\x1a\x2b\x3c\x4e\x5f'


def check_connection():
    global _e

    is_connected = False
    if _next_check < running_time():
        connected_led.off()
        is_connected = False
    else:
        is_connected = True
        connected_led.on()
    return is_connected



def _recv_cb(e):
    global _esp_buffer_counter
    global _next_check
    while True:  
        mac, data = e.irecv(0)
        if mac is None:
            return
        
        if data == None:
            return
        
        _next_check = running_time() + 750

        if data == b'ACK':
            continue

        if _esp_buffer_counter < _esp_buffer_max:
            _esp_buffer_counter += 1
            _esp_buffer.append(data[:len(data)])

def on():
   global _sta
   global _e
   global _group
   
   group_mac = bytearray(mac_base)
   group_mac.append(_group)
   mac = bytes(group_mac)

   _sta.active(True)
   _e.active(True)
   _sta.config(mac=mac)

   for peer in _e.get_peers():
       _e.del_peer(peer[0])

   _e.add_peer(mac) 
   _e.irq(_recv_cb)


def off():
    global _sta
    global _e
    
    _sta.active(False)
    _e.active(False)
    connected_led.off()

def config(length=32, queue=3, channel=7, power=6, address=0x75626974, group=0, data_rate=0):
    global _group
    global _e
    _group = group
    
    for peer in _e.get_peers():
       _e.del_peer(peer[0])

    group_mac = bytearray(mac_base)
    group_mac.append(_group)
    mac = bytes(group_mac)
    _e.add_peer(mac) 
    return

def reset():
    off()

def send(message):
    send_bytes(message.encode())

def receive_bytes(confirm=False):
    global _e
    global _esp_buffer_counter
    global _esp_buffer
    
    if _esp_buffer_counter <= 0:
        return None

    _esp_buffer_counter -= 1
    if confirm == True:
        try:
            _e.send(None, b'ACK', True)
        except:
            print("Ack not sent")

    return _esp_buffer.pop()


def receive_bytes_into(buffer):
    return

def send_bytes(message):
    global _e
    try:
        _e.send(None, message, True)
    except:
        print("ERROR")
    return

def receive():
    return receive_bytes().decode("utf-8")

def receive_full():
    return

# Used for the pro version
try:
    image_end = bytearray([0xFF,0xFE,0xFE,0xFE])
    lost_counter = 0

    import jpeg

    def handle_image_data(img_data):
        send_bytes(b'\x01')
        _next_check = running_time()

        while True:
            data = receive_bytes()

            if (_next_check + 100) < running_time():
                return

            if data is None:
                continue

            if data[0:4] == image_end:
                break

            _next_check = running_time()
            img_data.extend(data)
            send_bytes(b'\x01')

    def receive_video():
        global lost_counter
        
        try:
            decoder = jpeg.Decoder(rotation=0, format="RGB565_BE", block=True)
        except:
            print("JPEG ERROR")
            return
        
        img_data = bytearray()
        handle_image_data(img_data)
        try:
            for y in range(4, 121, 8):
                dt = decoder.decode(img_data)
                tft.blit_buffer(dt, 0, y, 160, 120)
            lost_counter = 0
        except:
            lost_counter = lost_counter + 1
            if lost_counter > 10 and lost_counter != 255:
                tft.fill(st7789.BLACK) 
                lost_counter = 255
            return
except:
    def recieve_video():
        return