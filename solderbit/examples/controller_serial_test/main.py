from microbit import *
import srt as controller


while True:
    data = (controller.read_all_inputs())
    data.append(bool(0))
    print(data)
    sleep(10)