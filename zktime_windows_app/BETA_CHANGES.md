# تغییرات اعمال شده برای نسخه BETA

## ✅ استفاده از کد شما برای نام کاربران

### کد اصلی شما:
```python
from zk_device_info import connect_to_device

# تنظیمات دستگاه
device_ip = '192.168.70.141'
device_port = 4370
timeout = 5

# اتصال به دستگاه
conn = connect_to_device(device_ip, device_port, timeout)
if not conn:
    print("اتصال به دستگاه برقرار نشد!")
else:
    try:
        users = conn.get_users()
        print(f"\n=== لیست کاربران ({len(users)} کاربر) ===")
        for i, user in enumerate(users, 1):
            print(f"{i}. نام: {user.name}, شناسه: {user.user_id}")
    except Exception as e:
        print(f"[!] خطا در دریافت لیست کاربران: {e}")
    finally:
        conn.disconnect()
        print("\nاتصال به دستگاه قطع شد.")
```

### ✅ تغییرات اعمال شده:

1. **در `simple_zktime_app.py`**:
   ```python
   # اضافه شد
   from zk_device_info import connect_to_device
   
   # تابع اتصال تغییر کرد
   def connect_to_device_local(self):
       conn = connect_to_device(self.DEVICE_IP, self.DEVICE_PORT, self.DEVICE_TIMEOUT)
       return conn
   ```

2. **نسخه BETA جدید**: `simple_zktime_app_beta.py`
   - استفاده از سرور BETA: `https://beta.sdadparts.com/api/attendance/device-import`
   - آیکون نارنجی با "B" به جای آبی با "Z"
   - فاصله همگام‌سازی 5 دقیقه برای تست
   - لاگ جداگانه: `zktime_beta_test.log`

## 🧪 فایل‌های جدید:

1. **`simple_zktime_app_beta.py`** - نسخه BETA با سرور تست
2. **`build_beta.bat`** - ساخت نسخه BETA
3. **`test_user_names.py`** - تست استخراج نام کاربران
4. **`BETA_CHANGES.md`** - این فایل

## 🎯 نحوه استفاده:

### برای نسخه عادی (سرور اصلی):
```cmd
build_simple.bat
# خروجی: dist/ZKTimeSimple.exe
```

### برای نسخه BETA (سرور تست):
```cmd
build_beta.bat
# خروجی: dist/ZKTimeBeta.exe
```

### تست نام کاربران:
```cmd
python test_user_names.py
```

## 🔧 تفاوت‌های نسخه BETA:

| ویژگی | نسخه عادی | نسخه BETA |
|-------|------------|------------|
| **سرور** | panel.sdadparts.com | **beta.sdadparts.com** |
| **آیکون** | آبی با "Z" | **نارنجی با "B"** |
| **فاصله همگام‌سازی** | 1 ساعت | **5 دقیقه** |
| **لاگ** | zktime_simple.log | **zktime_beta_test.log** |
| **منو** | عادی | **BETA نشان‌دار** |

## ✅ ویژگی‌های جدید نسخه BETA:

- **Test User List** - تست مستقیم لیست کاربران
- **Enhanced Logging** - لاگ کامل برای debugging
- **BETA Server** - ارسال به سرور تست
- **Quick Sync** - همگام‌سازی هر 5 دقیقه
- **User Name Display** - نمایش نام کاربران در messagebox

## 🚀 مزایا:

✅ **کد شما به کار گرفته شد** - دقیقاً همان تابع `connect_to_device`  
✅ **نسخه BETA جداگانه** - بدون تداخل با نسخه اصلی  
✅ **سرور تست** - امن برای آزمایش  
✅ **لاگ کامل** - همه جزئیات ثبت می‌شود  
✅ **تست آسان** - منوی جداگانه برای تست کاربران  

## 📋 دستورات:

```cmd
# نسخه عادی
build_simple.bat

# نسخه BETA  
build_beta.bat

# تست نام کاربران
python test_user_names.py
```

**حالا کد شما در برنامه استفاده می‌شود و نسخه BETA برای تست آماده است!** 🎉