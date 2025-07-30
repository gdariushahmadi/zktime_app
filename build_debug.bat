@echo off
echo Building ZKTeco Web Interface Debug Executable...
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

REM Build the debug executable (with console)
echo Building debug executable...
python -m PyInstaller --onefile --name ZKTecoWebInterface_Debug web_interface.py

if errorlevel 1 (
    echo Error: Failed to build debug executable
    pause
    exit /b 1
)

echo.
echo Debug build completed successfully!
echo Debug executable location: dist\ZKTecoWebInterface_Debug.exe
echo This version will show console window with error messages.
echo.
pause 