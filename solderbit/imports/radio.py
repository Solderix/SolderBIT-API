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
_esp_buffer_max = 5
_esp_buffer_counter = 0

mac_base = b'\x1a\x2b\x3c\x4e\x5f'  

def _recv_cb(e):
    global _esp_buffer_counter
    while True:  
        mac, data = e.irecv(0)
        if mac is None:
            return
        
        if data == None:
            return
    
        if _esp_buffer_counter < _esp_buffer_max:
            _esp_buffer_counter += 1
            _esp_buffer.append(data)

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

   print('Peers:', _e.get_peers())

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

def receive_bytes():
    global _e
    global _esp_buffer_counter
    global _esp_buffer
    
    if _esp_buffer_counter <= 0:
        return None

    _esp_buffer_counter -= 1
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


