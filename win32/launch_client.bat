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

SET /P TLOPO_INSTALL_DIR="Full TLoPO installation location: "
IF NOT DEFINED TLOPO_INSTALL_DIR SET TLOPO_INSTALL_DIR=C:\Program Files (x86)\TLOPO\

cd /D %TLOPO_INSTALL_DIR%

start tlopo.exe
exit
