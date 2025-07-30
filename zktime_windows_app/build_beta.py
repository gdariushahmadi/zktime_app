#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BETA build script for ZKTime BETA App
"""

import os
import sys
import subprocess
from pathlib import Path

def build_beta_app():
    """Build the BETA ZKTime app"""
    print("Building ZKTime BETA App...")
    
    # PyInstaller command for BETA app
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--onefile",                    # Single executable file
        "--windowed",                   # No console window
        "--name=ZKTimeBeta",            # Executable name
        "--hidden-import=requests",     # HTTP requests
        "--hidden-import=urllib3",      # HTTP client
        "--hidden-import=charset_normalizer",  # Character encoding
        "--hidden-import=certifi",      # SSL certificates
        "--hidden-import=idna",         # Internationalized domain names
        "--hidden-import=pystray",      # System tray
        "--hidden-import=PIL",          # Image processing
        "--hidden-import=PIL.Image",    # PIL Image
        "--hidden-import=PIL.ImageDraw", # PIL ImageDraw
        "--hidden-import=schedule",     # Scheduling
        "--hidden-import=pyzk",         # ZKTeco library
        "--hidden-import=zk",           # ZKTeco library
        "--hidden-import=tkinter",      # GUI framework
        "--hidden-import=tkinter.messagebox",  # Message boxes
        "--hidden-import=winreg",       # Windows registry
        "--hidden-import=threading",    # Threading
        "--hidden-import=logging",      # Logging
        "--hidden-import=json",         # JSON processing
        "--hidden-import=datetime",     # Date/time
        "--hidden-import=time",         # Time functions
        "--add-data=zk_device_info.py;.",  # Include zk_device_info module
        "simple_zktime_app_beta.py"
    ]
    
    try:
        subprocess.check_call(cmd)
        print("✅ BETA app built successfully!")
        print("📁 Executable: dist/ZKTimeBeta.exe")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Build failed: {e}")
        return False

def main():
    """Main build process"""
    print("🧪 ZKTime BETA App Builder")
    print("=" * 40)
    
    # Check if source file exists
    if not Path("simple_zktime_app_beta.py").exists():
        print("❌ Error: simple_zktime_app_beta.py not found")
        return False
    
    # Check if zk_device_info.py exists
    if not Path("zk_device_info.py").exists():
        print("❌ Error: zk_device_info.py not found")
        return False
    
    # Install requirements first
    print("📦 Installing requirements...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
        print("✅ Requirements installed")
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install requirements: {e}")
        return False
    
    # Build the app
    success = build_beta_app()
    
    if success:
        print("\n🎉 BETA build completed successfully!")
        print("📁 Location: dist/ZKTimeBeta.exe")
        print("🚀 Ready to test on Windows!")
        print("\nBETA Features:")
        print("  🧪 BETA server: beta.sdadparts.com")
        print("  🟠 Orange icon with 'B'")
        print("  ⏱️  5-minute sync interval")
        print("  📋 Test User List menu")
        print("  📄 Enhanced logging")
        print("  ✅ System Tray icon")
        print("  ✅ Manual sync")
        print("  ✅ Auto sync")
        print("  ✅ Device status")
        print("  ✅ Settings view")
        print("  ✅ Log viewer")
        print("  ✅ No console window")
        print("  ✅ No web interface")
        print("\n⚠️  This is a BETA version for testing!")
    else:
        print("\n❌ BETA build failed!")
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 