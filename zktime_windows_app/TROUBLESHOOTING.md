# Troubleshooting Guide

## ModuleNotFoundError: No module named 'requests'

### Problem
When running the Windows executable, you get this error:
```
Traceback (most recent call last):
  File "main.py", line 28, in <module>
  File "C:\Users\SD-MGH\AppData\Local\Temp\_MEI220322\services\device_service.py", line 9, in <module>
    import requests
ModuleNotFoundError: No module named 'requests'
```

### Solution

#### Method 1: Use the Fixed Build Script (Recommended)
1. **Delete the old executable** from the `dist/` directory
2. **Run the fixed build script**:
   ```cmd
   build_fixed.bat
   ```
   Or manually:
   ```cmd
   python build_exe_fixed.py
   ```

#### Method 2: Manual Fix
If you want to fix the existing build script:

1. **Edit `build_exe.py`** and add these hidden imports:
   ```python
   "--hidden-import=requests",     # HTTP requests
   "--hidden-import=urllib3",      # HTTP client
   "--hidden-import=charset_normalizer",  # Character encoding
   "--hidden-import=certifi",      # SSL certificates
   "--hidden-import=idna",         # Internationalized domain names
   ```

2. **Rebuild the executable**:
   ```cmd
   python build_exe.py
   ```

### Why This Happens

PyInstaller sometimes doesn't automatically detect all dependencies, especially when they're imported dynamically or in submodules. The `requests` library has several dependencies that need to be explicitly included.

### Prevention

Always use the fixed build script (`build_exe_fixed.py`) which includes all necessary hidden imports:

- `requests` - HTTP requests
- `urllib3` - HTTP client
- `charset_normalizer` - Character encoding
- `certifi` - SSL certificates
- `idna` - Internationalized domain names
- `win32api`, `win32con`, `win32gui` - Windows API
- `pystray` - System tray
- `PIL` - Image processing
- `schedule` - Scheduling
- `pyzk` - ZKTeco library
- `tkinter` - GUI framework
- And many more...

### Verification

After building with the fixed script, the executable should:
1. ✅ Start without ModuleNotFoundError
2. ✅ Show system tray icon
3. ✅ Display menu options
4. ✅ Connect to device and server

### Alternative Solutions

If the problem persists:

1. **Check Python environment**:
   ```cmd
   python -c "import requests; print('requests is available')"
   ```

2. **Reinstall requirements**:
   ```cmd
   pip uninstall requests
   pip install requests
   ```

3. **Use virtual environment**:
   ```cmd
   python -m venv venv
   venv\Scripts\activate
   pip install -r requirements.txt
   python build_exe_fixed.py
   ```

### Common Issues

1. **Missing dependencies**: Use the fixed build script
2. **Wrong Python version**: Use Python 3.8+
3. **Path issues**: Run from the correct directory
4. **Permission issues**: Run as Administrator

### Success Indicators

When the build is successful, you should see:
```
✅ Executable built successfully
✅ All dependencies included
✅ No ModuleNotFoundError when running
✅ System tray icon appears
✅ Menu options work correctly
```

### File Locations

- **Fixed build script**: `build_exe_fixed.py`
- **Fixed batch file**: `build_fixed.bat`
- **Executable**: `dist/ZKTecoDeviceSync.exe`
- **Configuration**: `dist/config.py`
- **Services**: `dist/services/`

### Next Steps

After successful build:
1. Test the executable: `dist/ZKTecoDeviceSync.exe`
2. Check system tray for the blue "Z" icon
3. Right-click icon to access menu
4. Test device connection
5. Test manual sync

The fixed build script includes all necessary dependencies and should resolve the ModuleNotFoundError completely. 