#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test script for ZKTeco device connection
"""

import logging
import sys
import os

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from services.api_service import ApiService
from config import Config

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

def test_device_connection():
    """Test device connection and data retrieval"""
    
    config = Config()
    device_config = config.get_device_config()
    
    print(f"Testing connection to device: {device_config['ip']}:{device_config['port']}")
    print("=" * 50)
    
    # Create API service
    api_service = ApiService(
        device_ip=device_config['ip'],
        device_port=device_config['port'],
        timeout=device_config['timeout']
    )
    
    # Test 1: Basic connection
    print("\n1. Testing basic connection...")
    if api_service.test_connection():
        print("✓ Connection test successful")
    else:
        print("✗ Connection test failed")
        return False
    
    # Test 2: Get device info
    print("\n2. Testing device info retrieval...")
    device_info = api_service.get_device_info()
    if device_info:
        print("✓ Device info retrieved successfully")
        print(f"   Device Name: {device_info['device_name']}")
        print(f"   Serial Number: {device_info['serial_number']}")
        print(f"   Firmware Version: {device_info['firmware_version']}")
    else:
        print("✗ Failed to retrieve device info")
        return False
    
    # Test 3: Get users info
    print("\n3. Testing users info retrieval...")
    users = api_service.get_users_info()
    if users is not None:
        print(f"✓ Users info retrieved successfully - {len(users)} users found")
        if users:
            print(f"   First user: {users[0]['name']} (ID: {users[0]['user_id']})")
    else:
        print("✗ Failed to retrieve users info")
        return False
    
    # Test 4: Get attendance info
    print("\n4. Testing attendance info retrieval...")
    attendance = api_service.get_attendance_info()
    if attendance is not None:
        print(f"✓ Attendance info retrieved successfully - {len(attendance)} records found")
        if attendance:
            print(f"   Latest record: User {attendance[0]['user_id']} at {attendance[0]['timestamp']}")
    else:
        print("✗ Failed to retrieve attendance info")
        return False
    
    # Test 5: Get comprehensive status
    print("\n5. Testing comprehensive status retrieval...")
    status = api_service.get_device_status()
    if status:
        print("✓ Device status retrieved successfully")
        print(f"   Users Count: {status['users_count']}")
        print(f"   Attendance Count: {status['attendance_count']}")
        print(f"   Connection Status: {status['connection_status']}")
    else:
        print("✗ Failed to retrieve device status")
        return False
    
    print("\n" + "=" * 50)
    print("✓ All tests passed! Device connection is working properly.")
    return True

if __name__ == "__main__":
    try:
        success = test_device_connection()
        if success:
            print("\nDevice connection test completed successfully!")
            sys.exit(0)
        else:
            print("\nDevice connection test failed!")
            sys.exit(1)
    except Exception as e:
        logger.error(f"Test failed with exception: {e}")
        print(f"\nTest failed with exception: {e}")
        sys.exit(1) 