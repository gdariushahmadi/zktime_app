#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Simple ZKTeco Device Sync Application
No web interface, just system tray and sync functionality
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

class SimpleZKTimeApp:
    """Simple ZKTeco sync application with only essential features"""
    
    def __init__(self):
        """Initialize the application"""
        # Configuration
        self.DEVICE_IP = '192.168.70.141'
        self.DEVICE_PORT = 4370
        self.DEVICE_TIMEOUT = 5
        self.SERVER_URL = 'https://panel.sdadparts.com/api/attendance/device-import'
        self.SERVER_TOKEN = '3|4GQYfJgpAhjlZfumsMMBrKvZyr68L9hVA3V9u5Fnd983ce66'
        self.SYNC_INTERVAL = 3600  # 1 hour
        
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
        log_file = 'zktime_simple.log'
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file, encoding='utf-8'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
        self.logger.info("Simple ZKTime App started")
        
    def create_icon_image(self):
        """Create a simple blue icon"""
        image = Image.new('RGBA', (64, 64), (0, 0, 0, 0))
        draw = ImageDraw.Draw(image)
        # Blue circle
        draw.ellipse([8, 8, 56, 56], fill=(0, 120, 255, 255))
        # White "Z"
        draw.text((24, 20), "Z", fill=(255, 255, 255, 255))
        return image
        
    def create_system_tray(self):
        """Create system tray menu"""
        try:
            icon_image = self.create_icon_image()
            
            menu = pystray.Menu(
                pystray.MenuItem("Manual Sync", self.manual_sync),
                pystray.MenuItem("Device Status", self.show_device_status),
                pystray.MenuItem("Start Auto Sync", self.start_auto_sync),
                pystray.MenuItem("Stop Auto Sync", self.stop_auto_sync),
                pystray.MenuItem("Settings", self.show_settings),
                pystray.MenuItem("View Log", self.view_log),
                pystray.MenuItem("Exit", self.exit_app)
            )
            
            self.icon = pystray.Icon("zktime_simple", icon_image, "ZKTime Simple Sync", menu)
            self.logger.info("System tray created successfully")
            
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
        """Get users from device"""
        try:
            users = conn.get_users()
            user_dict = {}
            for user in users:
                user_dict[user.user_id] = user.name
            self.logger.info(f"Retrieved {len(user_dict)} users from device")
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
            
            self.logger.info(f"Formatted {len(attendance_records_api)} records for API")
            return api_data
            
        except Exception as e:
            self.logger.error(f"Failed to format data: {e}")
            return None
            
    def send_to_server(self, data):
        """Send data to server"""
        try:
            headers = {
                'Content-Type': 'application/json',
                'Accept': 'application/json',
                'Authorization': f'Bearer {self.SERVER_TOKEN}'
            }
            
            response = requests.post(
                self.SERVER_URL,
                json=data,
                headers=headers,
                timeout=30
            )
            
            if response.status_code == 200:
                self.logger.info("Data sent to server successfully")
                return True
            else:
                self.logger.error(f"Server returned status {response.status_code}: {response.text}")
                return False
                
        except Exception as e:
            self.logger.error(f"Failed to send data to server: {e}")
            return False
            
    def perform_sync(self):
        """Perform complete sync process"""
        try:
            self.logger.info("Starting sync process")
            
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
                
            # Send to server
            success = self.send_to_server(api_data)
            
            if success:
                self.logger.info(f"Sync completed successfully. Sent {len(api_data['attendance_records'])} records")
            else:
                self.logger.error("Sync failed")
                
            return success
            
        except Exception as e:
            self.logger.error(f"Sync process failed: {e}")
            return False
            
    def manual_sync(self, icon=None, item=None):
        """Perform manual sync"""
        try:
            self.logger.info("Manual sync requested")
            
            # Run in background thread
            def sync_worker():
                success = self.perform_sync()
                if success:
                    messagebox.showinfo("Sync", "Manual sync completed successfully!")
                else:
                    messagebox.showerror("Sync", "Manual sync failed. Check log for details.")
                    
            thread = threading.Thread(target=sync_worker)
            thread.daemon = True
            thread.start()
            
        except Exception as e:
            self.logger.error(f"Manual sync failed: {e}")
            messagebox.showerror("Error", f"Manual sync failed: {e}")
            
    def show_device_status(self, icon=None, item=None):
        """Show device status"""
        try:
            conn = self.connect_to_device_local()
            if conn:
                users = conn.get_users()
                attendance = conn.get_attendance()
                conn.disconnect()
                
                status_text = f"Device Status:\n\n"
                status_text += f"IP: {self.DEVICE_IP}:{self.DEVICE_PORT}\n"
                status_text += f"Connection: ✓ Connected\n"
                status_text += f"Users: {len(users)}\n"
                status_text += f"Attendance Records: {len(attendance)}"
                
                messagebox.showinfo("Device Status", status_text)
            else:
                messagebox.showerror("Device Status", "Failed to connect to device")
                
        except Exception as e:
            self.logger.error(f"Failed to get device status: {e}")
            messagebox.showerror("Error", f"Failed to get device status: {e}")
            
    def start_auto_sync(self, icon=None, item=None):
        """Start automatic sync"""
        try:
            if self.sync_running:
                messagebox.showinfo("Auto Sync", "Auto sync is already running")
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
            
            self.logger.info(f"Auto sync started (interval: {self.SYNC_INTERVAL} seconds)")
            messagebox.showinfo("Auto Sync", f"Auto sync started (every {self.SYNC_INTERVAL//60} minutes)")
            
        except Exception as e:
            self.logger.error(f"Failed to start auto sync: {e}")
            messagebox.showerror("Error", f"Failed to start auto sync: {e}")
            
    def stop_auto_sync(self, icon=None, item=None):
        """Stop automatic sync"""
        try:
            self.sync_running = False
            schedule.clear()
            self.logger.info("Auto sync stopped")
            messagebox.showinfo("Auto Sync", "Auto sync stopped")
            
        except Exception as e:
            self.logger.error(f"Failed to stop auto sync: {e}")
            messagebox.showerror("Error", f"Failed to stop auto sync: {e}")
            
    def show_settings(self, icon=None, item=None):
        """Show settings"""
        try:
            root = tk.Tk()
            root.title("ZKTime Simple - Settings")
            root.geometry("400x300")
            root.resizable(False, False)
            
            tk.Label(root, text="Device Settings", font=("Arial", 12, "bold")).pack(pady=10)
            tk.Label(root, text=f"Device IP: {self.DEVICE_IP}").pack()
            tk.Label(root, text=f"Device Port: {self.DEVICE_PORT}").pack()
            tk.Label(root, text=f"Sync Interval: {self.SYNC_INTERVAL} seconds").pack()
            
            tk.Label(root, text="\nServer Settings", font=("Arial", 12, "bold")).pack(pady=10)
            tk.Label(root, text=f"Server URL: {self.SERVER_URL}").pack()
            
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
            log_file = 'zktime_simple.log'
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
            self.logger.info("Application exiting")
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
            self.logger.info("Starting Simple ZKTime App")
            
            # Start auto sync by default
            self.start_auto_sync()
            
            # Run system tray
            if self.icon:
                self.icon.run()
            else:
                self.logger.error("System tray not available")
                
        except Exception as e:
            self.logger.error(f"Application error: {e}")
            sys.exit(1)

def main():
    """Main entry point"""
    try:
        app = SimpleZKTimeApp()
        app.run()
    except Exception as e:
        print(f"Failed to start application: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()