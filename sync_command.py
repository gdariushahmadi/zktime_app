#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sync Command for ZKTeco Device Information System
Command-line script for scheduled device data synchronization
"""

import argparse
import logging
import sys
import time
from datetime import datetime

from services.device_service import DeviceService
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

def sync_device_data():
    """
    Sync device data to server
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        logger.info("Starting scheduled device data sync")
        
        device_service = DeviceService()
        result = device_service.sync_device_data()
        
        if result['success']:
            logger.info(f"Sync completed successfully: {result['message']}")
            if 'data_summary' in result:
                logger.info(f"Data summary: {result['data_summary']}")
            return True
        else:
            logger.error(f"Sync failed: {result['message']}")
            return False
            
    except Exception as e:
        logger.error(f"Error in sync_device_data: {e}")
        return False

def test_connections():
    """
    Test device and server connections
    
    Returns:
        bool: True if all connections successful, False otherwise
    """
    try:
        logger.info("Testing device and server connections")
        
        device_service = DeviceService()
        result = device_service.test_connection()
        
        device_ok = result.get('device_connection', False)
        server_ok = result.get('server_connection', False)
        
        if device_ok:
            logger.info("Device connection: OK")
        else:
            logger.error("Device connection: FAILED")
            
        if server_ok:
            logger.info("Server connection: OK")
        else:
            logger.error("Server connection: FAILED")
            
        return device_ok and server_ok
        
    except Exception as e:
        logger.error(f"Error in test_connections: {e}")
        return False

def get_device_status():
    """
    Get and display device status
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        logger.info("Getting device status")
        
        device_service = DeviceService()
        status = device_service.get_device_status_only()
        
        if status:
            logger.info("Device status retrieved successfully")
            logger.info(f"Device: {status['device_info']['device_name']}")
            logger.info(f"Serial: {status['device_info']['serial_number']}")
            logger.info(f"Users: {status['users_count']}")
            logger.info(f"Attendance: {status['attendance_count']}")
            return True
        else:
            logger.error("Failed to get device status")
            return False
            
    except Exception as e:
        logger.error(f"Error in get_device_status: {e}")
        return False

def continuous_sync():
    """
    Run continuous sync with specified interval
    """
    try:
        sync_config = Config.get_sync_config()
        interval = sync_config['interval']
        
        logger.info(f"Starting continuous sync with {interval} second interval")
        
        while True:
            logger.info("Running scheduled sync...")
            
            if sync_device_data():
                logger.info("Sync completed successfully")
            else:
                logger.error("Sync failed")
            
            logger.info(f"Waiting {interval} seconds until next sync...")
            time.sleep(interval)
            
    except KeyboardInterrupt:
        logger.info("Continuous sync interrupted by user")
    except Exception as e:
        logger.error(f"Error in continuous sync: {e}")

def main():
    """Main function"""
    parser = argparse.ArgumentParser(description='ZKTeco Device Information Sync Tool')
    parser.add_argument('command', choices=['sync', 'test', 'status', 'continuous'], 
                       help='Command to execute')
    parser.add_argument('--verbose', '-v', action='store_true', 
                       help='Enable verbose logging')
    
    args = parser.parse_args()
    
    # Set verbose logging if requested
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    logger.info(f"Executing command: {args.command}")
    
    try:
        if args.command == 'sync':
            success = sync_device_data()
            sys.exit(0 if success else 1)
            
        elif args.command == 'test':
            success = test_connections()
            sys.exit(0 if success else 1)
            
        elif args.command == 'status':
            success = get_device_status()
            sys.exit(0 if success else 1)
            
        elif args.command == 'continuous':
            continuous_sync()
            
    except Exception as e:
        logger.error(f"Command execution failed: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main() 