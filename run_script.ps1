Write-Host "Running ZKTeco Device Information Script..." -ForegroundColor Green
try {
    python zk_device_info.py
} catch {
    Write-Host "Error running script: $_" -ForegroundColor Red
}
Write-Host "Press any key to continue..." -ForegroundColor Yellow
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown") 