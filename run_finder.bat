@echo off
setlocal
cd /d %~dp0
echo ==========================================
echo           Log ID Finder Tool
echo ==========================================
echo.

:: Default search IDs, can be modified here
python id_finder.py 78128243 90000730 90000729 90000733

echo.
echo ==========================================
pause
