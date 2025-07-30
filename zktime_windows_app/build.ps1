# ZKTeco Windows Application Builder
# PowerShell script for building the executable

Write-Host "ZKTeco Windows Application Builder" -ForegroundColor Green
Write-Host "=================================" -ForegroundColor Green

Write-Host ""
Write-Host "Installing requirements..." -ForegroundColor Yellow
python -m pip install -r requirements.txt

Write-Host ""
Write-Host "Installing PyInstaller..." -ForegroundColor Yellow
python -m pip install pyinstaller

Write-Host ""
Write-Host "Building executable..." -ForegroundColor Yellow
python build_exe.py

Write-Host ""
Write-Host "Build process completed!" -ForegroundColor Green
Write-Host "Check the dist/ directory for the executable." -ForegroundColor Cyan

Read-Host "Press Enter to continue" 