set ampy_port=COM29

echo Removing all imports from solder:bit...
ampy -p %ampy_port% rmdir ./

for %%f in (".\imports\*.py") do (
    ampy -p %ampy_port% put %%f
    echo %%f
)

ampy -p %ampy_port% ls

echo Check if all files are present on the device.
echo Enter to exit...
pause >nul