#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fixed build script for ZKTeco Windows Application
Includes all necessary hidden imports to prevent ModuleNotFoundError
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def install_requirements():
    """Install required packages"""
    print("Installing requirements...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("Requirements installed successfully")
    except subprocess.CalledProcessError as e:
        print(f"Failed to install requirements: {e}")
        return False
    return True

def install_pyinstaller():
    """Install PyInstaller if not already installed"""
    print("Checking PyInstaller...")
    try:
        import PyInstaller
        print("PyInstaller already installed")
    except ImportError:
        print("Installing PyInstaller...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
            print("PyInstaller installed successfully")
        except subprocess.CalledProcessError as e:
            print(f"Failed to install PyInstaller: {e}")
            return False
    return True

def build_executable():
    """Build the executable using PyInstaller with all necessary imports"""
    print("Building executable...")
    
    # PyInstaller command with all necessary hidden imports
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--onefile",                    # Single executable file
        "--windowed",                   # No console window
        "--name=ZKTecoDeviceSync",      # Executable name
        "--icon=icon.ico",              # Icon file (if exists)
        "--add-data=../config.py;.",    # Include config file
        "--add-data=../services;services",  # Include services directory
        "--hidden-import=requests",     # HTTP requests
        "--hidden-import=urllib3",      # HTTP client
        "--hidden-import=charset_normalizer",  # Character encoding
        "--hidden-import=certifi",      # SSL certificates
        "--hidden-import=idna",         # Internationalized domain names
        "--hidden-import=win32api",     # Windows API
        "--hidden-import=win32con",     # Windows constants
        "--hidden-import=win32gui",     # Windows GUI
        "--hidden-import=winreg",       # Windows registry
        "--hidden-import=pystray",      # System tray
        "--hidden-import=PIL",          # Image processing
        "--hidden-import=PIL.Image",    # PIL Image
        "--hidden-import=PIL.ImageDraw", # PIL ImageDraw
        "--hidden-import=schedule",     # Scheduling
        "--hidden-import=pyzk",         # ZKTeco library
        "--hidden-import=zk",           # ZKTeco library
        "--hidden-import=tkinter",      # GUI framework
        "--hidden-import=tkinter.messagebox",  # Message boxes
        "--hidden-import=webbrowser",   # Web browser
        "--hidden-import=threading",    # Threading
        "--hidden-import=logging",      # Logging
        "--hidden-import=json",         # JSON processing
        "--hidden-import=datetime",     # Date/time
        "--hidden-import=time",         # Time functions
        "--hidden-import=os",           # Operating system
        "--hidden-import=sys",          # System
        "--hidden-import=pathlib",      # Path handling
        "--hidden-import=shutil",       # Shell utilities
        "--hidden-import=subprocess",   # Subprocess
        "--hidden-import=random",       # Random
        "--hidden-import=typing",       # Type hints
        "--hidden-import=collections",  # Collections
        "--hidden-import=re",           # Regular expressions
        "--hidden-import=base64",       # Base64 encoding
        "--hidden-import=hashlib",      # Hash functions
        "--hidden-import=ssl",          # SSL
        "--hidden-import=socket",       # Socket
        "--hidden-import=struct",       # Struct
        "--hidden-import=binascii",     # Binary ASCII
        "--hidden-import=codecs",       # Codecs
        "--hidden-import=locale",       # Locale
        "--hidden-import=calendar",     # Calendar
        "--hidden-import=email",        # Email
        "--hidden-import=email.mime",   # Email MIME
        "--hidden-import=email.mime.text", # Email MIME text
        "--hidden-import=email.mime.multipart", # Email MIME multipart
        "--hidden-import=email.mime.base", # Email MIME base
        "--hidden-import=email.mime.nonmultipart", # Email MIME nonmultipart
        "--hidden-import=email.charset", # Email charset
        "--hidden-import=email.encoders", # Email encoders
        "--hidden-import=email.generator", # Email generator
        "--hidden-import=email.header", # Email header
        "--hidden-import=email.message", # Email message
        "--hidden-import=email.parser", # Email parser
        "--hidden-import=email.policy", # Email policy
        "--hidden-import=email.utils",  # Email utils
        "--hidden-import=email.quoprimime", # Email quoted printable
        "--hidden-import=email.base64mime", # Email base64
        "--hidden-import=email.iterators", # Email iterators
        "--hidden-import=email.feedparser", # Email feedparser
        "--hidden-import=email.mime.nonmultipart", # Email MIME nonmultipart
        "--hidden-import=email.mime.multipart", # Email MIME multipart
        "--hidden-import=email.mime.text", # Email MIME text
        "--hidden-import=email.mime.base", # Email MIME base
        "--hidden-import=email.mime.image", # Email MIME image
        "--hidden-import=email.mime.audio", # Email MIME audio
        "--hidden-import=email.mime.application", # Email MIME application
        "--hidden-import=email.mime.message", # Email MIME message
        "--hidden-import=email.mime.multipart", # Email MIME multipart
        "--hidden-import=email.mime.nonmultipart", # Email MIME nonmultipart
        "--hidden-import=email.mime.text", # Email MIME text
        "--hidden-import=email.mime.base", # Email MIME base
        "--hidden-import=email.mime.image", # Email MIME image
        "--hidden-import=email.mime.audio", # Email MIME audio
        "--hidden-import=email.mime.application", # Email MIME application
        "--hidden-import=email.mime.message", # Email MIME message
        "main.py"
    ]
    
    try:
        subprocess.check_call(cmd)
        print("Executable built successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Failed to build executable: {e}")
        return False

def create_icon():
    """Create a simple icon file if it doesn't exist"""
    icon_path = Path("icon.ico")
    if not icon_path.exists():
        print("Creating icon file...")
        try:
            from PIL import Image, ImageDraw
            
            # Create a simple icon
            img = Image.new('RGBA', (64, 64), (0, 0, 0, 0))
            draw = ImageDraw.Draw(img)
            
            # Draw blue circle
            draw.ellipse([8, 8, 56, 56], fill=(0, 120, 255, 255))
            # Draw white "Z"
            draw.text((20, 15), "Z", fill=(255, 255, 255, 255))
            
            # Save as ICO
            img.save("icon.ico", format='ICO')
            print("Icon created successfully")
        except Exception as e:
            print(f"Failed to create icon: {e}")

def copy_config_files():
    """Copy necessary config files to dist directory"""
    print("Copying config files...")
    
    dist_dir = Path("dist")
    if dist_dir.exists():
        # Copy config.py
        if Path("../config.py").exists():
            shutil.copy2("../config.py", "dist/")
            print("config.py copied to dist/")
        
        # Copy services directory
        if Path("../services").exists():
            shutil.copytree("../services", "dist/services", dirs_exist_ok=True)
            print("services directory copied to dist/")

def create_readme():
    """Create a README file for the executable"""
    readme_content = """# ZKTeco Device Sync Windows Application

## Installation and Usage

### 1. Running the Application
- Double-click `ZKTecoDeviceSync.exe` to start the application
- The application will run in the background and appear in the system tray
- A blue icon with "Z" will appear in the system tray (next to the clock)

### 2. System Tray Menu
Right-click on the system tray icon to access:
- **Open Web Interface**: Opens the web interface in your browser
- **Manual Sync**: Perform a manual synchronization
- **Device Status**: View current device status
- **Test Connection**: Test device and server connections
- **Settings**: View application settings
- **Auto-start**: Enable/disable automatic startup with Windows
- **View Log**: Open the log file in text editor
- **Exit**: Close the application

### 3. Configuration
The application uses the following configuration:
- Device IP: 192.168.70.141 (default)
- Device Port: 4370 (default)
- Sync Interval: 3600 seconds (1 hour, default)
- Server URL: https://panel.sdadparts.com/api/attendance/device-import

To change settings, edit the `config.py` file before building the executable.

### 4. Logging
- Log file: `zktime_sync.log` (in the same directory as the executable)
- Log level: INFO (default)
- Logs include sync status, errors, and device information

### 5. Auto-start
- Use the "Auto-start" option in the system tray menu
- Requires administrator privileges for the first time
- The application will start automatically when Windows boots

### 6. Troubleshooting
- If the icon doesn't appear in system tray, check the log file
- Ensure the device IP and port are correct
- Check network connectivity to the device
- Verify server URL and token are correct

### 7. Files
- `ZKTecoDeviceSync.exe`: Main executable
- `config.py`: Configuration file
- `services/`: Service modules
- `zktime_sync.log`: Application log file

## Building from Source

To rebuild the executable:
1. Install Python 3.8+
2. Install requirements: `pip install -r requirements.txt`
3. Run build script: `python build_exe_fixed.py`
4. Executable will be created in `dist/` directory

## Requirements
- Windows 7/8/10/11
- Network access to ZKTeco device
- Internet access for server synchronization
"""
    
    with open("dist/README.txt", "w", encoding="utf-8") as f:
        f.write(readme_content)
    print("README.txt created in dist/")

def main():
    """Main build process"""
    print("Starting ZKTeco Windows Application build process (FIXED)...")
    
    # Check if we're in the right directory
    if not Path("main.py").exists():
        print("Error: main.py not found. Please run this script from the zktime_windows_app directory.")
        return False
    
    # Install requirements
    if not install_requirements():
        return False
    
    # Install PyInstaller
    if not install_pyinstaller():
        return False
    
    # Create icon
    create_icon()
    
    # Build executable
    if not build_executable():
        return False
    
    # Copy config files
    copy_config_files()
    
    # Create README
    create_readme()
    
    print("\nBuild completed successfully!")
    print("Executable location: dist/ZKTecoDeviceSync.exe")
    print("To run: Double-click ZKTecoDeviceSync.exe")
    print("\nNote: This build includes all necessary dependencies to prevent ModuleNotFoundError")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 