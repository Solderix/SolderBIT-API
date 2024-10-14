set ampy_port=COM29

echo solderbit.by
ampy -p %ampy_port% put .\imports\solderbit.py
echo controller.by
ampy -p %ampy_port% put .\imports\controller.py
echo radio.by
ampy -p %ampy_port% put .\imports\radio.py
echo ssd1306.by
ampy -p %ampy_port% put .\imports\ssd1306.py
echo vehicle.by
ampy -p %ampy_port% put .\imports\vehicle.py
echo main.by
ampy -p %ampy_port% put .\examples\car_joystick\main.py

ampy -p %ampy_port% ls

echo Check if all five files are present on the device.
echo Enter to exit...
pause >nul