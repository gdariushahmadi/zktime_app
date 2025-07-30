# ZKTeco Windows Application - Quick Start Guide

## 🚀 Quick Setup

### 1. Build the Executable
```bash
# Navigate to the Windows app directory
cd zktime_windows_app

# Run the build script
python build_exe.py
```

### 2. Test the Application
```bash
# Test basic functionality
python test_app.py
```

### 3. Install and Run
```bash
# Run the installer
install.bat
```

## 📋 Features Overview

✅ **System Tray Integration** - Runs in background with tray icon  
✅ **Automatic Sync** - Scheduled synchronization every hour  
✅ **Manual Sync** - On-demand synchronization  
✅ **Device Monitoring** - Real-time device status  
✅ **Connection Testing** - Test device and server connectivity  
✅ **Auto-start** - Start with Windows boot  
✅ **Comprehensive Logging** - Detailed logs for troubleshooting  
✅ **Settings Interface** - View and manage configuration  

## 🎯 System Tray Menu

Right-click the system tray icon (blue circle with "Z") to access:

- **Open Web Interface** - Opens web interface in browser
- **Manual Sync** - Perform immediate synchronization
- **Device Status** - View current device information
- **Test Connection** - Test device and server connections
- **Settings** - View application configuration
- **Auto-start** - Enable/disable Windows startup
- **View Log** - Open log file in text editor
- **Exit** - Close the application

## ⚙️ Configuration

### Device Settings (config.py)
```python
DEVICE_IP = '192.168.70.141'      # Your device IP
DEVICE_PORT = 4370                 # Device port
SYNC_INTERVAL = 3600               # Sync every hour
```

### Server Settings
```python
TARGET_SERVER_URL = 'https://panel.sdadparts.com/api/device/import'
TARGET_SERVER_TOKEN = 'your_token_here'
```

## 🔧 Troubleshooting

### Common Issues

**System Tray Icon Not Appearing**
- Check Task Manager for running process
- Run as Administrator
- Verify pystray and PIL packages installed

**Connection Errors**
- Verify device IP and port
- Check network connectivity
- Test with ping: `ping 192.168.70.141`

**Sync Failures**
- Check server URL and token
- Verify internet connectivity
- Review log file for details

### Log File
- Location: `zktime_sync.log` (same directory as executable)
- Contains: Sync status, errors, device information
- View via: System tray → View Log

## 📁 File Structure

```
zktime_windows_app/
├── main.py              # Main application
├── requirements.txt     # Dependencies
├── build_exe.py        # Build script
├── build.bat           # Windows build script
├── build.ps1           # PowerShell build script
├── test_app.py         # Test script
├── install.bat         # Installation script
├── README.md           # Detailed documentation
└── QUICK_START.md      # This file
```

## 🛠️ Development

### Prerequisites
```bash
pip install -r requirements.txt
pip install pyinstaller
```

### Run in Development Mode
```bash
python main.py
```

### Test Functionality
```bash
python test_app.py
```

### Build Executable
```bash
python build_exe.py
```

## 📦 Distribution

### For End Users
1. Build the executable: `python build_exe.py`
2. Run installer: `install.bat`
3. Application will be installed to Program Files
4. Desktop and Start Menu shortcuts created

### For Testing
1. Build the executable: `python build_exe.py`
2. Copy `dist/ZKTecoDeviceSync.exe` to target machine
3. Run the executable directly

## 🔒 Security Notes

- Store sensitive tokens in environment variables
- Use HTTPS for server communication
- Implement proper device authentication
- Regular log rotation to prevent disk space issues

## 📞 Support

For issues:
1. Check the log file for error details
2. Verify network connectivity
3. Test device connection manually
4. Review configuration settings

---

**Ready to deploy!** 🎉 