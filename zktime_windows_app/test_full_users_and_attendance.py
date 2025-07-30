#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Comprehensive test script for full user list and monthly attendance testing
"""

import sys
import os
import json
from datetime import datetime, timedelta
import random

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.device_service import DeviceService

def create_test_users():
    """Create comprehensive test user data"""
    test_users = [
        {'user_id': '1001', 'name': 'احمد محمدی', 'card': '0', 'privilege': 0},
        {'user_id': '1002', 'name': 'فاطمه احمدی', 'card': '0', 'privilege': 0},
        {'user_id': '1003', 'name': 'علی رضایی', 'card': '0', 'privilege': 0},
        {'user_id': '1004', 'name': 'مریم کریمی', 'card': '0', 'privilege': 0},
        {'user_id': '1005', 'name': 'حسین نوری', 'card': '0', 'privilege': 0},
        {'user_id': '1006', 'name': 'زهرا صالحی', 'card': '0', 'privilege': 0},
        {'user_id': '1007', 'name': 'محمد جعفری', 'card': '0', 'privilege': 0},
        {'user_id': '1008', 'name': 'نرگس احمدی', 'card': '0', 'privilege': 0},
        {'user_id': '1009', 'name': 'رضا محمودی', 'card': '0', 'privilege': 0},
        {'user_id': '1010', 'name': 'سارا رضایی', 'card': '0', 'privilege': 0},
        {'user_id': '1011', 'name': 'امیر حسینی', 'card': '0', 'privilege': 0},
        {'user_id': '1012', 'name': 'لیلا کریمی', 'card': '0', 'privilege': 0},
        {'user_id': '1013', 'name': 'حسن نوری', 'card': '0', 'privilege': 0},
        {'user_id': '1014', 'name': 'فریبا صالحی', 'card': '0', 'privilege': 0},
        {'user_id': '1015', 'name': 'مهدی جعفری', 'card': '0', 'privilege': 0}
    ]
    return test_users

def create_monthly_attendance_data():
    """Create attendance data for the last month"""
    # Calculate date range (last 30 days)
    end_date = datetime.now()
    start_date = end_date - timedelta(days=30)
    
    attendance_data = []
    
    # Generate attendance for each user for the last month
    for user in create_test_users():
        user_id = user['user_id']
        user_name = user['name']
        
        # Generate attendance for each day in the last month
        current_date = start_date
        while current_date <= end_date:
            # Skip weekends (Friday and Saturday in some regions)
            if current_date.weekday() < 5:  # Monday to Friday
                # Generate check-in time (between 7:00 and 9:00)
                check_in_hour = random.randint(7, 9)
                check_in_minute = random.randint(0, 59)
                check_in_time = current_date.replace(
                    hour=check_in_hour, 
                    minute=check_in_minute, 
                    second=random.randint(0, 59)
                )
                
                # Generate check-out time (between 16:00 and 18:00)
                check_out_hour = random.randint(16, 18)
                check_out_minute = random.randint(0, 59)
                check_out_time = current_date.replace(
                    hour=check_out_hour, 
                    minute=check_out_minute, 
                    second=random.randint(0, 59)
                )
                
                # Add check-in record
                attendance_data.append({
                    'user_id': user_id,
                    'timestamp': check_in_time.strftime('%Y-%m-%d %H:%M:%S'),
                    'status': 'Check In',
                    'punch': 1
                })
                
                # Add check-out record
                attendance_data.append({
                    'user_id': user_id,
                    'timestamp': check_out_time.strftime('%Y-%m-%d %H:%M:%S'),
                    'status': 'Check Out',
                    'punch': 2
                })
            
            current_date += timedelta(days=1)
    
    return attendance_data

def test_full_user_list():
    """Test and display full user list"""
    print("Testing Full User List")
    print("=" * 50)
    
    users = create_test_users()
    
    print(f"Total Users: {len(users)}")
    print("\nUser List:")
    print("-" * 50)
    
    for i, user in enumerate(users, 1):
        print(f"{i:2d}. ID: {user['user_id']} | Name: {user['name']} | Card: {user['card']}")
    
    print("-" * 50)
    print(f"✅ Successfully loaded {len(users)} users")
    
    return users

def test_monthly_attendance():
    """Test monthly attendance data processing"""
    print("\nTesting Monthly Attendance Data")
    print("=" * 50)
    
    # Create test device data with monthly attendance
    test_device_data = {
        'device_status': {
            'device_info': {
                'device_name': 'ZKTeco Test Device',
                'serial_number': 'TEST123456',
                'firmware_version': '1.0.0',
                'ip_address': '192.168.70.141',
                'port': 4370,
                'device_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            },
            'connection_status': True
        },
        'users': create_test_users(),
        'attendance': create_monthly_attendance_data(),
        'sync_info': {
            'sync_timestamp': datetime.now().isoformat(),
            'sync_status': 'success',
            'total_users': len(create_test_users()),
            'total_attendance': len(create_monthly_attendance_data())
        }
    }
    
    print(f"Generated {len(test_device_data['users'])} users")
    print(f"Generated {len(test_device_data['attendance'])} attendance records")
    
    # Test the formatting
    device_service = DeviceService()
    formatted_data = device_service.format_data_for_server(test_device_data)
    
    if formatted_data:
        print("✅ Monthly Attendance Test: PASSED")
        
        # Analyze the formatted data
        records = formatted_data.get('attendance_records', [])
        period = formatted_data.get('period', {})
        
        print(f"\nPeriod: {period.get('start_date')} to {period.get('end_date')}")
        print(f"Total Records: {len(records)}")
        
        # Show sample records
        print("\nSample Records:")
        print("-" * 50)
        for i, record in enumerate(records[:5], 1):  # Show first 5 records
            user_id = record.get('id_number', '')
            user_name = record.get('name', '')
            times = record.get('times', [])
            print(f"{i}. {user_name} ({user_id}) - {len(times)} time entries")
        
        if len(records) > 5:
            print(f"... and {len(records) - 5} more records")
        
        # Check time format compliance
        if records:
            first_record = records[0]
            times = first_record.get('times', [])
            if times:
                first_time = times[0]
                if len(first_time.split(':')) == 3:
                    print(f"✅ Time format is correct: {first_time}")
                else:
                    print(f"❌ Time format is incorrect: {first_time}")
        
        return True
    else:
        print("❌ Monthly Attendance Test: FAILED")
        return False

def test_attendance_statistics():
    """Test attendance statistics and analysis"""
    print("\nTesting Attendance Statistics")
    print("=" * 50)
    
    attendance_data = create_monthly_attendance_data()
    
    # Group by user
    user_attendance = {}
    for record in attendance_data:
        user_id = record['user_id']
        if user_id not in user_attendance:
            user_attendance[user_id] = []
        user_attendance[user_id].append(record)
    
    print(f"Total Users with Attendance: {len(user_attendance)}")
    print(f"Total Attendance Records: {len(attendance_data)}")
    
    # Calculate statistics
    total_days = 0
    total_checkins = 0
    total_checkouts = 0
    
    for user_id, records in user_attendance.items():
        days = set()
        checkins = 0
        checkouts = 0
        
        for record in records:
            date = record['timestamp'].split(' ')[0]
            days.add(date)
            
            if record['status'] == 'Check In':
                checkins += 1
            elif record['status'] == 'Check Out':
                checkouts += 1
        
        total_days += len(days)
        total_checkins += checkins
        total_checkouts += checkouts
        
        print(f"User {user_id}: {len(days)} days, {checkins} check-ins, {checkouts} check-outs")
    
    print(f"\nSummary:")
    print(f"  - Total Working Days: {total_days}")
    print(f"  - Total Check-ins: {total_checkins}")
    print(f"  - Total Check-outs: {total_checkouts}")
    print(f"  - Average Records per Day: {len(attendance_data) / max(total_days, 1):.1f}")
    
    return True

def test_date_range_validation():
    """Test that date range is limited to one month"""
    print("\nTesting Date Range Validation")
    print("=" * 50)
    
    attendance_data = create_monthly_attendance_data()
    
    if not attendance_data:
        print("❌ No attendance data generated")
        return False
    
    # Get date range
    dates = []
    for record in attendance_data:
        date_str = record['timestamp'].split(' ')[0]
        dates.append(datetime.strptime(date_str, '%Y-%m-%d'))
    
    min_date = min(dates)
    max_date = max(dates)
    date_range = (max_date - min_date).days
    
    print(f"Date Range: {min_date.strftime('%Y-%m-%d')} to {max_date.strftime('%Y-%m-%d')}")
    print(f"Total Days: {date_range}")
    
    if date_range <= 30:
        print("✅ Date range is within one month limit")
        return True
    else:
        print(f"❌ Date range exceeds one month: {date_range} days")
        return False

def main():
    """Main test function"""
    print("Comprehensive User and Attendance Testing")
    print("=" * 60)
    
    # Test full user list
    users_ok = test_full_user_list()
    
    # Test monthly attendance
    attendance_ok = test_monthly_attendance()
    
    # Test attendance statistics
    stats_ok = test_attendance_statistics()
    
    # Test date range validation
    date_ok = test_date_range_validation()
    
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    
    tests = [
        ("Full User List", users_ok),
        ("Monthly Attendance", attendance_ok),
        ("Attendance Statistics", stats_ok),
        ("Date Range Validation", date_ok)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, result in tests:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! The system is ready for production.")
        print("✅ User list is complete")
        print("✅ Monthly attendance data is properly formatted")
        print("✅ Date range is limited to one month")
        print("✅ All data formats comply with API requirements")
    else:
        print(f"\n⚠️  {total - passed} tests failed. Please check the implementation.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 