#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test script to verify API data format matches the required specification
"""

import sys
import os
import json
from datetime import datetime, timedelta

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.device_service import DeviceService

def create_test_data():
    """Create test attendance data to verify API format"""
    test_attendance = [
        {
            'user_id': '12345',
            'timestamp': '2024-01-01 08:00:00',
            'status': 'Check In',
            'punch': 1
        },
        {
            'user_id': '12345',
            'timestamp': '2024-01-01 12:00:00',
            'status': 'Check Out',
            'punch': 2
        },
        {
            'user_id': '12345',
            'timestamp': '2024-01-01 13:00:00',
            'status': 'Check In',
            'punch': 3
        },
        {
            'user_id': '12345',
            'timestamp': '2024-01-01 17:00:00',
            'status': 'Check Out',
            'punch': 4
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
        }
    ]
    
    return test_attendance

def test_api_format():
    """Test the API data format"""
    print("Testing API Data Format")
    print("=" * 50)
    
    # Create test device data
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
            {'user_id': '12345', 'name': 'John Doe', 'card': '0', 'privilege': 0},
            {'user_id': '67890', 'name': 'Jane Smith', 'card': '0', 'privilege': 0}
        ],
        'attendance': create_test_data(),
        'sync_info': {
            'sync_timestamp': datetime.now().isoformat(),
            'sync_status': 'success',
            'total_users': 2,
            'total_attendance': 6
        }
    }
    
    # Test the formatting
    device_service = DeviceService()
    formatted_data = device_service.format_data_for_server(test_device_data)
    
    if formatted_data:
        print("✅ API Format Test: PASSED")
        print("\nFormatted Data Structure:")
        print(json.dumps(formatted_data, indent=2, ensure_ascii=False))
        
        # Verify required fields
        required_fields = ['period', 'attendance_records']
        missing_fields = [field for field in required_fields if field not in formatted_data]
        
        if missing_fields:
            print(f"❌ Missing required fields: {missing_fields}")
            return False
        
        # Verify period structure
        period = formatted_data.get('period', {})
        if 'start_date' not in period or 'end_date' not in period:
            print("❌ Period object missing required fields")
            return False
        
        # Verify attendance records structure
        records = formatted_data.get('attendance_records', [])
        if not isinstance(records, list):
            print("❌ Attendance records should be an array")
            return False
        
        print(f"✅ Found {len(records)} attendance records")
        
        # Check first record structure
        if records:
            first_record = records[0]
            required_record_fields = ['date', 'id_number', 'name', 'times', 'card']
            missing_record_fields = [field for field in required_record_fields if field not in first_record]
            
            if missing_record_fields:
                print(f"❌ Record missing required fields: {missing_record_fields}")
                return False
            
            print("✅ Record structure is correct")
            
            # Check if daily details are included
            if 'daily' in first_record:
                daily = first_record['daily']
                if 'attendance_details' in daily:
                    print(f"✅ Daily details included with {len(daily['attendance_details'])} entries")
        
        return True
    else:
        print("❌ API Format Test: FAILED - No formatted data returned")
        return False

def test_api_endpoint():
    """Test the API endpoint configuration"""
    print("\nTesting API Endpoint Configuration")
    print("=" * 50)
    
    from config import Config
    
    config = Config()
    server_config = config.get_server_config()
    
    print(f"API URL: {server_config['url']}")
    print(f"Token: {server_config['token'][:10]}...")
    print(f"Timeout: {server_config['timeout']} seconds")
    print(f"Retry Attempts: {server_config['retry_attempts']}")
    
    # Check if URL matches the required endpoint
    expected_url = "https://panel.sdadparts.com/api/attendance/device-import"
    if server_config['url'] == expected_url:
        print("✅ API URL matches required endpoint")
        return True
    else:
        print(f"❌ API URL mismatch. Expected: {expected_url}, Got: {server_config['url']}")
        return False

def create_sample_request():
    """Create a sample API request for testing"""
    print("\nSample API Request")
    print("=" * 50)
    
    sample_data = {
        "period": {
            "start_date": "2024-01-01",
            "end_date": "2024-01-01"
        },
        "attendance_records": [
            {
                "date": "2024-01-01",
                "id_number": "12345",
                "name": "John Doe",
                "times": ["08:00", "12:00", "13:00", "17:00"],
                "card": "0",
                "daily": {
                    "date": "2024-01-01",
                    "user_id": "12345",
                    "attendance_details": [
                        {
                            "date": "2024-01-01",
                            "id_number": "12345",
                            "name": "John Doe",
                            "time": "08:00",
                            "status": "Check In",
                            "verification": "Fingerprint"
                        },
                        {
                            "date": "2024-01-01",
                            "id_number": "12345",
                            "name": "John Doe",
                            "time": "12:00",
                            "status": "Check Out",
                            "verification": "Fingerprint"
                        },
                        {
                            "date": "2024-01-01",
                            "id_number": "12345",
                            "name": "John Doe",
                            "time": "13:00",
                            "status": "Check In",
                            "verification": "Fingerprint"
                        },
                        {
                            "date": "2024-01-01",
                            "id_number": "12345",
                            "name": "John Doe",
                            "time": "17:00",
                            "status": "Check Out",
                            "verification": "Fingerprint"
                        }
                    ]
                }
            }
        ]
    }
    
    print("Sample curl command:")
    print("curl -X POST https://panel.sdadparts.com/api/attendance/device-import \\")
    print("  -H \"Content-Type: application/json\" \\")
    print("  -H \"Accept: application/json\" \\")
    print("  -H \"Authorization: Bearer 3|4GQYfJgpAhjlZfumsMMBrKvZyr68L9hVA3V9u5Fnd983ce66\" \\")
    print("  -d '" + json.dumps(sample_data, indent=2) + "'")
    
    return sample_data

def main():
    """Main test function"""
    print("ZKTeco API Format Verification")
    print("=" * 50)
    
    # Test API endpoint configuration
    endpoint_ok = test_api_endpoint()
    
    # Test API data format
    format_ok = test_api_format()
    
    # Create sample request
    create_sample_request()
    
    print("\n" + "=" * 50)
    if endpoint_ok and format_ok:
        print("✅ All tests passed! API format is correct.")
        print("The application is ready to send data in the required format.")
    else:
        print("❌ Some tests failed. Please check the configuration.")
    
    return endpoint_ok and format_ok

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 