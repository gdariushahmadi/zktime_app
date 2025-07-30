#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Device Controller for ZKTeco Device Information System
Provides API endpoints for device operations
"""

import logging
import json
from typing import Dict, Any
from datetime import datetime

from services.device_service import DeviceService

logger = logging.getLogger(__name__)

class DeviceController:
    """Controller for device operations and API endpoints"""
    
    def __init__(self):
        """Initialize device controller"""
        self.device_service = DeviceService()
    
    def get_device_data(self) -> Dict[str, Any]:
        """
        Get device data via API
        
        Returns:
            Dict containing API response
        """
        try:
            logger.info("API: Getting device data")
            
            device_data = self.device_service.get_device_data()
            if device_data:
                return {
                    'success': True,
                    'message': 'Device data retrieved successfully',
                    'data': device_data,
                    'timestamp': datetime.now().isoformat()
                }
            else:
                return {
                    'success': False,
                    'message': 'Failed to retrieve device data',
                    'timestamp': datetime.now().isoformat()
                }
                
        except Exception as e:
            logger.error(f"API Error getting device data: {e}")
            return {
                'success': False,
                'message': f'Error: {str(e)}',
                'timestamp': datetime.now().isoformat()
            }
    
    def sync_device_data(self) -> Dict[str, Any]:
        """
        Sync device data to server via API
        
        Returns:
            Dict containing sync result
        """
        try:
            logger.info("API: Syncing device data")
            
            result = self.device_service.sync_device_data()
            return result
            
        except Exception as e:
            logger.error(f"API Error syncing device data: {e}")
            return {
                'success': False,
                'message': f'Sync error: {str(e)}',
                'timestamp': datetime.now().isoformat()
            }
    
    def get_device_status(self) -> Dict[str, Any]:
        """
        Get device status only (lightweight) via API
        
        Returns:
            Dict containing device status
        """
        try:
            logger.info("API: Getting device status")
            
            status = self.device_service.get_device_status_only()
            if status:
                return {
                    'success': True,
                    'message': 'Device status retrieved successfully',
                    'data': status,
                    'timestamp': datetime.now().isoformat()
                }
            else:
                return {
                    'success': False,
                    'message': 'Failed to retrieve device status',
                    'timestamp': datetime.now().isoformat()
                }
                
        except Exception as e:
            logger.error(f"API Error getting device status: {e}")
            return {
                'success': False,
                'message': f'Error: {str(e)}',
                'timestamp': datetime.now().isoformat()
            }
    
    def test_connections(self) -> Dict[str, Any]:
        """
        Test device and server connections via API
        
        Returns:
            Dict containing test results
        """
        try:
            logger.info("API: Testing connections")
            
            results = self.device_service.test_connection()
            return {
                'success': True,
                'message': 'Connection test completed',
                'data': results
            }
            
        except Exception as e:
            logger.error(f"API Error testing connections: {e}")
            return {
                'success': False,
                'message': f'Test error: {str(e)}',
                'timestamp': datetime.now().isoformat()
            }
    
    def get_health_status(self) -> Dict[str, Any]:
        """
        Get system health status via API
        
        Returns:
            Dict containing health status
        """
        try:
            logger.info("API: Getting health status")
            
            # Test device connection
            device_status = self.device_service.get_device_status_only()
            
            # Test server connection
            connection_test = self.device_service.test_connection()
            
            health_status = {
                'system_status': 'healthy' if device_status else 'unhealthy',
                'device_connection': connection_test.get('device_connection', False),
                'server_connection': connection_test.get('server_connection', False),
                'last_check': datetime.now().isoformat(),
                'device_info': device_status.get('device_info', {}) if device_status else {}
            }
            
            return {
                'success': True,
                'message': 'Health status retrieved successfully',
                'data': health_status
            }
            
        except Exception as e:
            logger.error(f"API Error getting health status: {e}")
            return {
                'success': False,
                'message': f'Health check error: {str(e)}',
                'timestamp': datetime.now().isoformat()
            }
    
    def get_formatted_data(self) -> Dict[str, Any]:
        """
        Get formatted data ready for server transmission via API
        
        Returns:
            Dict containing formatted data
        """
        try:
            logger.info("API: Getting formatted data")
            
            device_data = self.device_service.get_device_data()
            if not device_data:
                return {
                    'success': False,
                    'message': 'Failed to retrieve device data',
                    'timestamp': datetime.now().isoformat()
                }
            
            formatted_data = self.device_service.format_data_for_server(device_data)
            if not formatted_data:
                return {
                    'success': False,
                    'message': 'Failed to format data',
                    'timestamp': datetime.now().isoformat()
                }
            
            return {
                'success': True,
                'message': 'Formatted data retrieved successfully',
                'data': formatted_data,
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"API Error getting formatted data: {e}")
            return {
                'success': False,
                'message': f'Error: {str(e)}',
                'timestamp': datetime.now().isoformat()
            } 