@echo off
echo ZKTeco Device Sync - Installation Script
echo ========================================

echo.
echo This script will install the ZKTeco Device Sync application.
echo.

REM Check if running as administrator
net session >nul 2>&1
if %errorLevel% == 0 (
    echo Running as administrator - OK
) else (
    echo WARNING: Not running as administrator
    echo Some features may not work properly
    echo.
)

REM Create installation directory
set INSTALL_DIR=%PROGRAMFILES%\ZKTecoDeviceSync
echo Creating installation directory: %INSTALL_DIR%

if not exist "%INSTALL_DIR%" mkdir "%INSTALL_DIR%"

REM Copy files
echo.
echo Copying application files...
copy "dist\ZKTecoDeviceSync.exe" "%INSTALL_DIR%\" >nul
if exist "dist\config.py" copy "dist\config.py" "%INSTALL_DIR%\" >nul
if exist "dist\services" xcopy "dist\services" "%INSTALL_DIR%\services\" /E /I /Y >nul

REM Create desktop shortcut
echo Creating desktop shortcut...
set SHORTCUT="%USERPROFILE%\Desktop\ZKTeco Device Sync.lnk"
echo @echo off > "%TEMP%\create_shortcut.vbs"
echo Set oWS = WScript.CreateObject("WScript.Shell") >> "%TEMP%\create_shortcut.vbs"
echo sLinkFile = "%SHORTCUT%" >> "%TEMP%\create_shortcut.vbs"
echo Set oLink = oWS.CreateShortcut(sLinkFile) >> "%TEMP%\create_shortcut.vbs"
echo oLink.TargetPath = "%INSTALL_DIR%\ZKTecoDeviceSync.exe" >> "%TEMP%\create_shortcut.vbs"
echo oLink.WorkingDirectory = "%INSTALL_DIR%" >> "%TEMP%\create_shortcut.vbs"
echo oLink.Description = "ZKTeco Device Sync Application" >> "%TEMP%\create_shortcut.vbs"
echo oLink.Save >> "%TEMP%\create_shortcut.vbs"
cscript //nologo "%TEMP%\create_shortcut.vbs" >nul
del "%TEMP%\create_shortcut.vbs" >nul

REM Create start menu shortcut
echo Creating start menu shortcut...
set START_MENU="%APPDATA%\Microsoft\Windows\Start Menu\Programs\ZKTeco Device Sync.lnk"
echo @echo off > "%TEMP%\create_startmenu.vbs"
echo Set oWS = WScript.CreateObject("WScript.Shell") >> "%TEMP%\create_startmenu.vbs"
echo sLinkFile = "%START_MENU%" >> "%TEMP%\create_startmenu.vbs"
echo Set oLink = oWS.CreateShortcut(sLinkFile) >> "%TEMP%\create_startmenu.vbs"
echo oLink.TargetPath = "%INSTALL_DIR%\ZKTecoDeviceSync.exe" >> "%TEMP%\create_startmenu.vbs"
echo oLink.WorkingDirectory = "%INSTALL_DIR%" >> "%TEMP%\create_startmenu.vbs"
echo oLink.Description = "ZKTeco Device Sync Application" >> "%TEMP%\create_startmenu.vbs"
echo oLink.Save >> "%TEMP%\create_startmenu.vbs"
cscript //nologo "%TEMP%\create_startmenu.vbs" >nul
del "%TEMP%\create_startmenu.vbs" >nul

REM Create uninstaller
echo Creating uninstaller...
echo @echo off > "%INSTALL_DIR%\uninstall.bat"
echo echo ZKTeco Device Sync - Uninstaller >> "%INSTALL_DIR%\uninstall.bat"
echo echo ================================ >> "%INSTALL_DIR%\uninstall.bat"
echo echo. >> "%INSTALL_DIR%\uninstall.bat"
echo echo Removing application files... >> "%INSTALL_DIR%\uninstall.bat"
echo rmdir /s /q "%INSTALL_DIR%" >> "%INSTALL_DIR%\uninstall.bat"
echo echo. >> "%INSTALL_DIR%\uninstall.bat"
echo echo Removing shortcuts... >> "%INSTALL_DIR%\uninstall.bat"
echo if exist "%USERPROFILE%\Desktop\ZKTeco Device Sync.lnk" del "%USERPROFILE%\Desktop\ZKTeco Device Sync.lnk" >> "%INSTALL_DIR%\uninstall.bat"
echo if exist "%APPDATA%\Microsoft\Windows\Start Menu\Programs\ZKTeco Device Sync.lnk" del "%APPDATA%\Microsoft\Windows\Start Menu\Programs\ZKTeco Device Sync.lnk" >> "%INSTALL_DIR%\uninstall.bat"
echo echo. >> "%INSTALL_DIR%\uninstall.bat"
echo echo Uninstallation completed. >> "%INSTALL_DIR%\uninstall.bat"
echo pause >> "%INSTALL_DIR%\uninstall.bat"

echo.
echo Installation completed successfully!
echo.
echo Application installed to: %INSTALL_DIR%
echo Desktop shortcut created
echo Start menu shortcut created
echo.
echo To run the application:
echo 1. Double-click the desktop shortcut, or
echo 2. Use the start menu shortcut, or
echo 3. Run: %INSTALL_DIR%\ZKTecoDeviceSync.exe
echo.
echo To uninstall: Run %INSTALL_DIR%\uninstall.bat
echo.
pause 