#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Web Interface for ZKTeco Device Information System
Provides a web-based interface for device management
"""

from flask import Flask, render_template_string, request, jsonify, redirect, url_for
import logging
from datetime import datetime
import threading
import os
import sys
import time

# Try to import System Tray dependencies
try:
    import pystray
    from pystray import MenuItem as item
    from PIL import Image, ImageDraw
    TRAY_AVAILABLE = True
except ImportError as e:
    print(f"System Tray not available: {e}")
    TRAY_AVAILABLE = False

try:
    import win32com.client
    WIN32_AVAILABLE = True
except ImportError:
    WIN32_AVAILABLE = False

try:
    import win10toast
    TOAST_AVAILABLE = True
except ImportError:
    TOAST_AVAILABLE = False

from controllers.device_controller import DeviceController
from config import Config

# Configure logging
logging.basicConfig(
    level=getattr(logging, Config.LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(Config.LOG_FILE),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)

# Initialize controller
device_controller = DeviceController()

# Global variable for tray icon
tray_icon = None

def create_image():
    """Create a simple icon for System Tray"""
    try:
        # Generate a simple icon (blue circle)
        image = Image.new('RGB', (64, 64), color=(255, 255, 255))
        d = ImageDraw.Draw(image)
        d.ellipse((8, 8, 56, 56), fill=(52, 152, 219))
        return image
    except Exception as e:
        logger.error(f"Error creating tray icon: {e}")
        return None

# Windows Startup shortcut management
def get_startup_shortcut_path():
    """Get the path for startup shortcut"""
    if not WIN32_AVAILABLE:
        return None, None
    
    try:
        startup_dir = os.path.join(os.environ['APPDATA'], r'Microsoft\Windows\Start Menu\Programs\Startup')
        exe_path = sys.executable if getattr(sys, 'frozen', False) else sys.argv[0]
        shortcut_path = os.path.join(startup_dir, 'ZKTecoWebInterface.lnk')
        return shortcut_path, exe_path
    except Exception as e:
        logger.error(f"Error getting startup path: {e}")
        return None, None

def add_to_startup():
    """Add application to Windows startup"""
    if not WIN32_AVAILABLE:
        logger.warning("win32com not available, cannot add to startup")
        return False
    
    try:
        shortcut_path, exe_path = get_startup_shortcut_path()
        if not shortcut_path or not exe_path:
            return False
            
        shell = win32com.client.Dispatch('WScript.Shell')
        shortcut = shell.CreateShortCut(shortcut_path)
        shortcut.Targetpath = exe_path
        shortcut.WorkingDirectory = os.path.dirname(exe_path)
        shortcut.save()
        logger.info("Added to startup successfully")
        return True
    except Exception as e:
        logger.error(f"Error adding to startup: {e}")
        return False

def remove_from_startup():
    """Remove application from Windows startup"""
    try:
        shortcut_path, _ = get_startup_shortcut_path()
        if shortcut_path and os.path.exists(shortcut_path):
            os.remove(shortcut_path)
            logger.info("Removed from startup successfully")
            return True
        return False
    except Exception as e:
        logger.error(f"Error removing from startup: {e}")
        return False

def is_in_startup():
    """Check if application is in Windows startup"""
    try:
        shortcut_path, _ = get_startup_shortcut_path()
        return shortcut_path and os.path.exists(shortcut_path)
    except Exception as e:
        logger.error(f"Error checking startup status: {e}")
        return False

# System Tray logic
def tray_thread():
    """Run System Tray in separate thread"""
    global tray_icon
    
    if not TRAY_AVAILABLE:
        logger.warning("System Tray not available")
        return
    
    try:
        def on_exit(icon, item):
            logger.info("Exiting application...")
            icon.stop()
            os._exit(0)

        def on_toggle_autostart(icon, item):
            try:
                if is_in_startup():
                    remove_from_startup()
                else:
                    add_to_startup()
                # Update menu text
                icon.update_menu()
            except Exception as e:
                logger.error(f"Error toggling autostart: {e}")

        def get_autostart_text():
            return 'حذف اجرای خودکار' if is_in_startup() else 'فعال‌سازی اجرای خودکار'

        def on_show_status(icon, item):
            try:
                if TOAST_AVAILABLE:
                    toaster = win10toast.ToastNotifier()
                    toaster.show_toast('وضعیت برنامه', 'برنامه در حال اجراست.', duration=3)
                else:
                    logger.info("Application is running - Web interface available at http://localhost:8080")
            except Exception as e:
                logger.error(f"Error showing status: {e}")

        def on_open_web(icon, item):
            try:
                import webbrowser
                webbrowser.open('http://localhost:8080')
            except Exception as e:
                logger.error(f"Error opening web interface: {e}")

        # Create menu
        menu = pystray.Menu(
            item('باز کردن رابط وب', on_open_web),
            item('نمایش وضعیت', on_show_status),
            pystray.Menu.SEPARATOR,
            item(lambda: get_autostart_text(), on_toggle_autostart),
            pystray.Menu.SEPARATOR,
            item('خروج', on_exit)
        )

        # Create icon
        icon_image = create_image()
        if not icon_image:
            logger.error("Could not create tray icon image")
            return

        tray_icon = pystray.Icon(
            'ZKTecoWebInterface',
            icon_image,
            'ZKTeco Web Interface\nhttp://localhost:8080',
            menu
        )
        
        logger.info("Starting System Tray...")
        tray_icon.run()
        
    except Exception as e:
        logger.error(f"Error in tray thread: {e}")

# HTML Template
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>سیستم اطلاعات دستگاه ZKTeco</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Tahoma', Arial, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 15px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
            overflow: hidden;
        }
        
        .header {
            background: linear-gradient(135deg, #2c3e50 0%, #34495e 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }
        
        .header h1 {
            font-size: 2.5em;
            margin-bottom: 10px;
        }
        
        .header p {
            font-size: 1.1em;
            opacity: 0.9;
        }
        
        .content {
            padding: 30px;
        }
        
        .dashboard {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }
        
        .card {
            background: #f8f9fa;
            border-radius: 10px;
            padding: 25px;
            border-left: 5px solid #3498db;
            transition: transform 0.3s ease;
        }
        
        .card:hover {
            transform: translateY(-5px);
        }
        
        .card h3 {
            color: #2c3e50;
            margin-bottom: 15px;
            font-size: 1.3em;
        }
        
        .status-indicator {
            display: inline-block;
            width: 12px;
            height: 12px;
            border-radius: 50%;
            margin-left: 10px;
        }
        
        .status-online {
            background: #27ae60;
        }
        
        .status-offline {
            background: #e74c3c;
        }
        
        .btn {
            background: linear-gradient(135deg, #3498db 0%, #2980b9 100%);
            color: white;
            border: none;
            padding: 12px 25px;
            border-radius: 25px;
            cursor: pointer;
            font-size: 1em;
            transition: all 0.3s ease;
            text-decoration: none;
            display: inline-block;
            margin: 5px;
        }
        
        .btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(52, 152, 219, 0.4);
        }
        
        .btn-success {
            background: linear-gradient(135deg, #27ae60 0%, #229954 100%);
        }
        
        .btn-warning {
            background: linear-gradient(135deg, #f39c12 0%, #e67e22 100%);
        }
        
        .btn-danger {
            background: linear-gradient(135deg, #e74c3c 0%, #c0392b 100%);
        }
        
        .info-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin-top: 15px;
        }
        
        .info-item {
            background: white;
            padding: 15px;
            border-radius: 8px;
            border: 1px solid #e9ecef;
        }
        
        .info-label {
            font-weight: bold;
            color: #6c757d;
            font-size: 0.9em;
        }
        
        .info-value {
            color: #2c3e50;
            font-size: 1.1em;
            margin-top: 5px;
        }
        
        .alert {
            padding: 15px;
            border-radius: 8px;
            margin: 20px 0;
        }
        
        .alert-success {
            background: #d4edda;
            color: #155724;
            border: 1px solid #c3e6cb;
        }
        
        .alert-error {
            background: #f8d7da;
            color: #721c24;
            border: 1px solid #f5c6cb;
        }
        
        .loading {
            display: none;
            text-align: center;
            padding: 20px;
        }
        
        .spinner {
            border: 4px solid #f3f3f3;
            border-top: 4px solid #3498db;
            border-radius: 50%;
            width: 40px;
            height: 40px;
            animation: spin 1s linear infinite;
            margin: 0 auto 10px;
        }
        
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        
        .footer {
            background: #f8f9fa;
            padding: 20px;
            text-align: center;
            color: #6c757d;
            border-top: 1px solid #e9ecef;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>سیستم اطلاعات دستگاه ZKTeco</h1>
            <p>مدیریت و همگام‌سازی اطلاعات دستگاه حضور و غیاب</p>
        </div>
        
        <div class="content">
            {% if message %}
            <div class="alert alert-{{ message_type }}">
                {{ message }}
            </div>
            {% endif %}
            
            <div class="dashboard">
                <div class="card">
                    <h3>وضعیت دستگاه <span class="status-indicator status-{{ 'online' if device_status else 'offline' }}"></span></h3>
                    <div class="info-grid">
                        <div class="info-item">
                            <div class="info-label">نام دستگاه</div>
                            <div class="info-value">{{ device_info.get('device_name', 'نامشخص') }}</div>
                        </div>
                        <div class="info-item">
                            <div class="info-label">شماره سریال</div>
                            <div class="info-value">{{ device_info.get('serial_number', 'نامشخص') }}</div>
                        </div>
                        <div class="info-item">
                            <div class="info-label">تعداد کاربران</div>
                            <div class="info-value">{{ device_info.get('users_count', 0) }}</div>
                        </div>
                        <div class="info-item">
                            <div class="info-label">رکوردهای حضور</div>
                            <div class="info-value">{{ device_info.get('attendance_count', 0) }}</div>
                        </div>
                    </div>
                </div>
                
                <div class="card">
                    <h3>عملیات</h3>
                    <div style="text-align: center;">
                        <a href="/sync" class="btn btn-success" onclick="showLoading()">همگام‌سازی</a>
                        <a href="/status" class="btn btn-warning">بروزرسانی وضعیت</a>
                        <a href="/test" class="btn btn-danger">تست اتصال</a>
                    </div>
                    <div class="loading" id="loading">
                        <div class="spinner"></div>
                        <p>در حال پردازش...</p>
                    </div>
                </div>
                
                <div class="card">
                    <h3>اطلاعات سیستم</h3>
                    <div class="info-grid">
                        <div class="info-item">
                            <div class="info-label">آخرین همگام‌سازی</div>
                            <div class="info-value">{{ last_sync or 'هیچ' }}</div>
                        </div>
                        <div class="info-item">
                            <div class="info-label">وضعیت سرور</div>
                            <div class="info-value">{{ 'متصل' if server_status else 'قطع' }}</div>
                        </div>
                        <div class="info-item">
                            <div class="info-label">فاصله همگام‌سازی</div>
                            <div class="info-value">{{ sync_interval }} ثانیه</div>
                        </div>
                    </div>
                </div>
            </div>
            
            <div class="card">
                <h3>لاگ‌های اخیر</h3>
                <div style="max-height: 300px; overflow-y: auto; background: #f8f9fa; padding: 15px; border-radius: 8px;">
                    {% for log in recent_logs %}
                    <div style="margin-bottom: 10px; padding: 10px; background: white; border-radius: 5px; border-left: 3px solid #3498db;">
                        <strong>{{ log.timestamp }}</strong><br>
                        {{ log.message }}
                    </div>
                    {% endfor %}
                </div>
            </div>
        </div>
        
        <div class="footer">
            <p>سیستم اطلاعات دستگاه ZKTeco - نسخه 1.0.0</p>
            <p>آخرین بروزرسانی: {{ current_time }}</p>
        </div>
    </div>
    
    <script>
        function showLoading() {
            document.getElementById('loading').style.display = 'block';
        }
        
        // Auto-refresh status every 30 seconds
        setInterval(function() {
            fetch('/status')
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        location.reload();
                    }
                });
        }, 30000);
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    """Main dashboard page"""
    try:
        # Get device status
        status_result = device_controller.get_device_status()
        device_status = status_result['success']
        device_info = status_result.get('data', {})
        
        # Get health status
        health_result = device_controller.get_health_status()
        server_status = health_result.get('data', {}).get('server_connection', False)
        
        # Get configuration
        sync_config = Config.get_sync_config()
        
        return render_template_string(HTML_TEMPLATE,
            device_status=device_status,
            device_info=device_info.get('device_info', {}),
            server_status=server_status,
            last_sync=device_info.get('last_sync', ''),
            sync_interval=sync_config['interval'],
            current_time=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            recent_logs=[],  # You can implement log retrieval here
            message=request.args.get('message', ''),
            message_type=request.args.get('type', 'success')
        )
        
    except Exception as e:
        logger.error(f"Error in dashboard: {e}")
        return render_template_string(HTML_TEMPLATE,
            device_status=False,
            device_info={},
            server_status=False,
            last_sync='',
            sync_interval=3600,
            current_time=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            recent_logs=[],
            message=f'خطا در بارگذاری: {str(e)}',
            message_type='error'
        )

@app.route('/sync')
def sync():
    """Sync device data"""
    try:
        result = device_controller.sync_device_data()
        
        if result['success']:
            message = f"همگام‌سازی موفق: {result['message']}"
            message_type = 'success'
        else:
            message = f"خطا در همگام‌سازی: {result['message']}"
            message_type = 'error'
            
        return redirect(f'/?message={message}&type={message_type}')
        
    except Exception as e:
        logger.error(f"Error in sync: {e}")
        return redirect(f'/?message=خطای سرور: {str(e)}&type=error')

@app.route('/status')
def status():
    """Get device status"""
    try:
        result = device_controller.get_device_status()
        return jsonify(result)
    except Exception as e:
        logger.error(f"Error in status: {e}")
        return jsonify({
            'success': False,
            'message': f'Error: {str(e)}'
        })

@app.route('/test')
def test():
    """Test connections"""
    try:
        result = device_controller.test_connections()
        
        if result['success']:
            message = "تست اتصال موفق"
            message_type = 'success'
        else:
            message = "خطا در تست اتصال"
            message_type = 'error'
            
        return redirect(f'/?message={message}&type={message_type}')
        
    except Exception as e:
        logger.error(f"Error in test: {e}")
        return redirect(f'/?message=خطای سرور: {str(e)}&type=error')

if __name__ == '__main__':
    try:
        logger.info("Starting ZKTeco Device Information Web Interface")
        
        # Start tray icon in a separate thread
        if TRAY_AVAILABLE:
            tray = threading.Thread(target=tray_thread, daemon=True)
            tray.start()
            # Give tray a moment to initialize
            time.sleep(1)
            logger.info("System Tray started successfully")
        else:
            logger.warning("System Tray not available - running in console mode only")
        
        # Start Flask app
        logger.info("Starting web server on http://localhost:8080")
        app.run(
            host='0.0.0.0',
            port=8080,
            debug=False
        )
        
    except KeyboardInterrupt:
        logger.info("Application interrupted by user")
        if tray_icon:
            tray_icon.stop()
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        if tray_icon:
            tray_icon.stop()
        sys.exit(1) 