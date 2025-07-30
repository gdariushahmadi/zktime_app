@echo off
echo 🔨 ZKTime Simple App Builder
echo =============================

echo.
echo Building a SIMPLE app with:
echo   ✅ Only system tray
echo   ✅ No web interface  
echo   ✅ No console window
echo   ✅ Just sync functionality
echo.

echo 📦 Installing requirements...
pip install -r requirements.txt
pip install pyinstaller

echo.
echo 🔨 Building executable...
python build_simple.py

echo.
echo ✅ Done! Check dist/ZKTimeSimple.exe
pause