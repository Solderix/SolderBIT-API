import os, sys, subprocess, shutil
import argparse

ESP_VID = 0x303A    
COMMON_PID = 0x1001
UP_PID = 0x4001     
BAUDRATE_DEAFUTLT = 115200

parser = argparse.ArgumentParser(description="SolderBit Import Flasher")
parser.add_argument("--path", type=str, help="Path to import scripts", default="imports")
args = parser.parse_args()

print("Using path:", args.path)
IMPORTS_DIR = args.path

def import_pyserial():
    try:
        from serial.tools import list_ports
        print("pyserial present...")
        return
    except ImportError:
        print("pyserial missing, installing...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyserial"])
        from serial.tools import list_ports

def import_ampy():
    try:
        import ampy 
        print("Adafruit Micropyrhon present...")
    except ImportError:
        print("Adafruit Micropyrhon missing, installing...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "adafruit-ampy"])
        import ampy 

def upload_all(port):
    for name in sorted(os.listdir(IMPORTS_DIR)):
        if not name.endswith(".py"):
            continue
        local = os.path.join(IMPORTS_DIR, name)
        print("Uploading", name, "...")
    
        subprocess.check_call(["ampy", "--port", port, "put", local])
    print("Done.")
    

import_pyserial()
import_ampy()

from serial.tools import list_ports

found_device_flag = False

for p in list_ports.comports():
    vid = p.vid
    pid = p.pid
    if vid == ESP_VID and pid == UP_PID:
        print("Found SolderBIT in uP mode on port:", p.device)
        upload_all(p.device)
        exit()

print("SolderBIT device in uP mode not found. Please connect the device in uP mode and try again.")
    