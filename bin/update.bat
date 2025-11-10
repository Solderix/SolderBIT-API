@echo off
set myport=%1

if "%myport%"=="" (
    echo Usage: %0 COMxx
    exit /b 1
)

esptool --chip esp32s3 --port %myport% erase_flash
if ERRORLEVEL 1 (
    echo Erase failed!
    exit /b 1
)
timeout /t 1 /nobreak >nul

esptool --chip esp32s3 --port %myport% write_flash -z 0 .\ESP32_GENERIC_S3-20240602-v1.23.0.bin
if ERRORLEVEL 1 (
    echo Flash failed!
    exit /b 1
)
timeout /t 4 /nobreak >nul

echo Removing all imports from solder:bit...
ampy -p COM29 rmdir ./

for %%f in ("..\solderbit\imports\*.py") do (
    ampy -p COM29 put %%f
    echo %%f
)

ampy -p COM29 ls
timeout /t 1 /nobreak >nul

ampy -p COM29 put ..\solderbit\examples\test\main.py

echo All steps completed successfully!