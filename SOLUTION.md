# راه‌حل کامل برای اجرای اسکریپت ZKTeco

## مشکل فعلی
ترمینال PowerShell مشکل encoding دارد و نمی‌تواند دستورات را به درستی اجرا کند.

## راه‌حل‌های مختلف

### راه‌حل 1: استفاده از Command Prompt
1. کلید `Win + R` را فشار دهید
2. `cmd` را تایپ کنید و Enter بزنید
3. به پوشه پروژه بروید:
   ```cmd
   cd "C:\Users\SD-MGH\OneDrive\Desktop\ZKTimenet3.0.4.4-4\tapi"
   ```
4. اسکریپت را اجرا کنید:
   ```cmd
   python test_python.py
   ```
5. اگر موفق بود، اسکریپت اصلی را اجرا کنید:
   ```cmd
   python zk_device_info.py
   ```

### راه‌حل 2: استفاده از PowerShell جدید
1. کلید `Win + X` را فشار دهید
2. "Windows PowerShell" یا "Terminal" را انتخاب کنید
3. به پوشه پروژه بروید:
   ```powershell
   cd "C:\Users\SD-MGH\OneDrive\Desktop\ZKTimenet3.0.4.4-4\tapi"
   ```
4. اسکریپت را اجرا کنید:
   ```powershell
   python test_python.py
   ```

### راه‌حل 3: استفاده از فایل‌های اجرایی
1. روی فایل `run_script.bat` دوبار کلیک کنید
2. یا روی فایل `run_script.ps1` راست کلیک کرده و "Run with PowerShell" را انتخاب کنید

### راه‌حل 4: استفاده از IDE
1. VS Code یا PyCharm را باز کنید
2. پوشه پروژه را باز کنید
3. فایل `test_python.py` را باز کنید
4. F5 را فشار دهید یا Run را کلیک کنید

## فایل‌های موجود

- `zk_device_info.py` - اسکریپت اصلی
- `test_python.py` - اسکریپت تست (برای بررسی نصب)
- `run_script.bat` - فایل اجرایی CMD
- `run_script.ps1` - فایل اجرایی PowerShell
- `requirements.txt` - فایل وابستگی‌ها
- `README.md` - راهنمای کامل

## مراحل تست

1. ابتدا `test_python.py` را اجرا کنید تا مطمئن شوید همه چیز درست نصب شده
2. اگر تست موفق بود، `zk_device_info.py` را اجرا کنید
3. اگر خطا داشتید، مطمئن شوید که:
   - Python نصب است
   - pyzk نصب است: `pip install pyzk==0.9`
   - آدرس IP دستگاه صحیح است

## تنظیمات دستگاه

در فایل `zk_device_info.py` این خط را پیدا کنید و آدرس IP دستگاه خود را وارد کنید:
```python
device_ip = '192.168.70.141'  # آدرس IP دستگاه خود را وارد کنید
```

## عیب‌یابی

- اگر خطای "ModuleNotFoundError" داشتید: `pip install pyzk==0.9`
- اگر خطای اتصال داشتید: آدرس IP و پورت را بررسی کنید
- اگر خطای encoding داشتید: از Command Prompt استفاده کنید 