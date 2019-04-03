@echo off
title TLoPO Launcher - https://github.com/ethanlindley

echo ====================================================
echo Leave the following entry blank if your 
echo installation location is in the default location:
echo (C:\Program Files (x86)\TLOPO\)
echo.
echo If it isn't, then enter the installation location
echo INCLUDING the drive letter 
echo (ex: D:\TLOPO\)
echo ====================================================
echo.

REM Get the user's input...
SET /P TLOPO_INSTALL_DIR="Full TLoPO installation location: "
REM In case they don't supply a value
IF NOT DEFINED TLOPO_INSTALL_DIR SET TLOPO_INSTALL_DIR=C:\Program Files (x86)\TLOPO\

REM Change directories (and drives, if necessary) to the install location
cd /D %TLOPO_INSTALL_DIR%

REM Clear the command prompt
cls

REM Execute the program and exit the command prompt upon program termination
cmd /c "" tlopo.exe && exit
