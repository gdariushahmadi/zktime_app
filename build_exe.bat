@echo off
echo Building ZKTeco Web Interface Executable...
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    pause
    exit /b 1
)

REM Install PyInstaller if not installed
echo Installing PyInstaller...
pip install pyinstaller

REM Build the executable
echo Building executable...
python -m PyInstaller --onefile --name ZKTecoWebInterface web_interface.py

if errorlevel 1 (
    echo Error: Failed to build executable
    pause
    exit /b 1
)

echo.
echo Build completed successfully!
echo Executable location: dist\ZKTecoWebInterface.exe
echo.
pause 