#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test script to verify user name extraction using zk_device_info
"""

import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from zk_device_info import connect_to_device

def test_user_names():
    """Test user name extraction as requested"""
    print("🧪 Testing User Name Extraction")
    print("=" * 40)
    
    # تنظیمات دستگاه (لطفاً مقادیر را با اطلاعات دستگاه خود جایگزین کنید)
    device_ip = '192.168.70.141'  # آدرس IP دستگاه
    device_port = 4370            # پورت دستگاه (معمولاً 4370)
    timeout = 5                   # زمان انتظار برای اتصال (ثانیه)

    # اتصال به دستگاه
    conn = connect_to_device(device_ip, device_port, timeout)
    if not conn:
        print("اتصال به دستگاه برقرار نشد!")
        return False
    else:
        try:
            users = conn.get_users()
            print(f"\n=== لیست کاربران ({len(users)} کاربر) ===")
            user_dict = {}
            for i, user in enumerate(users, 1):
                print(f"{i}. نام: {user.name}, شناسه: {user.user_id}")
                user_dict[user.user_id] = user.name
            
            print(f"\n✅ تست موفق! {len(user_dict)} کاربر دریافت شد")
            print("\n📋 دیکشنری کاربران:")
            for user_id, name in user_dict.items():
                print(f"  {user_id}: {name}")
                
            return True
        except Exception as e:
            print(f"[!] خطا در دریافت لیست کاربران: {e}")
            return False
        finally:
            conn.disconnect()
            print("\nاتصال به دستگاه قطع شد.")

def main():
    """Main function"""
    print("🔧 User Name Extraction Test")
    print("Using the exact code you provided")
    print()
    
    success = test_user_names()
    
    if success:
        print("\n🎉 تست با موفقیت انجام شد!")
        print("✅ کد شما به درستی نام کاربران را استخراج می‌کند")
        print("✅ این کد در برنامه اصلی استفاده شده است")
    else:
        print("\n❌ تست ناموفق!")
        print("⚠️  لطفاً اتصال شبکه و تنظیمات دستگاه را بررسی کنید")

if __name__ == "__main__":
    main()