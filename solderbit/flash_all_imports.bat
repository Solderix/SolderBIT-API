set ampy_port=%1

if "%ampy_port%"=="" (
    echo Usage: %0 COMxx
    exit /b 1
)

echo Removing all imports from solder:bit...
ampy -p %ampy_port% rmdir ./

for %%f in (".\imports\*.py") do (
    ampy -p %ampy_port% put %%f
    echo %%f
)

ampy -p %ampy_port% ls

echo Check if all files are present on the device.
