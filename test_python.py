#!/usr/bin/env python3
# -*- coding: utf-8 -*-

print("=== Python Test Script ===")
print("Python is working!")

try:
    from zk import ZK
    print("✓ pyzk library imported successfully")
    
    # Test basic ZK functionality
    print("✓ ZK class available")
    
    # Test connection (without actually connecting)
    print("Testing ZK initialization...")
    zk = ZK('192.168.70.141', port=4370, timeout=5)
    print("✓ ZK object created successfully")
    
    print("\n=== All tests passed! ===")
    print("Your environment is ready to run the main script.")
    
except ImportError as e:
    print(f"✗ Error importing pyzk: {e}")
    print("Please install pyzk: pip install pyzk==0.9")
except Exception as e:
    print(f"✗ Error: {e}")

input("Press Enter to continue...") 