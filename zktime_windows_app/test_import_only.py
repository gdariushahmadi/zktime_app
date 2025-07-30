#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test script to verify imports work correctly
"""

import sys
import os

def test_imports():
    """Test that all imports work correctly"""
    print("🧪 Testing Imports")
    print("=" * 30)
    
    try:
        # Test zk_device_info import
        from zk_device_info import connect_to_device
        print("✅ zk_device_info import successful")
        
        # Test other imports
        import requests
        print("✅ requests import successful")
        
        import pystray
        print("✅ pystray import successful")
        
        from PIL import Image, ImageDraw
        print("✅ PIL import successful")
        
        import schedule
        print("✅ schedule import successful")
        
        from zk import ZK
        print("✅ zk import successful")
        
        print("\n🎉 All imports successful!")
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def main():
    """Main function"""
    print("🔧 Import Test")
    print("Testing all required modules")
    print()
    
    success = test_imports()
    
    if success:
        print("\n✅ Ready to build executable!")
        print("All required modules are available")
    else:
        print("\n❌ Some modules are missing!")
        print("Please install missing dependencies")

if __name__ == "__main__":
    main() 