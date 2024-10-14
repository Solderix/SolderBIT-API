from micropython import const
from machine import *
from solderbit import *
import bluetooth
import struct
import network

connected_led = machine.Pin(CONNECTED_PIN, machine.Pin.OUT)

CHANNEL_MODE = const(1)
PEER_TO_PEER_MODE = const(2)

RADIO_OFF = False
RADIO_ON = True

_IRQ_CENTRAL_CONNECT = const(1)
_IRQ_CENTRAL_DISCONNECT = const(2)
_IRQ_GATTS_WRITE = const(3)
_IRQ_GATTS_READ_REQUEST = const(4)
_IRQ_SCAN_RESULT = const(5)
_IRQ_SCAN_DONE = const(6)
_IRQ_PERIPHERAL_CONNECT = const(7)
_IRQ_PERIPHERAL_DISCONNECT = const(8)
_IRQ_GATTC_SERVICE_RESULT = const(9)
_IRQ_GATTC_SERVICE_DONE = const(10)
_IRQ_GATTC_CHARACTERISTIC_RESULT = const(11)
_IRQ_GATTC_CHARACTERISTIC_DONE = const(12)
_IRQ_GATTC_DESCRIPTOR_RESULT = const(13)
_IRQ_GATTC_DESCRIPTOR_DONE = const(14)
_IRQ_GATTC_READ_RESULT = const(15)
_IRQ_GATTC_READ_DONE = const(16)
_IRQ_GATTC_WRITE_DONE = const(17)
_IRQ_GATTC_NOTIFY = const(18)
_IRQ_GATTC_INDICATE = const(19)
_IRQ_GATTS_INDICATE_DONE = const(20)
_IRQ_MTU_EXCHANGED = const(21)
_IRQ_L2CAP_ACCEPT = const(22)
_IRQ_L2CAP_CONNECT = const(23)
_IRQ_L2CAP_DISCONNECT = const(24)
_IRQ_L2CAP_RECV = const(25)
_IRQ_L2CAP_SEND_READY = const(26)
_IRQ_CONNECTION_UPDATE = const(27)
_IRQ_ENCRYPTION_UPDATE = const(28)
_IRQ_GET_SECRET = const(29)
_IRQ_SET_SECRET = const(30)

device_random_names = [
    "Byte",
    "Cybot",
    "Droid",
    "Mech",
    "Robo",
    "Cyrex",
    "Botix",
    "Titan",
    "R2D2",
    "Cylon",
    "Zer0",
    "Nova",
    "Sonic",
    "Evolv",
    "Nexus",
    "Viper",
    "Astra",
    "Echo",
    "Pulse",
    "Astro",
    "Xylon",
    "Spark",
    "Slick",
    "Omega",
    "Xenon",
    "Zoom",
    "Blitz",
    "Zenith",
    "Blaze",
    "Cogix",
    "Jaxon",
    "Volt",
    "Draco",
    "Orion",
    "Cyton",
    "Pluto",
    "Infer",
    "Wizar",
    "Ziggy",
    "Cosmo",
    "Vortex",
    "Spinx",
    "Galax",
    "Quark",
    "Quinx",
    "Pulsar",
    "Cogs",
    "Wheels",
    "Ultra",
    "Giga",
    "Shpyro",
    "Soldy",
    "Dr. 0",
    "Klein",
    "Dr. 8",
    "Borous",
    "Dala",
    "Mobius",
    "Rusty",
]


_FLAG_WRITE = const(0x0008)
_FLAG_NOTIFY = const(0x0010)


_SOLDERIX_UUID = bluetooth.UUID("6E400001-B5A3-F393-E0A9-E50E24DCCA9E")
_SOLDERIX_TX = (
    bluetooth.UUID("6E400003-B5A3-F393-E0A9-E50E24DCCA9E"),
    _FLAG_NOTIFY,
)
_SOLDERIX_RX = (
    bluetooth.UUID("6E400002-B5A3-F393-E0A9-E50E24DCCA9E"),
    _FLAG_WRITE,
)
_SOLDERIX_SERVICE = (
    _SOLDERIX_UUID,
    (_SOLDERIX_TX, _SOLDERIX_RX),
)


_ADV_TYPE_FLAGS = const(0x01)
_ADV_TYPE_NAME = const(0x09)
_ADV_TYPE_UUID16_COMPLETE = const(0x3)
_ADV_TYPE_UUID32_COMPLETE = const(0x5)
_ADV_TYPE_UUID128_COMPLETE = const(0x7)
_ADV_TYPE_UUID16_MORE = const(0x2)
_ADV_TYPE_UUID32_MORE = const(0x4)
_ADV_TYPE_UUID128_MORE = const(0x6)
_ADV_TYPE_APPEARANCE = const(0x19)
_ADV_MAX_PAYLOAD = const(31)

_RX_BUFFER_MAX = const(10)

PERIPHERAL_MODE = const(0)
CENTRAL_MODE = const(1)

class Radio:
    def __init__(self) -> None:
        self.ble = bluetooth.BLE()
        self.operatio_mode = CHANNEL_MODE
        self.ble.irq(self.ble_irq)
        self.device_list = []
        self.device_list_tmp = []
        self._is_connected = False
        self._scan_done = True
        self._rx_buffer = []
        wlan_sta = network.WLAN(network.STA_IF)
        self.wlan_mac = wlan_sta.config('mac')
        self.name = None
        connected_led.off()

    def on(self, mode=PERIPHERAL_MODE, name=None):
        if name == None and self.name == None:
            name = device_random_names[sum(self.wlan_mac)%len(device_random_names)]
        self.name = name
        self.ble.active(True)
        ((self._tx_handle, self._rx_handle),) = self.ble.gatts_register_services((_SOLDERIX_SERVICE,))
        self.ble.gatts_set_buffer(self._rx_handle, 100, True)
        
        if mode == CENTRAL_MODE:
            self.scan()
            #while self._scan_done == False:
                #pass
            #self._scan_done = False
            #return self.device_list
            return None
        elif mode == PERIPHERAL_MODE:
            self.advertise()
            return None

    def off(self):
        self.ble.active(False)

    def config(self, *kwargs):
        return

    def reset(self):
        self.device_list = []
        self._is_connected = False
        self._scan_done = False
        self._rx_buffer = []
        connected_led.off()
        self._conn_handle = None
        self.off()
        return
    
    def send(self, message):
        self.send_bytes(message.encode())
        return
    
    def receive_bytes(self):
        if not self._is_connected:
            return None
        
        if len(self._rx_buffer) > 0:
            return self._rx_buffer.pop()
        return None
    
    def receive_bytes_into(self, buffer):
        buffer = self.receive_bytes()
    
    def send_bytes(self, message):
        if not self._is_connected:
            return
        try:
            self.ble.gattc_write(self._conn_handle, self._rx_handle, message, True)
        except:
            self._is_connected = False
    
    def receive(self):
        tmp = self.receive_bytes()
        if tmp != None:
            tmp = tmp.decode()
        return tmp
        
        if len(self._rx_buffer) > 0:
            return self._rx_buffer.pop().decode()
        return None
    
    def receive_full(self):
        if not self._is_connected:
            return None
        
        if len(self._rx_buffer) > 0:
            tmp = self._rx_buffer
            self._rx_buffer = []
            return tmp
        return None
    
    #custom functions
    def channel_mode(self):
        self.operatio_mode = CHANNEL_MODE
 
    def peer_mode(self):
        self.operatio_mode = PEER_TO_PEER_MODE

    def ble_irq(self, event, data):
        if event == _IRQ_CENTRAL_CONNECT:
            conn_handle, _, _ = data
            self._is_connected = True
            self._conn_handle = conn_handle
            connected_led.on()
            print("Connected to central")

        elif event == _IRQ_CENTRAL_DISCONNECT:
            self._is_connected = False
            self._conn_handle = None
            connected_led.off()
            print("Disconnected from central")
            self.advertise()

        elif event == _IRQ_PERIPHERAL_CONNECT:
            conn_handle, addr_type, addr = data
            self._conn_handle = conn_handle
            self.ble.gattc_discover_services(self._conn_handle)
            self._is_connected = True
            connected_led.on()
            print("Connected to peripheral")

        elif event == _IRQ_PERIPHERAL_DISCONNECT:
            self._is_connected = False
            self._conn_handle = None
            connected_led.off()
            print("Disconected from peripheral")

        elif event == _IRQ_SCAN_RESULT:
            addr_type, addr, adv_type, rssi, adv_data = data
            entry = { "name" : decode_name(adv_data),
                     "addr" : _memory_2_array(addr),
                     "addr_type" : addr_type} 


            if _SOLDERIX_UUID in decode_services(adv_data) and entry not in self.device_list_tmp:
                self.device_list_tmp.append(entry)
                
        elif event == _IRQ_SCAN_DONE:
            self._scan_done = True

            for device in self.device_list:
                if device not in self.device_list_tmp:
                    self.device_list.remove(device)
                elif device in self.device_list_tmp:
                    self.device_list_tmp.remove(device)

            self.device_list += self.device_list_tmp
            self.device_list_tmp = []
            print("Scan done!")

        elif event == _IRQ_GATTC_READ_DONE:
            pass

        elif event == _IRQ_GATTC_WRITE_DONE:
            conn_handle, value_handle, status = data
            #print("TX complete")

        elif event == _IRQ_GATTS_WRITE:
            conn_handle, value_handle = data
            value = self.ble.gatts_read(value_handle)
            
            if value_handle != self._rx_handle:
                return
            
            #remove oldest entry if buffer full
            if len(self._rx_buffer) >= _RX_BUFFER_MAX: 
                self._rx_buffer.pop()
            self._rx_buffer.append(value)


    def scan(self, duration_ms=5000):
        if self._scan_done == True:
            self._scan_done = False
            try:
                self.ble.gap_scan(2000, 30000, 30000)
            except:
                pass
            
    def get_devices(self):
        self.scan()
        return self.device_list

    def advertise(self):
       _payload = advertising_payload(name=self.name, services=[_SOLDERIX_UUID])
       self.ble.gap_advertise(500000, adv_data=_payload)

    def connect(self, device):
        #print(_memory_2_array(device["addr"]))
        self.ble.gap_connect(device["addr_type"],device["addr"])
        self.device_list = []

    def disconnect(self):
        self._is_connected = False
        self.ble.gap_disconnect(self._conn_handle)

    def connection(self):
        return self._is_connected


# Generate a payload to be passed to gap_advertise(adv_data=...).
def advertising_payload(limited_disc=False, br_edr=False, name=None, services=None, appearance=0):
    payload = bytearray()

    def _append(adv_type, value):
        nonlocal payload
        payload += struct.pack("BB", len(value) + 1, adv_type) + value

    _append(
        _ADV_TYPE_FLAGS,
        struct.pack("B", (0x01 if limited_disc else 0x02) + (0x18 if br_edr else 0x04)),
    )

    if name:
        _append(_ADV_TYPE_NAME, name)

    if services:
        for uuid in services:
            b = bytes(uuid)
            if len(b) == 2:
                _append(_ADV_TYPE_UUID16_COMPLETE, b)
            elif len(b) == 4:
                _append(_ADV_TYPE_UUID32_COMPLETE, b)
            elif len(b) == 16:
                _append(_ADV_TYPE_UUID128_COMPLETE, b)

    # See org.bluetooth.characteristic.gap.appearance.xml
    if appearance:
        _append(_ADV_TYPE_APPEARANCE, struct.pack("<h", appearance))

    if len(payload) > _ADV_MAX_PAYLOAD:
        raise ValueError("advertising payload too large")

    return payload


def decode_field(payload, adv_type):
    i = 0
    result = []
    while i + 1 < len(payload):
        if payload[i + 1] == adv_type:
            result.append(payload[i + 2 : i + payload[i] + 1])
        i += 1 + payload[i]
    return result


def decode_name(payload):
    n = decode_field(payload, _ADV_TYPE_NAME)
    return str(n[0], "utf-8") if n else ""


def decode_services(payload):
    services = []
    for u in decode_field(payload, _ADV_TYPE_UUID16_COMPLETE):
        services.append(bluetooth.UUID(struct.unpack("<h", u)[0]))
    for u in decode_field(payload, _ADV_TYPE_UUID32_COMPLETE):
        services.append(bluetooth.UUID(struct.unpack("<d", u)[0]))
    for u in decode_field(payload, _ADV_TYPE_UUID128_COMPLETE):
        services.append(bluetooth.UUID(u))
    return services


def _memory_2_mac(data):
    data_out = f'{data[0]:x}'
    for byte in data[1:]:
        data_out = data_out + ":" + f'{byte:x}'
    return data_out


def _memory_2_array(data):
    return bytearray(data)


radio = Radio()