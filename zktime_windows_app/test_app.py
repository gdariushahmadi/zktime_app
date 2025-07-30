#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test script for ZKTeco Windows Application
Tests basic functionality without system tray
"""

import sys
import os
import logging
import time
from datetime import datetime

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import Config
from services.device_service import DeviceService

def setup_test_logging():
    """Setup logging for testing"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('test_app.log', encoding='utf-8'),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger(__name__)

def test_config():
    """Test configuration loading"""
    logger = logging.getLogger(__name__)
    logger.info("Testing configuration...")
    
    try:
        config = Config()
        logger.info(f"Device IP: {config.DEVICE_IP}")
        logger.info(f"Device Port: {config.DEVICE_PORT}")
        logger.info(f"Sync Interval: {config.SYNC_INTERVAL}")
        logger.info(f"Server URL: {config.TARGET_SERVER_URL}")
        logger.info("Configuration test: PASSED")
        return True
    except Exception as e:
        logger.error(f"Configuration test: FAILED - {e}")
        return False

def test_device_service():
    """Test device service initialization"""
    logger = logging.getLogger(__name__)
    logger.info("Testing device service...")
    
    try:
        device_service = DeviceService()
        logger.info("Device service initialized successfully")
        logger.info("Device service test: PASSED")
        return True
    except Exception as e:
        logger.error(f"Device service test: FAILED - {e}")
        return False

def test_connection():
    """Test device and server connections"""
    logger = logging.getLogger(__name__)
    logger.info("Testing connections...")
    
    try:
        device_service = DeviceService()
        result = device_service.test_connection()
        
        device_ok = result.get('device_connection', False)
        server_ok = result.get('server_connection', False)
        
        logger.info(f"Device connection: {'OK' if device_ok else 'FAILED'}")
        logger.info(f"Server connection: {'OK' if server_ok else 'FAILED'}")
        
        if device_ok and server_ok:
            logger.info("Connection test: PASSED")
            return True
        else:
            logger.warning("Connection test: PARTIAL - Some connections failed")
            return False
            
    except Exception as e:
        logger.error(f"Connection test: FAILED - {e}")
        return False

def test_device_status():
    """Test device status retrieval"""
    logger = logging.getLogger(__name__)
    logger.info("Testing device status...")
    
    try:
        device_service = DeviceService()
        status = device_service.get_device_status_only()
        
        if status:
            logger.info(f"Device name: {status.get('device_info', {}).get('device_name', 'Unknown')}")
            logger.info(f"Serial number: {status.get('device_info', {}).get('serial_number', 'Unknown')}")
            logger.info(f"IP address: {status.get('device_info', {}).get('ip_address', 'Unknown')}")
            logger.info(f"Connection status: {status.get('connection_status', False)}")
            logger.info("Device status test: PASSED")
            return True
        else:
            logger.error("Device status test: FAILED - No status returned")
            return False
            
    except Exception as e:
        logger.error(f"Device status test: FAILED - {e}")
        return False

def test_sync():
    """Test data synchronization"""
    logger = logging.getLogger(__name__)
    logger.info("Testing data synchronization...")
    
    try:
        device_service = DeviceService()
        result = device_service.sync_device_data()
        
        if result['success']:
            logger.info(f"Sync successful: {result['message']}")
            if 'data_summary' in result:
                logger.info(f"Data summary: {result['data_summary']}")
            logger.info("Sync test: PASSED")
            return True
        else:
            logger.error(f"Sync failed: {result['message']}")
            logger.warning("Sync test: FAILED")
            return False
            
    except Exception as e:
        logger.error(f"Sync test: FAILED - {e}")
        return False

def run_all_tests():
    """Run all tests"""
    logger = setup_test_logging()
    logger.info("Starting ZKTeco Windows Application tests...")
    
    tests = [
        ("Configuration", test_config),
        ("Device Service", test_device_service),
        ("Connection", test_connection),
        ("Device Status", test_device_status),
        ("Data Sync", test_sync)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        logger.info(f"\n{'='*50}")
        logger.info(f"Running {test_name} test...")
        logger.info(f"{'='*50}")
        
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            logger.error(f"Test {test_name} crashed: {e}")
            results.append((test_name, False))
    
    # Summary
    logger.info(f"\n{'='*50}")
    logger.info("TEST SUMMARY")
    logger.info(f"{'='*50}")
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "PASSED" if result else "FAILED"
        logger.info(f"{test_name}: {status}")
        if result:
            passed += 1
    
    logger.info(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        logger.info("All tests passed! Application is ready for use.")
    else:
        logger.warning(f"{total - passed} tests failed. Check configuration and network connectivity.")
    
    return passed == total

def main():
    """Main test function"""
    print("ZKTeco Windows Application Test Suite")
    print("=====================================")
    print()
    
    success = run_all_tests()
    
    if success:
        print("\n✅ All tests passed! The application is ready for building.")
        print("Run 'python build_exe.py' to create the executable.")
    else:
        print("\n❌ Some tests failed. Please check the configuration and network connectivity.")
        print("Review the test_app.log file for detailed information.")
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 