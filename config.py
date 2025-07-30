#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Configuration file for ZKTeco Device Information System
"""

import os
from typing import Dict, Any

class Config:
    """Configuration class for the device information system"""
    
    # Device Configuration
    DEVICE_IP = os.getenv('DEVICE_IP', '192.168.70.141')
    DEVICE_PORT = int(os.getenv('DEVICE_PORT', '4370'))
    DEVICE_TIMEOUT = int(os.getenv('DEVICE_TIMEOUT', '5'))
    
    # Target Server Configuration
    TARGET_SERVER_URL = os.getenv('TARGET_SERVER_URL', 'hhttps://panel.sdadparts.com/api/attendance/device-import')
    TARGET_SERVER_TOKEN = os.getenv('TARGET_SERVER_TOKEN', '3|4GQYfJgpAhjlZfumsMMBrKvZyr68L9hVA3V9u5Fnd983ce66')
    
    # Sync Configuration
    SYNC_INTERVAL = int(os.getenv('SYNC_INTERVAL', '3600'))  # seconds
    SYNC_START_TIME = os.getenv('SYNC_START_TIME', '00:00')
    SYNC_END_TIME = os.getenv('SYNC_END_TIME', '23:59')
    
    # Logging Configuration
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FILE = os.getenv('LOG_FILE', 'device_sync.log')
    
    # API Configuration
    API_TIMEOUT = int(os.getenv('API_TIMEOUT', '30'))
    API_RETRY_ATTEMPTS = int(os.getenv('API_RETRY_ATTEMPTS', '3'))
    API_RETRY_DELAY = int(os.getenv('API_RETRY_DELAY', '5'))
    
    @classmethod
    def get_device_config(cls) -> Dict[str, Any]:
        """Get device configuration"""
        return {
            'ip': cls.DEVICE_IP,
            'port': cls.DEVICE_PORT,
            'timeout': cls.DEVICE_TIMEOUT
        }
    
    @classmethod
    def get_server_config(cls) -> Dict[str, Any]:
        """Get target server configuration"""
        return {
            'url': cls.TARGET_SERVER_URL,
            'token': cls.TARGET_SERVER_TOKEN,
            'timeout': cls.API_TIMEOUT,
            'retry_attempts': cls.API_RETRY_ATTEMPTS,
            'retry_delay': cls.API_RETRY_DELAY
        }
    
    @classmethod
    def get_sync_config(cls) -> Dict[str, Any]:
        """Get sync configuration"""
        return {
            'interval': cls.SYNC_INTERVAL,
            'start_time': cls.SYNC_START_TIME,
            'end_time': cls.SYNC_END_TIME
        } 