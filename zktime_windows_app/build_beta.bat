@echo off
echo 🧪 ZKTime BETA Test App Builder
echo ===============================

echo.
echo Building BETA version with:
echo   🔸 BETA server: beta.sdadparts.com
echo   🔸 Orange icon (B for Beta)
echo   🔸 5-minute sync interval for testing
echo   🔸 Enhanced logging
echo   🔸 User list testing
echo.

echo 📦 Installing requirements...
pip install -r requirements.txt
pip install pyinstaller

echo.
echo 🔨 Building BETA executable...
python build_beta.py

echo.
echo ✅ BETA build completed!
echo 📁 Executable: dist/ZKTimeBeta.exe
echo 📄 Log file: zktime_beta_test.log
echo 🌐 Server: https://beta.sdadparts.com/api/attendance/device-import
echo.
echo ⚠️  This is a BETA version for testing purposes!
pause