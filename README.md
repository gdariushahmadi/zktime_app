# ZKTeco Device Information System

سیستم جامع اطلاعات دستگاه ZKTeco برای همگام‌سازی اطلاعات با سرور مرکزی

## Overview

این سیستم برای دریافت اطلاعات دستگاه‌های ZKTeco و ارسال آن‌ها به سرور مرکزی طراحی شده است. سیستم شامل چندین کامپوننت است که با هم کار می‌کنند تا اطلاعات دستگاه را دریافت، پردازش و به سرور هدف ارسال کنند.

## System Architecture

### Components

1. **DeviceService** - سرویس اصلی برای عملیات اطلاعات دستگاه
2. **ApiService** - مدیریت ارتباط با دستگاه‌های ZKTeco
3. **DeviceController** - کنترلر API برای عملیات دستگاه
4. **Web Interface** - رابط وب برای مدیریت دستگاه
5. **Sync Command** - اسکریپت خط فرمان برای همگام‌سازی زمان‌بندی شده

### Data Flow

```
ZKTeco Device → ApiService → DeviceService → Target Server
```

## Configuration

### Environment Variables

این متغیرها را در فایل `.env` یا به عنوان متغیرهای محیطی تنظیم کنید:

```env
# Device Configuration
DEVICE_IP=192.168.70.141
DEVICE_PORT=4370
DEVICE_TIMEOUT=5

# Target Server Configuration
TARGET_SERVER_URL=https://panel.sdadparts.com/api/device/import
TARGET_SERVER_TOKEN=3|4GQYfJgpAhjlZfumsMMBrKvZyr68L9hVA3V9u5Fnd983ce66

# Sync Configuration
SYNC_INTERVAL=3600
SYNC_START_TIME=00:00
SYNC_END_TIME=23:59

# Logging Configuration
LOG_LEVEL=INFO
LOG_FILE=device_sync.log

# API Configuration
API_TIMEOUT=30
API_RETRY_ATTEMPTS=3
API_RETRY_DELAY=5
```

## Installation

### پیش‌نیازها

- Python 3.6 یا بالاتر
- کتابخانه‌های مورد نیاز

### نصب

1. نصب وابستگی‌ها:
```bash
pip install -r requirements.txt
```

2. کپی فایل تنظیمات:
```bash
cp env_example.txt .env
```

3. ویرایش تنظیمات در فایل `.env`

## Core Services

### 1. ApiService (`services/api_service.py`)

مدیریت ارتباط مستقیم با دستگاه‌های ZKTeco.

#### متدهای کلیدی:

- **`connect()`** - اتصال به دستگاه
- **`get_device_info()`** - دریافت اطلاعات پایه دستگاه
- **`get_users_info()`** - دریافت لیست کاربران
- **`get_attendance_info()`** - دریافت اطلاعات حضور و غیاب
- **`get_device_status()`** - دریافت وضعیت کامل دستگاه

#### استفاده:
```python
from services.api_service import ApiService

api_service = ApiService('192.168.70.141', 4370, 5)
if api_service.connect():
    device_info = api_service.get_device_info()
    print(f"Device: {device_info['device_name']}")
```

### 2. DeviceService (`services/device_service.py`)

سرویس اصلی برای عملیات اطلاعات دستگاه.

#### متدهای کلیدی:

- **`get_device_data()`** - دریافت اطلاعات کامل دستگاه
- **`sync_device_data()`** - همگام‌سازی با سرور
- **`send_to_server(data)`** - ارسال داده به سرور
- **`test_connection()`** - تست اتصالات

#### استفاده:
```python
from services.device_service import DeviceService

device_service = DeviceService()
result = device_service.sync_device_data()
if result['success']:
    print("Sync successful")
```

## Controllers

### DeviceController (`controllers/device_controller.py`)

کنترلر API برای عملیات دستگاه.

#### Endpoints:
- `get_device_data()` - دریافت اطلاعات دستگاه
- `sync_device_data()` - همگام‌سازی داده
- `get_device_status()` - دریافت وضعیت دستگاه
- `test_connections()` - تست اتصالات

## API Endpoints

### REST API Server (`api_server.py`)

```bash
# شروع سرور API
python api_server.py
```

#### Endpoints:
- `GET /api/device/data` - دریافت اطلاعات دستگاه
- `POST /api/device/sync` - همگام‌سازی داده
- `GET /api/device/status` - دریافت وضعیت دستگاه
- `GET /api/device/health` - بررسی سلامت سیستم
- `POST /api/device/test` - تست اتصالات
- `GET /api/device/formatted` - دریافت داده فرمت شده

### Web Interface (`web_interface.py`)

```bash
# شروع رابط وب
python web_interface.py
```

#### Routes:
- `GET /` - داشبورد اصلی
- `GET /sync` - همگام‌سازی دستی
- `GET /status` - بروزرسانی وضعیت
- `GET /test` - تست اتصال

## Scheduled Tasks

### Command Line Tool (`sync_command.py`)

اسکریپت خط فرمان برای همگام‌سازی زمان‌بندی شده:

```bash
# همگام‌سازی یکباره
python sync_command.py sync

# تست اتصالات
python sync_command.py test

# دریافت وضعیت
python sync_command.py status

# همگام‌سازی مداوم
python sync_command.py continuous
```

## Data Structure

### فرمت داده ارسالی به سرور:
```json
{
    "device_info": {
        "name": "ZKTeco Device",
        "serial_number": "123456789",
        "firmware_version": "Ver 6.60",
        "ip_address": "192.168.70.141",
        "port": 4370,
        "device_time": "2024-01-15 10:30:00",
        "connection_status": "connected"
    },
    "users_summary": {
        "total_users": 50,
        "users_list": [
            {
                "user_id": "1",
                "name": "احمد محمدی",
                "card": "12345",
                "privilege": 0
            }
        ]
    },
    "attendance_summary": {
        "total_records": 1250,
        "recent_records": [
            {
                "user_id": "1",
                "timestamp": "2024-01-15 08:00:00",
                "status": 0,
                "punch": 0
            }
        ]
    },
    "sync_metadata": {
        "sync_timestamp": "2024-01-15T10:30:00",
        "sync_status": "success",
        "source_device": "192.168.70.141"
    }
}
```

## How to Run

### 1. Manual Sync via Web Interface
1. اجرای رابط وب: `python web_interface.py`
2. مراجعه به `http://localhost:8080`
3. کلیک روی دکمه "همگام‌سازی"

### 2. Manual Sync via API
```bash
curl -X POST http://localhost:5000/api/device/sync \
  -H "Content-Type: application/json"
```

### 3. Manual Sync via Command Line
```bash
python sync_command.py sync
```

### 4. Automatic Scheduled Sync
```bash
# همگام‌سازی مداوم
python sync_command.py continuous

# یا با cron (Linux/Mac)
# */30 * * * * cd /path/to/project && python sync_command.py sync
```

## Error Handling

### مشکلات رایج و راه‌حل‌ها

1. **خطا در اتصال به دستگاه**
   - بررسی آدرس IP دستگاه در تنظیمات
   - بررسی اتصال شبکه
   - بررسی اعتبارنامه‌های دستگاه

2. **خطا در احراز هویت**
   - بررسی نام کاربری/رمز عبور در تنظیمات
   - بررسی مدیریت نشست دستگاه

3. **خطا در اتصال به سرور هدف**
   - بررسی URL سرور
   - بررسی توکن احراز هویت
   - بررسی گواهینامه‌های SSL

### Logging

سیستم لاگ‌ها را در فایل `device_sync.log` ذخیره می‌کند:
```bash
tail -f device_sync.log
```

## Security Considerations

1. **احراز هویت**: استفاده از Bearer token برای احراز هویت API
2. **SSL**: غیرفعال کردن تأیید SSL برای دستگاه‌های داخلی (در صورت نیاز تنظیم کنید)
3. **مدیریت نشست**: مدیریت صحیح نشست با دستگاه‌های حضور و غیاب
4. **مدیریت خطا**: مدیریت جامع خطا و لاگینگ

## Troubleshooting

### Debug Mode
فعال کردن لاگینگ debug در `config.py`:
```python
LOG_LEVEL = 'DEBUG'
```

### Test Connection
تست اتصال دستگاه:
```bash
python sync_command.py test
```

## Performance Optimization

1. **پردازش دسته‌ای**: داده‌ها به صورت دسته‌ای پردازش می‌شوند
2. **کش**: مدیریت نشست برای اتصالات دستگاه
3. **زمان‌بندی**: وظایف زمان‌بندی شده بدون همپوشانی
4. **بازیابی خطا**: مکانیزم‌های retry خودکار

## Monitoring

### Health Check Endpoints
- `GET /api/device/health` - بررسی سلامت سیستم
- `GET /api/device/status` - بررسی وضعیت دستگاه

### Metrics to Monitor
- نرخ موفقیت همگام‌سازی
- حجم داده پردازش شده
- فراوانی خطا
- زمان پاسخ

## Future Enhancements

1. **همگام‌سازی Real-time**: بروزرسانی‌های real-time با WebSocket
2. **چندین دستگاه**: پشتیبانی از چندین دستگاه حضور و غیاب
3. **فیلترینگ پیشرفته**: گزینه‌های فیلترینگ دقیق‌تر داده
4. **گزارش‌گیری**: گزارش‌گیری و تحلیل پیشرفته
5. **اپلیکیشن موبایل**: رابط موبایل برای مدیریت حضور و غیاب

## Examples

### دریافت اطلاعات دستگاه
```python
from services.device_service import DeviceService

service = DeviceService()
data = service.get_device_data()
print(f"Device: {data['device_status']['device_info']['device_name']}")
```

### همگام‌سازی با سرور
```python
from services.device_service import DeviceService

service = DeviceService()
result = service.sync_device_data()
if result['success']:
    print("Sync successful!")
else:
    print(f"Sync failed: {result['message']}")
```

### استفاده از API
```python
import requests

# دریافت اطلاعات دستگاه
response = requests.get('http://localhost:5000/api/device/data')
data = response.json()

# همگام‌سازی
response = requests.post('http://localhost:5000/api/device/sync')
result = response.json()
``` #   z k t i m e _ a p p  
 #   z k t i m e _ a p p  
 