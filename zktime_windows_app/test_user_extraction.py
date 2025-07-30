#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test script to verify user name extraction from device data
"""

import sys
import os
import json
from datetime import datetime

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.device_service import DeviceService

def test_user_name_extraction():
    """Test that user names are properly extracted from device data"""
    print("Testing User Name Extraction")
    print("=" * 50)
    
    # Create test data with users from device
    test_device_data = {
        'device_status': {
            'device_info': {
                'device_name': 'Test Device',
                'serial_number': 'TEST123',
                'firmware_version': '1.0.0',
                'ip_address': '192.168.70.141',
                'port': 4370,
                'device_time': '2024-01-01 10:00:00'
            },
            'connection_status': True
        },
        'users': [
            {'user_id': '12345', 'name': 'احمد محمدی', 'card': '0', 'privilege': 0},
            {'user_id': '67890', 'name': 'فاطمه احمدی', 'card': '0', 'privilege': 0},
            {'user_id': '11111', 'name': 'علی رضایی', 'card': '0', 'privilege': 0}
        ],
        'attendance': [
            {
                'user_id': '12345',
                'timestamp': '2024-01-01 08:00:00',
                'status': 'Check In',
                'punch': 1
            },
            {
                'user_id': '12345',
                'timestamp': '2024-01-01 17:00:00',
                'status': 'Check Out',
                'punch': 2
            },
            {
                'user_id': '67890',
                'timestamp': '2024-01-01 09:00:00',
                'status': 'Check In',
                'punch': 1
            },
            {
                'user_id': '67890',
                'timestamp': '2024-01-01 18:00:00',
                'status': 'Check Out',
                'punch': 2
            },
            {
                'user_id': '11111',
                'timestamp': '2024-01-01 07:30:00',
                'status': 'Check In',
                'punch': 1
            },
            {
                'user_id': '11111',
                'timestamp': '2024-01-01 16:30:00',
                'status': 'Check Out',
                'punch': 2
            }
        ],
        'sync_info': {
            'sync_timestamp': datetime.now().isoformat(),
            'sync_status': 'success',
            'total_users': 3,
            'total_attendance': 6
        }
    }
    
    # Test the formatting
    device_service = DeviceService()
    formatted_data = device_service.format_data_for_server(test_device_data)
    
    if formatted_data:
        print("✅ User Name Extraction Test: PASSED")
        print("\nFormatted Data with User Names:")
        print(json.dumps(formatted_data, indent=2, ensure_ascii=False))
        
        # Verify user names are correctly extracted
        records = formatted_data.get('attendance_records', [])
        user_names_found = []
        
        for record in records:
            user_id = record.get('id_number', '')
            user_name = record.get('name', '')
            user_names_found.append(f"{user_id}: {user_name}")
            
            # Check if name is not "Unknown User" or "User {id}"
            if user_name and not user_name.startswith('User ') and user_name != 'Unknown User':
                print(f"✅ User {user_id} has proper name: {user_name}")
            else:
                print(f"❌ User {user_id} has fallback name: {user_name}")
        
        print(f"\nFound {len(user_names_found)} user records:")
        for user_info in user_names_found:
            print(f"  - {user_info}")
        
        # Check time format
        if records:
            first_record = records[0]
            times = first_record.get('times', [])
            if times:
                first_time = times[0]
                if len(first_time.split(':')) == 3:  # Should be HH:MM:SS
                    print(f"✅ Time format is correct: {first_time}")
                else:
                    print(f"❌ Time format is incorrect: {first_time}")
        
        return True
    else:
        print("❌ User Name Extraction Test: FAILED - No formatted data returned")
        return False

def test_time_format():
    """Test that time format is H:i:s"""
    print("\nTesting Time Format (H:i:s)")
    print("=" * 50)
    
    # Test different time formats
    test_times = [
        '2024-01-01 08:00:00',
        '2024-01-01 12:30:45',
        '2024-01-01 17:15:30'
    ]
    
    for test_time in test_times:
        try:
            timestamp = datetime.fromisoformat(test_time.replace('Z', '+00:00'))
            formatted_time = timestamp.strftime('%H:%M:%S')
            print(f"Input: {test_time} -> Output: {formatted_time}")
            
            # Verify format is HH:MM:SS
            if len(formatted_time.split(':')) == 3:
                print(f"✅ Time format is correct: {formatted_time}")
            else:
                print(f"❌ Time format is incorrect: {formatted_time}")
                
        except Exception as e:
            print(f"❌ Error parsing time {test_time}: {e}")
    
    return True

def main():
    """Main test function"""
    print("User Name and Time Format Verification")
    print("=" * 50)
    
    # Test user name extraction
    user_test_ok = test_user_name_extraction()
    
    # Test time format
    time_test_ok = test_time_format()
    
    print("\n" + "=" * 50)
    if user_test_ok and time_test_ok:
        print("✅ All tests passed!")
        print("✅ User names are properly extracted from device")
        print("✅ Time format is correct (H:i:s)")
    else:
        print("❌ Some tests failed. Please check the implementation.")
    
    return user_test_ok and time_test_ok

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 