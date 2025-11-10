@echo off
set myport=%1

setlocal enabledelayedexpansion

rem get number part
set NUM=%myport:COM=%

rem increment
set /a NUM+=1

rem build new port
set NEWPORT=COM!NUM!

echo Original: %PORT%
echo Incremented: !NEWPORT!

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

esptool --chip esp32s3 --port %myport% write_flash -z 0 .\ESP32_GENERIC_S3_LCD_JPEG.bin
if ERRORLEVEL 1 (
    echo Flash failed!
    exit /b 1
)
timeout /t 1 /nobreak >nul

echo reseting...
esptool.py --port %myport% run

timeout /t 4 /nobreak >nul

echo Removing all imports from solder:bit...
ampy -p %NEWPORT% rmdir ./

for %%f in ("..\solderbit\imports\*.py") do (
    ampy -p %NEWPORT% put %%f
    echo %%f
)

ampy -p %NEWPORT% ls
timeout /t 1 /nobreak >nul

ampy -p %NEWPORT% put ..\solderbit\examples\test\tes2\main.py

echo All steps completed successfully!