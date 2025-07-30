# ZKTeco Device Sync Windows Application

A Windows desktop application for synchronizing attendance device data with a remote server. The application runs in the system tray with automatic synchronization, manual sync options, and comprehensive logging.

## Features

- **System Tray Integration**: Runs in the background with system tray icon
- **Automatic Synchronization**: Scheduled sync based on configurable intervals
- **Manual Sync**: On-demand synchronization through system tray menu
- **Device Status Monitoring**: Real-time device connection and data status
- **Connection Testing**: Test device and server connectivity
- **Auto-start Support**: Automatic startup with Windows boot
- **Comprehensive Logging**: Detailed logs for troubleshooting
- **Settings Interface**: View and manage application settings
- **Web Interface Access**: Quick access to web-based interface

## Installation

### Prerequisites
- Windows 7/8/10/11
- Python 3.8 or higher
- Network access to ZKTeco attendance device
- Internet access for server synchronization

### Building the Executable

#### Method 1: Using Batch File (Recommended)
1. Open Command Prompt as Administrator
2. Navigate to the `zktime_windows_app` directory
3. Run: `build.bat`
4. Wait for the build process to complete
5. The executable will be created in the `dist/` directory

#### Method 2: Using PowerShell
1. Open PowerShell as Administrator
2. Navigate to the `zktime_windows_app` directory
3. Run: `.\build.ps1`
4. Wait for the build process to complete

#### Method 3: Manual Build
1. Install requirements: `pip install -r requirements.txt`
2. Install PyInstaller: `pip install pyinstaller`
3. Run build script: `python build_exe.py`

### Running the Application

1. **First Time Setup**:
   - Double-click `ZKTecoDeviceSync.exe` in the `dist/` directory
   - The application will start and appear in the system tray
   - A blue icon with "Z" will appear next to the clock

2. **System Tray Menu**:
   Right-click on the system tray icon to access:
   - **Open Web Interface**: Opens web interface in browser
   - **Manual Sync**: Perform immediate synchronization
   - **Device Status**: View current device information
   - **Test Connection**: Test device and server connections
   - **Settings**: View application configuration
   - **Auto-start**: Enable/disable Windows startup
   - **View Log**: Open log file in text editor
   - **Exit**: Close the application

## Configuration

### Device Settings
The application uses the following default settings (configurable in `config.py`):

```python
DEVICE_IP = '192.168.70.141'      # Device IP address
DEVICE_PORT = 4370                 # Device port
DEVICE_TIMEOUT = 5                 # Connection timeout
SYNC_INTERVAL = 3600               # Sync interval in seconds (1 hour)
```

### Server Settings
```python
TARGET_SERVER_URL = 'https://panel.sdadparts.com/api/device/import'
TARGET_SERVER_TOKEN = 'your_token_here'
```

### Logging Configuration
```python
LOG_LEVEL = 'INFO'                 # Log level (DEBUG, INFO, WARNING, ERROR)
LOG_FILE = 'zktime_sync.log'       # Log file name
```

## Usage

### Automatic Synchronization
- The application automatically syncs data based on the configured interval
- Default interval is 1 hour (3600 seconds)
- Sync status is logged to `zktime_sync.log`

### Manual Synchronization
1. Right-click the system tray icon
2. Select "Manual Sync"
3. Check the log file for sync results

### Device Status Monitoring
1. Right-click the system tray icon
2. Select "Device Status"
3. View device information, connection status, and data counts

### Connection Testing
1. Right-click the system tray icon
2. Select "Test Connection"
3. Verify device and server connectivity

### Auto-start Configuration
1. Right-click the system tray icon
2. Select "Auto-start"
3. Choose to enable or disable automatic startup

## Logging

### Log File Location
- Log file: `zktime_sync.log` (in the same directory as the executable)
- Log level: INFO (default)
- Encoding: UTF-8

### Log Contents
- Application startup and shutdown
- Device connection status
- Synchronization attempts and results
- Error messages and troubleshooting information
- Device data summaries

### Viewing Logs
1. Right-click the system tray icon
2. Select "View Log"
3. Log file opens in default text editor

## Troubleshooting

### Common Issues

#### System Tray Icon Not Appearing
- Check if the application is running in Task Manager
- Verify that `pystray` and `PIL` packages are installed
- Run the application as Administrator

#### Connection Errors
- Verify device IP address and port in configuration
- Check network connectivity to the device
- Ensure firewall allows connections to the device port
- Test with ping or telnet to verify connectivity

#### Sync Failures
- Check server URL and token in configuration
- Verify internet connectivity
- Review log file for detailed error messages
- Test server connection manually

#### Auto-start Not Working
- Run the application as Administrator
- Check Windows Registry for startup entry
- Verify executable path is correct

### Debug Mode
To run in debug mode (with console window):
1. Edit `build_exe.py`
2. Change `--windowed` to `--console`
3. Rebuild the executable

## File Structure

```
zktime_windows_app/
├── main.py              # Main application file
├── requirements.txt     # Python dependencies
├── build_exe.py        # Build script
├── build.bat           # Windows batch build script
├── build.ps1           # PowerShell build script
├── README.md           # This file
└── dist/               # Built executable directory
    ├── ZKTecoDeviceSync.exe
    ├── config.py
    ├── services/
    └── README.txt
```

## Development

### Prerequisites for Development
```bash
pip install -r requirements.txt
pip install pyinstaller
```

### Running in Development Mode
```bash
python main.py
```

### Building for Distribution
```bash
python build_exe.py
```

## Security Considerations

- Store sensitive configuration in environment variables
- Use HTTPS for server communication
- Implement proper authentication for device access
- Regular log rotation to prevent disk space issues
- Secure storage of server tokens

## Support

For issues and questions:
1. Check the log file for error details
2. Verify network connectivity
3. Test device connection manually
4. Review configuration settings

## License

This application is part of the ZKTeco Device Information System project.

## Version History

- v1.0.0: Initial release with system tray, auto-sync, and logging
- Features: System tray integration, automatic synchronization, manual sync, device monitoring, connection testing, auto-start support, comprehensive logging 