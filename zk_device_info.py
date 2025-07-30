#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ZKTeco Device Information Retrieval Script
This script connects to a ZKTeco device and retrieves basic information.
"""

from zk import ZK
import sys
import time

def connect_to_device(device_ip, device_port=4370, timeout=5):
    """
    Connect to ZKTeco device and return connection object
    """
    zk = ZK(device_ip, port=device_port, timeout=timeout)
    try:
        conn = zk.connect()
        print(f"[+] اتصال برقرار شد به {device_ip}:{device_port}")
        return conn
    except Exception as e:
        print(f"[!] خطا در اتصال به دستگاه: {e}")
        return None

def get_device_info(conn):
    """
    Retrieve and display device information
    """
    try:
        print("\n=== اطلاعات دستگاه ===")
        
        # اطلاعات پایه
        device_name = conn.get_device_name()
        print(f"→ نام دستگاه: {device_name}")
        
        serial_number = conn.get_serialnumber()
        print(f"→ شماره سریال: {serial_number}")
        
        firmware_version = conn.get_firmware_version()
        print(f"→ ورژن فریمور: {firmware_version}")
        
        # اطلاعات کاربران
        users = conn.get_users()
        print(f"→ تعداد کاربران: {len(users)}")
        
        # اطلاعات حضور و غیاب
        attendance = conn.get_attendance()
        print(f"→ تعداد حضور و غیاب: {len(attendance)}")
        
        # اطلاعات اضافی
        try:
            device_time = conn.get_time()
            print(f"→ زمان دستگاه: {device_time}")
        except:
            print("→ زمان دستگاه: در دسترس نیست")
            
        try:
            device_info = conn.get_device_info()
            print(f"→ اطلاعات کامل دستگاه: {device_info}")
        except:
            print("→ اطلاعات کامل دستگاه: در دسترس نیست")
            
        return True
        
    except Exception as e:
        print(f"[!] خطا در دریافت اطلاعات: {e}")
        return False

def get_users_list(conn):
    """
    Display list of users
    """
    try:
        users = conn.get_users()
        print(f"\n=== لیست کاربران ({len(users)} کاربر) ===")
        for i, user in enumerate(users, 1):
            print(f"{i}. نام: {user.name}, شناسه: {user.user_id}, کارت: {user.card}")
    except Exception as e:
        print(f"[!] خطا در دریافت لیست کاربران: {e}")

def get_attendance_list(conn):
    """
    Display recent attendance records
    """
    try:
        attendance = conn.get_attendance()
        print(f"\n=== آخرین حضور و غیاب ({len(attendance)} رکورد) ===")
        for i, record in enumerate(attendance[-10:], 1):  # Show last 10 records
            print(f"{i}. کاربر: {record.user_id}, زمان: {record.timestamp}, وضعیت: {record.status}")
    except Exception as e:
        print(f"[!] خطا در دریافت حضور و غیاب: {e}")

def main():
    """
    Main function
    """
    # تنظیمات اتصال به دستگاه
    device_ip = '192.168.70.141'
    device_port = 4370
    timeout = 5
    
    print("=== ZKTeco Device Information Tool ===")
    print(f"تلاش برای اتصال به {device_ip}:{device_port}")
    
    # اتصال به دستگاه
    conn = connect_to_device(device_ip, device_port, timeout)
    if not conn:
        print("[!] نتوانست به دستگاه متصل شود")
        sys.exit(1)
    
    try:
        # دریافت اطلاعات پایه
        if get_device_info(conn):
            print("\n[+] اطلاعات با موفقیت دریافت شد")
        
        # نمایش لیست کاربران
        get_users_list(conn)
        
        # نمایش حضور و غیاب
        get_attendance_list(conn)
        
    except Exception as e:
        print(f"[!] خطای غیرمنتظره: {e}")
    
    finally:
        # قطع اتصال
        try:
            conn.disconnect()
            print("\n[+] اتصال قطع شد")
        except:
            print("\n[!] خطا در قطع اتصال")

if __name__ == "__main__":
    main() 