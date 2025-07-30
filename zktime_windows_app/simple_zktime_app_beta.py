#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Simple ZKTeco Device Sync Application (BETA SERVER VERSION)
No web interface, just system tray and sync functionality
Uses BETA server for testing: https://beta.sdadparts.com/api/attendance/device-import
"""

import sys
import os
import logging
import threading
import time
import json
import requests
from datetime import datetime, timedelta
from typing import Dict, Any, List
import tkinter as tk
from tkinter import messagebox
import pystray
from PIL import Image, ImageDraw
import winreg
import schedule
from zk import ZK

# Import zk_device_info from local directory
from zk_device_info import connect_to_device

class SimpleZKTimeAppBeta:
    """Simple ZKTeco sync application with BETA server for testing"""
    
    def __init__(self):
        """Initialize the application"""
        # Configuration
        self.DEVICE_IP = '192.168.70.141'
        self.DEVICE_PORT = 4370
        self.DEVICE_TIMEOUT = 5
        self.SERVER_URL = 'https://beta.sdadparts.com/api/attendance/device-import'  # BETA SERVER
        self.SERVER_TOKEN = '3|4GQYfJgpAhjlZfumsMMBrKvZyr68L9hVA3V9u5Fnd983ce66'
        self.SYNC_INTERVAL = 300  # 5 minutes for testing
        
        # Application state
        self.sync_running = False
        self.sync_thread = None
        self.icon = None
        
        # Setup logging
        self.setup_logging()
        
        # Create system tray
        self.create_system_tray()
        
    def setup_logging(self):
        """Setup simple logging"""
        log_file = 'zktime_beta_test.log'
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file, encoding='utf-8'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
        self.logger.info("Simple ZKTime App BETA started")
        self.logger.info(f"Using BETA server: {self.SERVER_URL}")
        
    def create_icon_image(self):
        """Create a simple beta icon (orange instead of blue)"""
        image = Image.new('RGBA', (64, 64), (0, 0, 0, 0))
        draw = ImageDraw.Draw(image)
        # Orange circle for beta
        draw.ellipse([8, 8, 56, 56], fill=(255, 140, 0, 255))
        # White "B" for Beta
        draw.text((22, 20), "B", fill=(255, 255, 255, 255))
        return image
        
    def create_system_tray(self):
        """Create system tray menu"""
        try:
            icon_image = self.create_icon_image()
            
            menu = pystray.Menu(
                pystray.MenuItem("Manual Sync (BETA)", self.manual_sync),
                pystray.MenuItem("Test User List", self.test_user_list),
                pystray.MenuItem("Device Status", self.show_device_status),
                pystray.MenuItem("Start Auto Sync", self.start_auto_sync),
                pystray.MenuItem("Stop Auto Sync", self.stop_auto_sync),
                pystray.MenuItem("Settings (BETA)", self.show_settings),
                pystray.MenuItem("View Log", self.view_log),
                pystray.MenuItem("Exit", self.exit_app)
            )
            
            self.icon = pystray.Icon("zktime_beta", icon_image, "ZKTime BETA Test", menu)
            self.logger.info("System tray created successfully (BETA version)")
            
        except Exception as e:
            self.logger.error(f"Failed to create system tray: {e}")
            
    def connect_to_device_local(self):
        """Connect to ZKTeco device using imported function"""
        try:
            conn = connect_to_device(self.DEVICE_IP, self.DEVICE_PORT, self.DEVICE_TIMEOUT)
            if conn:
                self.logger.info(f"Connected to device {self.DEVICE_IP}:{self.DEVICE_PORT}")
            return conn
        except Exception as e:
            self.logger.error(f"Device connection failed: {e}")
            return None
            
    def get_users_from_device(self, conn):
        """Get users from device using the recommended method"""
        try:
            users = conn.get_users()
            user_dict = {}
            for user in users:
                user_dict[user.user_id] = user.name
            self.logger.info(f"Retrieved {len(user_dict)} users from device:")
            for user_id, name in user_dict.items():
                self.logger.info(f"  - {user_id}: {name}")
            return user_dict
        except Exception as e:
            self.logger.error(f"Failed to get users: {e}")
            return {}
            
    def get_attendance_from_device(self, conn):
        """Get attendance records from device"""
        try:
            attendance = conn.get_attendance()
            records = []
            for record in attendance:
                records.append({
                    'user_id': record.user_id,
                    'timestamp': record.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
                    'status': 'Check In' if record.punch == 1 else 'Check Out'
                })
            self.logger.info(f"Retrieved {len(records)} attendance records")
            return records
        except Exception as e:
            self.logger.error(f"Failed to get attendance: {e}")
            return []
            
    def format_data_for_api(self, users_dict, attendance_records):
        """Format data for API"""
        try:
            # Group by date and user
            grouped_data = {}
            
            for record in attendance_records:
                timestamp = datetime.strptime(record['timestamp'], '%Y-%m-%d %H:%M:%S')
                date_str = timestamp.strftime('%Y-%m-%d')
                time_str = timestamp.strftime('%H:%M:%S')
                user_id = record['user_id']
                user_name = users_dict.get(user_id, f"User {user_id}")
                
                if date_str not in grouped_data:
                    grouped_data[date_str] = {}
                    
                if user_id not in grouped_data[date_str]:
                    grouped_data[date_str][user_id] = {
                        'date': date_str,
                        'id_number': user_id,
                        'name': user_name,
                        'times': [],
                        'card': '0'
                    }
                    
                grouped_data[date_str][user_id]['times'].append(time_str)
            
            # Convert to API format
            attendance_records_api = []
            for date_str in grouped_data:
                for user_id in grouped_data[date_str]:
                    user_data = grouped_data[date_str][user_id]
                    user_data['times'].sort()  # Sort times
                    attendance_records_api.append(user_data)
            
            # Get date range
            if attendance_records_api:
                dates = [record['date'] for record in attendance_records_api]
                start_date = min(dates)
                end_date = max(dates)
            else:
                today = datetime.now().strftime('%Y-%m-%d')
                start_date = today
                end_date = today
                
            api_data = {
                'period': {
                    'start_date': start_date,
                    'end_date': end_date
                },
                'attendance_records': attendance_records_api
            }
            
            self.logger.info(f"Formatted {len(attendance_records_api)} records for BETA API")
            self.logger.info(f"Sample formatted data: {json.dumps(api_data, indent=2, ensure_ascii=False)[:500]}...")
            return api_data
            
        except Exception as e:
            self.logger.error(f"Failed to format data: {e}")
            return None
            
    def send_to_server(self, data):
        """Send data to BETA server"""
        try:
            headers = {
                'Content-Type': 'application/json',
                'Accept': 'application/json',
                'Authorization': f'Bearer {self.SERVER_TOKEN}'
            }
            
            self.logger.info(f"Sending data to BETA server: {self.SERVER_URL}")
            self.logger.info(f"Data size: {len(json.dumps(data))} characters")
            
            response = requests.post(
                self.SERVER_URL,
                json=data,
                headers=headers,
                timeout=30
            )
            
            self.logger.info(f"Server response status: {response.status_code}")
            self.logger.info(f"Server response: {response.text}")
            
            if response.status_code == 200:
                self.logger.info("Data sent to BETA server successfully")
                return True
            else:
                self.logger.error(f"BETA server returned status {response.status_code}: {response.text}")
                return False
                
        except Exception as e:
            self.logger.error(f"Failed to send data to BETA server: {e}")
            return False
            
    def perform_sync(self):
        """Perform complete sync process with BETA server"""
        try:
            self.logger.info("Starting BETA sync process")
            
            # Connect to device
            conn = self.connect_to_device_local()
            if not conn:
                return False
                
            # Get users and attendance
            users_dict = self.get_users_from_device(conn)
            attendance_records = self.get_attendance_from_device(conn)
            
            # Disconnect from device
            conn.disconnect()
            
            if not attendance_records:
                self.logger.info("No attendance records found")
                return True
                
            # Format data
            api_data = self.format_data_for_api(users_dict, attendance_records)
            if not api_data:
                return False
                
            # Send to BETA server
            success = self.send_to_server(api_data)
            
            if success:
                self.logger.info(f"BETA sync completed successfully. Sent {len(api_data['attendance_records'])} records")
            else:
                self.logger.error("BETA sync failed")
                
            return success
            
        except Exception as e:
            self.logger.error(f"BETA sync process failed: {e}")
            return False
            
    def test_user_list(self, icon=None, item=None):
        """Test user list functionality"""
        try:
            self.logger.info("Testing user list functionality")
            
            conn = self.connect_to_device_local()
            if conn:
                users = conn.get_users()
                conn.disconnect()
                
                # Show users in messagebox
                user_text = f"کاربران دستگاه ({len(users)} کاربر):\n\n"
                for i, user in enumerate(users[:10], 1):  # Show first 10 users
                    user_text += f"{i}. {user.name} (کد: {user.user_id})\n"
                
                if len(users) > 10:
                    user_text += f"\n... و {len(users) - 10} کاربر دیگر"
                
                messagebox.showinfo("لیست کاربران", user_text)
                self.logger.info(f"Displayed {len(users)} users to user")
            else:
                messagebox.showerror("خطا", "اتصال به دستگاه برقرار نشد")
                
        except Exception as e:
            self.logger.error(f"Failed to test user list: {e}")
            messagebox.showerror("خطا", f"خطا در دریافت لیست کاربران: {e}")
            
    def manual_sync(self, icon=None, item=None):
        """Perform manual sync with BETA server"""
        try:
            self.logger.info("Manual BETA sync requested")
            
            # Run in background thread
            def sync_worker():
                success = self.perform_sync()
                if success:
                    messagebox.showinfo("Sync", "Manual BETA sync completed successfully!")
                else:
                    messagebox.showerror("Sync", "Manual BETA sync failed. Check log for details.")
                    
            thread = threading.Thread(target=sync_worker)
            thread.daemon = True
            thread.start()
            
        except Exception as e:
            self.logger.error(f"Manual BETA sync failed: {e}")
            messagebox.showerror("Error", f"Manual BETA sync failed: {e}")
            
    def show_device_status(self, icon=None, item=None):
        """Show device status"""
        try:
            conn = self.connect_to_device_local()
            if conn:
                users = conn.get_users()
                attendance = conn.get_attendance()
                conn.disconnect()
                
                status_text = f"Device Status (BETA):\n\n"
                status_text += f"IP: {self.DEVICE_IP}:{self.DEVICE_PORT}\n"
                status_text += f"Connection: ✓ Connected\n"
                status_text += f"Users: {len(users)}\n"
                status_text += f"Attendance Records: {len(attendance)}\n"
                status_text += f"Server: BETA ({self.SERVER_URL})"
                
                messagebox.showinfo("Device Status", status_text)
            else:
                messagebox.showerror("Device Status", "Failed to connect to device")
                
        except Exception as e:
            self.logger.error(f"Failed to get device status: {e}")
            messagebox.showerror("Error", f"Failed to get device status: {e}")
            
    def start_auto_sync(self, icon=None, item=None):
        """Start automatic sync with BETA server"""
        try:
            if self.sync_running:
                messagebox.showinfo("Auto Sync", "BETA auto sync is already running")
                return
                
            self.sync_running = True
            
            def sync_scheduler():
                schedule.every(self.SYNC_INTERVAL).seconds.do(self.perform_sync)
                while self.sync_running:
                    schedule.run_pending()
                    time.sleep(1)
                    
            self.sync_thread = threading.Thread(target=sync_scheduler)
            self.sync_thread.daemon = True
            self.sync_thread.start()
            
            self.logger.info(f"BETA auto sync started (interval: {self.SYNC_INTERVAL} seconds)")
            messagebox.showinfo("Auto Sync", f"BETA auto sync started (every {self.SYNC_INTERVAL//60} minutes)")
            
        except Exception as e:
            self.logger.error(f"Failed to start BETA auto sync: {e}")
            messagebox.showerror("Error", f"Failed to start BETA auto sync: {e}")
            
    def stop_auto_sync(self, icon=None, item=None):
        """Stop automatic sync"""
        try:
            self.sync_running = False
            schedule.clear()
            self.logger.info("BETA auto sync stopped")
            messagebox.showinfo("Auto Sync", "BETA auto sync stopped")
            
        except Exception as e:
            self.logger.error(f"Failed to stop BETA auto sync: {e}")
            messagebox.showerror("Error", f"Failed to stop BETA auto sync: {e}")
            
    def show_settings(self, icon=None, item=None):
        """Show settings"""
        try:
            root = tk.Tk()
            root.title("ZKTime BETA - Settings")
            root.geometry("450x350")
            root.resizable(False, False)
            
            tk.Label(root, text="Device Settings", font=("Arial", 12, "bold")).pack(pady=10)
            tk.Label(root, text=f"Device IP: {self.DEVICE_IP}").pack()
            tk.Label(root, text=f"Device Port: {self.DEVICE_PORT}").pack()
            tk.Label(root, text=f"Sync Interval: {self.SYNC_INTERVAL} seconds").pack()
            
            tk.Label(root, text="\nServer Settings (BETA)", font=("Arial", 12, "bold"), fg="orange").pack(pady=10)
            tk.Label(root, text=f"Server URL: {self.SERVER_URL}", fg="orange").pack()
            tk.Label(root, text="⚠️ This is BETA server for testing!", fg="red").pack()
            
            tk.Label(root, text="\nSync Status", font=("Arial", 12, "bold")).pack(pady=10)
            status = "Running" if self.sync_running else "Stopped"
            tk.Label(root, text=f"Auto Sync: {status}").pack()
            
            tk.Button(root, text="Close", command=root.destroy).pack(pady=20)
            root.mainloop()
            
        except Exception as e:
            self.logger.error(f"Failed to show settings: {e}")
            messagebox.showerror("Error", f"Failed to show settings: {e}")
            
    def view_log(self, icon=None, item=None):
        """View log file"""
        try:
            log_file = 'zktime_beta_test.log'
            if os.path.exists(log_file):
                os.startfile(log_file)
            else:
                messagebox.showinfo("Log", "Log file not found")
        except Exception as e:
            self.logger.error(f"Failed to open log file: {e}")
            messagebox.showerror("Error", f"Failed to open log file: {e}")
            
    def exit_app(self, icon=None, item=None):
        """Exit application"""
        try:
            self.logger.info("BETA application exiting")
            self.sync_running = False
            if self.icon:
                self.icon.stop()
            sys.exit(0)
        except Exception as e:
            self.logger.error(f"Error during exit: {e}")
            sys.exit(1)
            
    def run(self):
        """Run the application"""
        try:
            self.logger.info("Starting Simple ZKTime BETA App")
            
            # Run system tray
            if self.icon:
                self.icon.run()
            else:
                self.logger.error("System tray not available")
                
        except Exception as e:
            self.logger.error(f"BETA application error: {e}")
            sys.exit(1)

def main():
    """Main entry point"""
    try:
        app = SimpleZKTimeAppBeta()
        app.run()
    except Exception as e:
        print(f"Failed to start BETA application: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()