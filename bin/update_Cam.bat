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

esptool --chip esp32s3 --port %myport% write_flash -z 0 .\Solderix_Cam_V2.1_esp32s3.bin
if ERRORLEVEL 1 (
    echo Flash failed!
    exit /b 1
)
timeout /t 1 /nobreak >nul

echo All steps completed successfully!