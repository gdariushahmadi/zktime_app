@echo off
echo ZKTeco Windows Application Builder
echo =================================

echo.
echo Installing requirements...
pip install -r requirements.txt

echo.
echo Installing PyInstaller...
pip install pyinstaller

echo.
echo Building executable...
python build_exe.py

echo.
echo Build process completed!
echo Check the dist/ directory for the executable.
pause 