#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Simple build script for ZKTime Simple App
"""

import os
import sys
import subprocess
from pathlib import Path

def build_simple_app():
    """Build the simple ZKTime app"""
    print("Building Simple ZKTime App...")
    
    # PyInstaller command for simple app
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--onefile",                    # Single executable file
        "--windowed",                   # No console window
        "--name=ZKTimeSimple",          # Executable name
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
        "simple_zktime_app.py"
    ]
    
    try:
        subprocess.check_call(cmd)
        print("✅ Simple app built successfully!")
        print("📁 Executable: dist/ZKTimeSimple.exe")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Build failed: {e}")
        return False

def main():
    """Main build process"""
    print("🔨 ZKTime Simple App Builder")
    print("=" * 40)
    
    # Check if source file exists
    if not Path("simple_zktime_app.py").exists():
        print("❌ Error: simple_zktime_app.py not found")
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
    success = build_simple_app()
    
    if success:
        print("\n🎉 Build completed successfully!")
        print("📁 Location: dist/ZKTimeSimple.exe")
        print("🚀 Ready to run on Windows!")
        print("\nFeatures:")
        print("  ✅ System Tray icon")
        print("  ✅ Manual sync")
        print("  ✅ Auto sync (every hour)")
        print("  ✅ Device status")
        print("  ✅ Settings view")
        print("  ✅ Log viewer")
        print("  ✅ No console window")
        print("  ✅ No web interface")
    else:
        print("\n❌ Build failed!")
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)