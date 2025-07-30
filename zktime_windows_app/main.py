#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ZKTeco Device Sync Windows Application
Main application with system tray, auto-start, and sync features
"""

import sys
import os
import logging
import threading
import time
import json
import webbrowser
from datetime import datetime, timedelta
from typing import Dict, Any, Optional
import tkinter as tk
from tkinter import messagebox, simpledialog
import pystray
from PIL import Image, ImageDraw
import winreg
import schedule

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import Config
from services.device_service import DeviceService

class ZKTecoWindowsApp:
    """Main Windows application with system tray and sync functionality"""
    
    def __init__(self):
        """Initialize the application"""
        self.config = Config()
        self.device_service = None
        self.sync_thread = None
        self.sync_running = False
        self.icon = None
        self.setup_logging()
        self.setup_device_service()
        self.setup_system_tray()
        
    def setup_logging(self):
        """Setup logging configuration"""
        log_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'zktime_sync.log')
        logging.basicConfig(
            level=getattr(logging, self.config.LOG_LEVEL),
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file, encoding='utf-8'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
        self.logger.info("ZKTeco Windows Application started")
        
    def setup_device_service(self):
        """Initialize device service"""
        try:
            self.device_service = DeviceService()
            self.logger.info("Device service initialized successfully")
        except Exception as e:
            self.logger.error(f"Failed to initialize device service: {e}")
            
    def create_icon_image(self) -> Image.Image:
        """Create system tray icon"""
        # Create a simple blue icon
        width = 64
        height = 64
        image = Image.new('RGBA', (width, height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(image)
        
        # Draw a blue circle
        draw.ellipse([8, 8, width-8, height-8], fill=(0, 120, 255, 255))
        # Draw a white "Z" in the center
        draw.text((20, 15), "Z", fill=(255, 255, 255, 255), font=None)
        
        return image
        
    def setup_system_tray(self):
        """Setup system tray icon and menu"""
        try:
            icon_image = self.create_icon_image()
            
            menu = pystray.Menu(
                pystray.MenuItem("Open Web Interface", self.open_web_interface),
                pystray.MenuItem("Manual Sync", self.manual_sync),
                pystray.MenuItem("Device Status", self.show_device_status),
                pystray.MenuItem("Test Connection", self.test_connection),
                pystray.MenuItem("Settings", self.show_settings),
                pystray.MenuItem("Auto-start", self.toggle_auto_start),
                pystray.MenuItem("View Log", self.view_log),
                pystray.MenuItem("Exit", self.exit_app)
            )
            
            self.icon = pystray.Icon("zktime_sync", icon_image, "ZKTeco Device Sync", menu)
            self.logger.info("System tray icon created successfully")
            
        except Exception as e:
            self.logger.error(f"Failed to create system tray icon: {e}")
            
    def open_web_interface(self, icon=None, item=None):
        """Open web interface in browser"""
        try:
            webbrowser.open('http://localhost:8080')
            self.logger.info("Web interface opened in browser")
        except Exception as e:
            self.logger.error(f"Failed to open web interface: {e}")
            messagebox.showerror("Error", f"Failed to open web interface: {e}")
            
    def manual_sync(self, icon=None, item=None):
        """Perform manual sync"""
        try:
            self.logger.info("Starting manual sync")
            
            # Run sync in a separate thread to avoid blocking
            sync_thread = threading.Thread(target=self._perform_sync)
            sync_thread.daemon = True
            sync_thread.start()
            
            messagebox.showinfo("Sync Started", "Manual sync has been started. Check the log for details.")
            
        except Exception as e:
            self.logger.error(f"Failed to start manual sync: {e}")
            messagebox.showerror("Error", f"Failed to start manual sync: {e}")
            
    def _perform_sync(self):
        """Perform the actual sync operation"""
        try:
            if not self.device_service:
                self.logger.error("Device service not initialized")
                return
                
            result = self.device_service.sync_device_data()
            
            if result['success']:
                self.logger.info(f"Manual sync completed successfully: {result['message']}")
                if 'data_summary' in result:
                    self.logger.info(f"Data summary: {result['data_summary']}")
            else:
                self.logger.error(f"Manual sync failed: {result['message']}")
                
        except Exception as e:
            self.logger.error(f"Error in manual sync: {e}")
            
    def show_device_status(self, icon=None, item=None):
        """Show device status"""
        try:
            if not self.device_service:
                messagebox.showerror("Error", "Device service not initialized")
                return
                
            status = self.device_service.get_device_status_only()
            
            if status:
                status_text = f"Device Status:\n\n"
                status_text += f"Name: {status.get('device_info', {}).get('device_name', 'Unknown')}\n"
                status_text += f"Serial: {status.get('device_info', {}).get('serial_number', 'Unknown')}\n"
                status_text += f"IP: {status.get('device_info', {}).get('ip_address', 'Unknown')}\n"
                status_text += f"Connection: {'Connected' if status.get('connection_status') else 'Disconnected'}\n"
                status_text += f"Users: {status.get('user_count', 0)}\n"
                status_text += f"Attendance Records: {status.get('attendance_count', 0)}"
                
                messagebox.showinfo("Device Status", status_text)
            else:
                messagebox.showerror("Error", "Failed to get device status")
                
        except Exception as e:
            self.logger.error(f"Failed to get device status: {e}")
            messagebox.showerror("Error", f"Failed to get device status: {e}")
            
    def test_connection(self, icon=None, item=None):
        """Test device and server connections"""
        try:
            if not self.device_service:
                messagebox.showerror("Error", "Device service not initialized")
                return
                
            result = self.device_service.test_connection()
            
            device_ok = result.get('device_connection', False)
            server_ok = result.get('server_connection', False)
            
            status_text = "Connection Test Results:\n\n"
            status_text += f"Device Connection: {'✓ OK' if device_ok else '✗ FAILED'}\n"
            status_text += f"Server Connection: {'✓ OK' if server_ok else '✗ FAILED'}"
            
            if device_ok and server_ok:
                messagebox.showinfo("Connection Test", status_text)
            else:
                messagebox.showwarning("Connection Test", status_text)
                
        except Exception as e:
            self.logger.error(f"Failed to test connections: {e}")
            messagebox.showerror("Error", f"Failed to test connections: {e}")
            
    def show_settings(self, icon=None, item=None):
        """Show settings dialog"""
        try:
            # Create a simple settings dialog
            root = tk.Tk()
            root.title("ZKTeco Sync Settings")
            root.geometry("400x300")
            root.resizable(False, False)
            
            # Device settings
            tk.Label(root, text="Device Settings", font=("Arial", 12, "bold")).pack(pady=10)
            
            tk.Label(root, text=f"Device IP: {self.config.DEVICE_IP}").pack()
            tk.Label(root, text=f"Device Port: {self.config.DEVICE_PORT}").pack()
            tk.Label(root, text=f"Sync Interval: {self.config.SYNC_INTERVAL} seconds").pack()
            
            # Server settings
            tk.Label(root, text="\nServer Settings", font=("Arial", 12, "bold")).pack(pady=10)
            
            server_url = self.config.TARGET_SERVER_URL
            if len(server_url) > 50:
                server_url = server_url[:47] + "..."
            tk.Label(root, text=f"Server URL: {server_url}").pack()
            
            # Sync status
            tk.Label(root, text="\nSync Status", font=("Arial", 12, "bold")).pack(pady=10)
            
            status_text = "Running" if self.sync_running else "Stopped"
            tk.Label(root, text=f"Auto Sync: {status_text}").pack()
            
            # Buttons
            button_frame = tk.Frame(root)
            button_frame.pack(pady=20)
            
            tk.Button(button_frame, text="Close", command=root.destroy).pack(side=tk.LEFT, padx=5)
            
            root.mainloop()
            
        except Exception as e:
            self.logger.error(f"Failed to show settings: {e}")
            messagebox.showerror("Error", f"Failed to show settings: {e}")
            
    def toggle_auto_start(self, icon=None, item=None):
        """Toggle auto-start functionality"""
        try:
            if self.is_auto_start_enabled():
                self.disable_auto_start()
                messagebox.showinfo("Auto-start", "Auto-start has been disabled")
            else:
                self.enable_auto_start()
                messagebox.showinfo("Auto-start", "Auto-start has been enabled")
                
        except Exception as e:
            self.logger.error(f"Failed to toggle auto-start: {e}")
            messagebox.showerror("Error", f"Failed to toggle auto-start: {e}")
            
    def is_auto_start_enabled(self) -> bool:
        """Check if auto-start is enabled"""
        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, 
                                r"Software\Microsoft\Windows\CurrentVersion\Run", 
                                0, winreg.KEY_READ)
            winreg.QueryValueEx(key, "ZKTecoDeviceSync")
            winreg.CloseKey(key)
            return True
        except:
            return False
            
    def enable_auto_start(self):
        """Enable auto-start"""
        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, 
                                r"Software\Microsoft\Windows\CurrentVersion\Run", 
                                0, winreg.KEY_WRITE)
            exe_path = os.path.abspath(sys.argv[0])
            winreg.SetValueEx(key, "ZKTecoDeviceSync", 0, winreg.REG_SZ, exe_path)
            winreg.CloseKey(key)
            self.logger.info("Auto-start enabled")
        except Exception as e:
            self.logger.error(f"Failed to enable auto-start: {e}")
            raise
            
    def disable_auto_start(self):
        """Disable auto-start"""
        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, 
                                r"Software\Microsoft\Windows\CurrentVersion\Run", 
                                0, winreg.KEY_WRITE)
            winreg.DeleteValue(key, "ZKTecoDeviceSync")
            winreg.CloseKey(key)
            self.logger.info("Auto-start disabled")
        except Exception as e:
            self.logger.error(f"Failed to disable auto-start: {e}")
            raise
            
    def view_log(self, icon=None, item=None):
        """Open log file in default text editor"""
        try:
            log_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'zktime_sync.log')
            if os.path.exists(log_file):
                os.startfile(log_file)
            else:
                messagebox.showinfo("Log", "Log file not found")
        except Exception as e:
            self.logger.error(f"Failed to open log file: {e}")
            messagebox.showerror("Error", f"Failed to open log file: {e}")
            
    def exit_app(self, icon=None, item=None):
        """Exit the application"""
        try:
            self.logger.info("Application exiting")
            if self.icon:
                self.icon.stop()
            sys.exit(0)
        except Exception as e:
            self.logger.error(f"Error during exit: {e}")
            sys.exit(1)
            
    def start_scheduled_sync(self):
        """Start the scheduled sync process"""
        try:
            self.logger.info("Starting scheduled sync process")
            self.sync_running = True
            
            # Schedule sync based on configuration
            sync_interval = self.config.SYNC_INTERVAL
            schedule.every(sync_interval).seconds.do(self._scheduled_sync)
            
            # Run the scheduler in a separate thread
            def run_scheduler():
                while self.sync_running:
                    schedule.run_pending()
                    time.sleep(1)
                    
            self.sync_thread = threading.Thread(target=run_scheduler)
            self.sync_thread.daemon = True
            self.sync_thread.start()
            
            self.logger.info(f"Scheduled sync started with {sync_interval} second interval")
            
        except Exception as e:
            self.logger.error(f"Failed to start scheduled sync: {e}")
            
    def _scheduled_sync(self):
        """Perform scheduled sync"""
        try:
            self.logger.info("Starting scheduled sync")
            
            if not self.device_service:
                self.logger.error("Device service not initialized")
                return
                
            result = self.device_service.sync_device_data()
            
            if result['success']:
                self.logger.info(f"Scheduled sync completed successfully: {result['message']}")
                if 'data_summary' in result:
                    self.logger.info(f"Data summary: {result['data_summary']}")
            else:
                self.logger.error(f"Scheduled sync failed: {result['message']}")
                
        except Exception as e:
            self.logger.error(f"Error in scheduled sync: {e}")
            
    def run(self):
        """Run the application"""
        try:
            self.logger.info("Starting ZKTeco Windows Application")
            
            # Start scheduled sync
            self.start_scheduled_sync()
            
            # Run system tray icon
            if self.icon:
                self.icon.run()
            else:
                self.logger.error("System tray icon not available")
                # Fallback: run without system tray
                while True:
                    time.sleep(1)
                    
        except Exception as e:
            self.logger.error(f"Error running application: {e}")
            sys.exit(1)

def main():
    """Main entry point"""
    try:
        app = ZKTecoWindowsApp()
        app.run()
    except Exception as e:
        print(f"Failed to start application: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 