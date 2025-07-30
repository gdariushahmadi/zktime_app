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
python -m PyInstaller --onefile --windowed --name=ZKTimeBeta --hidden-import=requests --hidden-import=urllib3 --hidden-import=charset_normalizer --hidden-import=certifi --hidden-import=idna --hidden-import=pystray --hidden-import=PIL --hidden-import=PIL.Image --hidden-import=PIL.ImageDraw --hidden-import=schedule --hidden-import=pyzk --hidden-import=zk --hidden-import=tkinter --hidden-import=tkinter.messagebox --hidden-import=winreg --hidden-import=threading --hidden-import=logging --hidden-import=json --hidden-import=datetime --hidden-import=time simple_zktime_app_beta.py

echo.
echo ✅ BETA build completed!
echo 📁 Executable: dist/ZKTimeBeta.exe
echo 📄 Log file: zktime_beta_test.log
echo 🌐 Server: https://beta.sdadparts.com/api/attendance/device-import
echo.
echo ⚠️  This is a BETA version for testing purposes!
pause