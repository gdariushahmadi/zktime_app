# ZKTeco Device Information System Documentation

## Overview
The ZKTeco Device Information System is designed to automatically sync device information from ZKTeco attendance devices to a central dashboard server. The system consists of multiple components that work together to fetch data from attendance devices, process it, and send it to a target server in a standardized format.

## System Architecture

### Components

1. **DeviceService** - Main service for handling device data operations
2. **ApiService** - Handles communication with ZKTeco devices
3. **DeviceController** - API controller for device operations
4. **Web Interface** - Web-based management interface
5. **Sync Command** - Command-line tool for scheduled sync

### Data Flow

```
ZKTeco Device → ApiService → DeviceService → Target Server
```

## Configuration

### Environment Variables

Add these to your `.env` file or set as environment variables:

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

### Configuration Files

#### `config.py`
```python
class Config:
    DEVICE_IP = os.getenv('DEVICE_IP', '192.168.70.141')
    DEVICE_PORT = int(os.getenv('DEVICE_PORT', '4370'))
    TARGET_SERVER_URL = os.getenv('TARGET_SERVER_URL', 'https://panel.sdadparts.com/api/device/import')
    TARGET_SERVER_TOKEN = os.getenv('TARGET_SERVER_TOKEN', 'your-token-here')
    SYNC_INTERVAL = int(os.getenv('SYNC_INTERVAL', '3600'))
```

## Core Services

### 1. ApiService (`services/api_service.py`)

Handles direct communication with ZKTeco devices.

#### Key Methods:

- **`connect()`** - Connects to the ZKTeco device
- **`get_device_info()`** - Retrieves basic device information
- **`get_users_info()`** - Gets user list from device
- **`get_attendance_info()`** - Gets attendance records
- **`get_device_status()`** - Gets comprehensive device status

#### Usage:
```python
from services.api_service import ApiService

api_service = ApiService('192.168.70.141', 4370, 5)
if api_service.connect():
    device_info = api_service.get_device_info()
    print(f"Device: {device_info['device_name']}")
```

### 2. DeviceService (`services/device_service.py`)

Main service for device data operations.

#### Key Methods:

- **`get_device_data()`** - Fetches comprehensive device data
- **`sync_device_data()`** - Syncs data to target server
- **`send_to_server(data)`** - Sends data to dashboard server
- **`test_connection()`** - Tests device and server connections

#### Usage:
```python
from services.device_service import DeviceService

device_service = DeviceService()
result = device_service.sync_device_data()
if result['success']:
    print("Sync successful!")
```

## Controllers

### DeviceController (`controllers/device_controller.py`)

API controller for device operations.

#### Methods:
- `get_device_data()` - Get device data via API
- `sync_device_data()` - Sync data via API
- `get_device_status()` - Get device status
- `test_connections()` - Test connections
- `get_health_status()` - Get system health

## API Endpoints

### REST API Server (`api_server.py`)

#### Routes:
- `GET /api/device/data` - Get device data
- `POST /api/device/sync` - Sync device data to server
- `GET /api/device/status` - Get device status
- `GET /api/device/health` - Get system health
- `POST /api/device/test` - Test connections
- `GET /api/device/formatted` - Get formatted data

### Web Interface (`web_interface.py`)

#### Routes:
- `GET /` - Main dashboard
- `GET /sync` - Manual sync trigger
- `GET /status` - Update status
- `GET /test` - Test connection

## Scheduled Tasks

### Command Line Tool (`sync_command.py`)

The system includes a command-line tool for scheduled sync:

#### Commands:
```bash
python sync_command.py sync      # One-time sync
python sync_command.py test      # Test connections
python sync_command.py status    # Get device status
python sync_command.py continuous # Continuous sync
```

#### Scheduling:
```bash
# Add to crontab for automatic scheduling
*/30 * * * * cd /path-to-your-project && python sync_command.py sync
```

## Data Structure

### Device Data Format Sent to Server
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
                "privilege": 0,
                "password": "",
                "group_id": "",
                "user_sns": "",
                "work_code": ""
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
1. Run web interface: `python web_interface.py`
2. Navigate to `http://localhost:8080`
3. Click "Sync" button

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
# Continuous sync
python sync_command.py continuous

# Or with cron
*/30 * * * * cd /path-to-your-project && python sync_command.py sync
```

## Error Handling

### Common Issues and Solutions

1. **Device Connection Failed**
   - Check device IP in configuration
   - Verify network connectivity
   - Check device credentials

2. **Authentication Failed**
   - Verify device connection parameters
   - Check device session management

3. **Target Server Connection Failed**
   - Verify server URL
   - Check authentication token
   - Verify SSL certificates

### Logging

The system logs errors to `device_sync.log`:
```bash
tail -f device_sync.log
```

## Security Considerations

1. **Authentication**: Uses Bearer token for API authentication
2. **SSL**: Disabled SSL verification for internal devices (configure as needed)
3. **Session Management**: Proper session handling with ZKTeco devices
4. **Error Handling**: Comprehensive error handling and logging

## Troubleshooting

### Debug Mode
Enable debug logging in `config.py`:
```python
LOG_LEVEL = 'DEBUG'
```

### Test Connection
Test device connectivity:
```bash
python sync_command.py test
```

## Performance Optimization

1. **Batch Processing**: Data is processed efficiently
2. **Caching**: Session management for device connections
3. **Scheduling**: Non-overlapping scheduled tasks
4. **Error Recovery**: Automatic retry mechanisms

## Monitoring

### Health Check Endpoints
- `GET /api/device/health` - Check system health
- `GET /api/device/status` - Check device status

### Metrics to Monitor
- Sync success rate
- Data volume processed
- Error frequency
- Response times

## Future Enhancements

1. **Real-time Sync**: WebSocket-based real-time updates
2. **Multiple Devices**: Support for multiple ZKTeco devices
3. **Advanced Filtering**: More granular data filtering options
4. **Reporting**: Enhanced reporting and analytics
5. **Mobile App**: Mobile interface for device management

## Installation Guide

### Prerequisites
- Python 3.6 or higher
- Required Python packages (see requirements.txt)

### Installation Steps

1. **Clone or download the project**
2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment**:
   ```bash
   cp env_example.txt .env
   # Edit .env file with your settings
   ```

4. **Test installation**:
   ```bash
   python sync_command.py test
   ```

### Quick Start

1. **Start web interface**:
   ```bash
   python web_interface.py
   ```

2. **Start API server**:
   ```bash
   python api_server.py
   ```

3. **Run manual sync**:
   ```bash
   python sync_command.py sync
   ```

## API Reference

### Authentication
All API endpoints use Bearer token authentication:
```
Authorization: Bearer your-token-here
```

### Response Format
All API responses follow this format:
```json
{
    "success": true,
    "message": "Operation completed successfully",
    "data": {...},
    "timestamp": "2024-01-15T10:30:00"
}
```

### Error Responses
```json
{
    "success": false,
    "message": "Error description",
    "timestamp": "2024-01-15T10:30:00"
}
```

## Examples

### Python Client Example
```python
import requests

# Get device data
response = requests.get('http://localhost:5000/api/device/data')
data = response.json()

# Sync device data
response = requests.post('http://localhost:5000/api/device/sync')
result = response.json()

# Test connections
response = requests.post('http://localhost:5000/api/device/test')
test_result = response.json()
```

### cURL Examples
```bash
# Get device data
curl -X GET http://localhost:5000/api/device/data

# Sync device data
curl -X POST http://localhost:5000/api/device/sync

# Test connections
curl -X POST http://localhost:5000/api/device/test
```

## Support

For issues and questions:
1. Check the logs in `device_sync.log`
2. Test connections using `python sync_command.py test`
3. Verify configuration in `.env` file
4. Check network connectivity to device and server 