@echo off
echo ZKTeco Windows Application Builder (FIXED)
echo ==========================================

echo.
echo This build includes all necessary dependencies to prevent ModuleNotFoundError
echo.

echo Installing requirements...
pip install -r requirements.txt

echo.
echo Installing PyInstaller...
pip install pyinstaller

echo.
echo Building executable with all dependencies...
python build_exe_fixed.py

echo.
echo Build process completed!
echo Check the dist/ directory for the executable.
echo.
echo Note: This build includes requests, urllib3, and all other dependencies
pause 