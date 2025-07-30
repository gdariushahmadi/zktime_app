#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
API Service for ZKTeco Device Communication
Handles direct communication with ZKTeco attendance devices
"""

import logging
from typing import Optional, Dict, Any, List
from zk import ZK
from datetime import datetime
import time

logger = logging.getLogger(__name__)

class ApiService:
    """Service for handling ZKTeco device API communication"""
    
    def __init__(self, device_ip: str, device_port: int = 4370, timeout: int = 5):
        """
        Initialize API service
        
        Args:
            device_ip: Device IP address
            device_port: Device port (default: 4370)
            timeout: Connection timeout in seconds
        """
        self.device_ip = device_ip
        self.device_port = device_port
        self.timeout = timeout
        self.zk = ZK(device_ip, port=device_port, timeout=timeout)
        self.connection = None
        
    def connect(self) -> bool:
        """
        Connect to the ZKTeco device
        
        Returns:
            bool: True if connection successful, False otherwise
        """
        try:
            logger.info(f"Attempting to connect to device {self.device_ip}:{self.device_port}")
            self.connection = self.zk.connect()
            if self.connection:
                logger.info(f"Successfully connected to device {self.device_ip}:{self.device_port}")
                return True
            else:
                logger.error(f"Failed to connect to device {self.device_ip}:{self.device_port}")
                return False
        except Exception as e:
            logger.error(f"Error connecting to device {self.device_ip}:{self.device_port}: {e}")
            return False
    
    def disconnect(self):
        """Disconnect from the device"""
        try:
            if self.connection:
                self.connection.disconnect()
                logger.info(f"Disconnected from device {self.device_ip}:{self.device_port}")
        except Exception as e:
            logger.error(f"Error disconnecting from device: {e}")
    
    def get_device_info(self) -> Optional[Dict[str, Any]]:
        """
        Get basic device information
        
        Returns:
            Dict containing device information or None if failed
        """
        try:
            # Ensure we have a connection
            if not self.connection or not self.connection.is_enable():
                if not self.connect():
                    return None
            
            device_info = {
                'device_name': self.connection.get_device_name(),
                'serial_number': self.connection.get_serialnumber(),
                'firmware_version': self.connection.get_firmware_version(),
                'device_time': str(self.connection.get_time()),
                'ip_address': self.device_ip,
                'port': self.device_port,
                'sync_timestamp': datetime.now().isoformat()
            }
            
            logger.info(f"Retrieved device info: {device_info['device_name']}")
            return device_info
            
        except Exception as e:
            logger.error(f"Error getting device info: {e}")
            # Try to reconnect on error
            try:
                self.disconnect()
                if self.connect():
                    # Retry once after reconnection
                    device_info = {
                        'device_name': self.connection.get_device_name(),
                        'serial_number': self.connection.get_serialnumber(),
                        'firmware_version': self.connection.get_firmware_version(),
                        'device_time': str(self.connection.get_time()),
                        'ip_address': self.device_ip,
                        'port': self.device_port,
                        'sync_timestamp': datetime.now().isoformat()
                    }
                    logger.info(f"Retrieved device info after reconnection: {device_info['device_name']}")
                    return device_info
            except Exception as retry_e:
                logger.error(f"Error getting device info after reconnection: {retry_e}")
            return None
    
    def get_users_info(self) -> Optional[List[Dict[str, Any]]]:
        """
        Get users information from device
        
        Returns:
            List of user dictionaries or None if failed
        """
        try:
            # Ensure we have a connection
            if not self.connection or not self.connection.is_enable():
                if not self.connect():
                    return None
            
            users = self.connection.get_users()
            users_info = []
            
            for user in users:
                user_info = {
                    'user_id': user.user_id,
                    'name': user.name,
                    'card': user.card,
                    'privilege': user.privilege,
                    'password': user.password,
                    'group_id': user.group_id,
                    'user_sns': user.user_sns,
                    'work_code': user.work_code
                }
                users_info.append(user_info)
            
            logger.info(f"Retrieved {len(users_info)} users from device")
            return users_info
            
        except Exception as e:
            logger.error(f"Error getting users info: {e}")
            # Try to reconnect on error
            try:
                self.disconnect()
                if self.connect():
                    # Retry once after reconnection
                    users = self.connection.get_users()
                    users_info = []
                    
                    for user in users:
                        user_info = {
                            'user_id': user.user_id,
                            'name': user.name,
                            'card': user.card,
                            'privilege': user.privilege,
                            'password': user.password,
                            'group_id': user.group_id,
                            'user_sns': user.user_sns,
                            'work_code': user.work_code
                        }
                        users_info.append(user_info)
                    
                    logger.info(f"Retrieved {len(users_info)} users after reconnection")
                    return users_info
            except Exception as retry_e:
                logger.error(f"Error getting users info after reconnection: {retry_e}")
            return None
    
    def get_attendance_info(self) -> Optional[List[Dict[str, Any]]]:
        """
        Get attendance information from device
        
        Returns:
            List of attendance records or None if failed
        """
        try:
            # Ensure we have a connection
            if not self.connection or not self.connection.is_enable():
                if not self.connect():
                    return None
            
            attendance = self.connection.get_attendance()
            attendance_info = []
            
            for record in attendance:
                attendance_record = {
                    'user_id': record.user_id,
                    'timestamp': str(record.timestamp),
                    'status': record.status,
                    'punch': record.punch
                }
                attendance_info.append(attendance_record)
            
            logger.info(f"Retrieved {len(attendance_info)} attendance records from device")
            return attendance_info
            
        except Exception as e:
            logger.error(f"Error getting attendance info: {e}")
            # Try to reconnect on error
            try:
                self.disconnect()
                if self.connect():
                    # Retry once after reconnection
                    attendance = self.connection.get_attendance()
                    attendance_info = []
                    
                    for record in attendance:
                        attendance_record = {
                            'user_id': record.user_id,
                            'timestamp': str(record.timestamp),
                            'status': record.status,
                            'punch': record.punch
                        }
                        attendance_info.append(attendance_record)
                    
                    logger.info(f"Retrieved {len(attendance_info)} attendance records after reconnection")
                    return attendance_info
            except Exception as retry_e:
                logger.error(f"Error getting attendance info after reconnection: {retry_e}")
            return None
    
    def get_device_status(self) -> Optional[Dict[str, Any]]:
        """
        Get comprehensive device status
        
        Returns:
            Dict containing device status or None if failed
        """
        try:
            # Ensure we have a connection
            if not self.connection or not self.connection.is_enable():
                if not self.connect():
                    return None
            
            # Get basic device info
            device_info = self.get_device_info()
            if not device_info:
                return None
            
            # Get users count
            users = self.get_users_info()
            users_count = len(users) if users else 0
            
            # Get attendance count
            attendance = self.get_attendance_info()
            attendance_count = len(attendance) if attendance else 0
            
            # Compile status
            status = {
                'device_info': device_info,
                'users_count': users_count,
                'attendance_count': attendance_count,
                'connection_status': 'connected',
                'last_sync': datetime.now().isoformat()
            }
            
            logger.info(f"Device status retrieved: {users_count} users, {attendance_count} attendance records")
            return status
            
        except Exception as e:
            logger.error(f"Error getting device status: {e}")
            # Try to reconnect and retry once
            try:
                self.disconnect()
                if self.connect():
                    # Retry getting device info
                    device_info = self.get_device_info()
                    if device_info:
                        users = self.get_users_info()
                        users_count = len(users) if users else 0
                        
                        attendance = self.get_attendance_info()
                        attendance_count = len(attendance) if attendance else 0
                        
                        status = {
                            'device_info': device_info,
                            'users_count': users_count,
                            'attendance_count': attendance_count,
                            'connection_status': 'connected',
                            'last_sync': datetime.now().isoformat()
                        }
                        
                        logger.info(f"Device status retrieved after reconnection: {users_count} users, {attendance_count} attendance records")
                        return status
            except Exception as retry_e:
                logger.error(f"Error getting device status after reconnection: {retry_e}")
            return None
    
    def test_connection(self) -> bool:
        """
        Test device connection
        
        Returns:
            bool: True if connection successful, False otherwise
        """
        try:
            if self.connect():
                # Test if we can actually get device info
                try:
                    device_name = self.connection.get_device_name()
                    logger.info(f"Connection test successful - Device: {device_name}")
                    return True
                except Exception as test_e:
                    logger.error(f"Connection test failed - cannot get device info: {test_e}")
                    return False
            return False
        except Exception as e:
            logger.error(f"Connection test failed: {e}")
            return False 