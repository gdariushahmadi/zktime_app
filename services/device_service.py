#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Device Service for ZKTeco Device Information System
Main service for device data operations and server synchronization
"""

import logging
import requests
import json
from typing import Optional, Dict, Any, List
from datetime import datetime, timedelta
import time

from .api_service import ApiService
from config import Config

logger = logging.getLogger(__name__)

class DeviceService:
    """Main service for device data operations and server synchronization"""
    
    def __init__(self):
        """Initialize device service"""
        self.config = Config()
        self.api_service = None
        self._initialize_api_service()
    
    def _initialize_api_service(self):
        """Initialize API service with device configuration"""
        device_config = self.config.get_device_config()
        self.api_service = ApiService(
            device_ip=device_config['ip'],
            device_port=device_config['port'],
            timeout=device_config['timeout']
        )
    
    def get_device_data(self) -> Optional[Dict[str, Any]]:
        """
        Get comprehensive device data
        
        Returns:
            Dict containing all device data or None if failed
        """
        try:
            logger.info("Starting device data retrieval")
            
            # Get device status
            device_status = self.api_service.get_device_status()
            if not device_status:
                logger.error("Failed to get device status")
                return None
            
            # Get users information
            users_info = self.api_service.get_users_info()
            
            # Get attendance information
            attendance_info = self.api_service.get_attendance_info()
            
            # Compile complete data
            device_data = {
                'device_status': device_status,
                'users': users_info or [],
                'attendance': attendance_info or [],
                'sync_info': {
                    'sync_timestamp': datetime.now().isoformat(),
                    'sync_status': 'success',
                    'total_users': len(users_info) if users_info else 0,
                    'total_attendance': len(attendance_info) if attendance_info else 0
                }
            }
            
            logger.info(f"Device data retrieved successfully: {device_data['sync_info']['total_users']} users, {device_data['sync_info']['total_attendance']} attendance records")
            return device_data
            
        except Exception as e:
            logger.error(f"Error getting device data: {e}")
            return None
    
    def format_data_for_server(self, device_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Format device data for server transmission according to API specification
        
        Args:
            device_data: Raw device data
            
        Returns:
            Formatted data for server in the required API format
        """
        try:
            # Get attendance records and users from device data
            attendance_records = device_data.get('attendance', [])
            users_list = device_data.get('users', [])
            
            # Create user lookup dictionary for names
            user_lookup = {}
            for user in users_list:
                user_lookup[user.get('user_id', '')] = user.get('name', 'Unknown User')
            
            # Group attendance records by date and user
            attendance_by_date_user = {}
            
            for record in attendance_records:
                # Extract date and user info from attendance record
                # Assuming record structure: {'user_id': '12345', 'timestamp': '2024-01-01 08:00:00', ...}
                if 'timestamp' in record:
                    # Parse timestamp to get date and time
                    try:
                        timestamp = datetime.fromisoformat(record['timestamp'].replace('Z', '+00:00'))
                        date_str = timestamp.strftime('%Y-%m-%d')
                        time_str = timestamp.strftime('%H:%M:%S')  # Changed to H:i:s format
                        user_id = record.get('user_id', 'unknown')
                        
                        # Get user name from lookup or use user_id as fallback
                        user_name = user_lookup.get(user_id, f"User {user_id}")
                        
                        if date_str not in attendance_by_date_user:
                            attendance_by_date_user[date_str] = {}
                        
                        if user_id not in attendance_by_date_user[date_str]:
                            attendance_by_date_user[date_str][user_id] = {
                                'date': date_str,
                                'id_number': user_id,
                                'name': user_name,
                                'times': [],
                                'card': '0',
                                'attendance_details': []
                            }
                        
                        # Add time to times array
                        if time_str not in attendance_by_date_user[date_str][user_id]['times']:
                            attendance_by_date_user[date_str][user_id]['times'].append(time_str)
                        
                        # Add detailed record
                        detail_record = {
                            'date': date_str,
                            'id_number': user_id,
                            'name': user_name,
                            'time': time_str,
                            'status': 'Check In' if len(attendance_by_date_user[date_str][user_id]['times']) % 2 == 1 else 'Check Out',
                            'verification': 'Fingerprint'  # Default verification method
                        }
                        attendance_by_date_user[date_str][user_id]['attendance_details'].append(detail_record)
                        
                    except Exception as e:
                        logger.warning(f"Error parsing attendance record: {e}")
                        continue
            
            # Convert to the required API format
            formatted_records = []
            all_dates = sorted(attendance_by_date_user.keys())
            
            for date_str in all_dates:
                for user_id, user_data in attendance_by_date_user[date_str].items():
                    # Sort times chronologically
                    user_data['times'].sort()
                    
                    # Create the record in API format
                    record = {
                        'date': user_data['date'],
                        'id_number': user_data['id_number'],
                        'name': user_data['name'],
                        'times': user_data['times'],
                        'card': user_data['card']
                    }
                    
                    # Add daily details if there are multiple entries
                    if len(user_data['attendance_details']) > 1:
                        record['daily'] = {
                            'date': user_data['date'],
                            'user_id': user_data['id_number'],
                            'attendance_details': user_data['attendance_details']
                        }
                    
                    formatted_records.append(record)
            
            # Determine period dates
            if all_dates:
                start_date = min(all_dates)
                end_date = max(all_dates)
            else:
                # If no attendance data, use current date
                today = datetime.now().strftime('%Y-%m-%d')
                start_date = today
                end_date = today
            
            # Create the final API format
            api_data = {
                'period': {
                    'start_date': start_date,
                    'end_date': end_date
                },
                'attendance_records': formatted_records
            }
            
            logger.info(f"Formatted {len(formatted_records)} attendance records for API")
            return api_data
            
        except Exception as e:
            logger.error(f"Error formatting data for server: {e}")
            return None
    
    def send_to_server(self, data: Dict[str, Any]) -> bool:
        """
        Send data to target server
        
        Args:
            data: Formatted data to send
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            server_config = self.config.get_server_config()
            
            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {server_config["token"]}',
                'Accept': 'application/json'
            }
            
            logger.info(f"Sending data to server: {server_config['url']}")
            
            # Retry mechanism
            for attempt in range(server_config['retry_attempts']):
                try:
                    response = requests.post(
                        server_config['url'],
                        json=data,
                        headers=headers,
                        timeout=server_config['timeout'],
                        verify=False  # Disable SSL verification for internal devices
                    )
                    
                    if response.status_code == 200:
                        logger.info(f"Data sent successfully to server. Response: {response.text}")
                        return True
                    else:
                        logger.warning(f"Server returned status {response.status_code}: {response.text}")
                        
                except requests.exceptions.RequestException as e:
                    logger.warning(f"Request attempt {attempt + 1} failed: {e}")
                    if attempt < server_config['retry_attempts'] - 1:
                        time.sleep(server_config['retry_delay'])
                        continue
                    else:
                        logger.error(f"All retry attempts failed")
                        return False
            
            return False
            
        except Exception as e:
            logger.error(f"Error sending data to server: {e}")
            return False
    
    def sync_device_data(self) -> Dict[str, Any]:
        """
        Sync device data to server
        
        Returns:
            Dict containing sync result
        """
        try:
            logger.info("Starting device data sync")
            
            # Get device data
            device_data = self.get_device_data()
            if not device_data:
                return {
                    'success': False,
                    'message': 'Failed to retrieve device data',
                    'timestamp': datetime.now().isoformat()
                }
            
            # Format data for server
            formatted_data = self.format_data_for_server(device_data)
            if not formatted_data:
                return {
                    'success': False,
                    'message': 'Failed to format data for server',
                    'timestamp': datetime.now().isoformat()
                }
            
            # Send to server
            if self.send_to_server(formatted_data):
                return {
                    'success': True,
                    'message': 'Device data synced successfully',
                    'timestamp': datetime.now().isoformat(),
                    'data_summary': {
                        'users_count': device_data['sync_info']['total_users'],
                        'attendance_count': device_data['sync_info']['total_attendance']
                    }
                }
            else:
                return {
                    'success': False,
                    'message': 'Failed to send data to server',
                    'timestamp': datetime.now().isoformat()
                }
                
        except Exception as e:
            logger.error(f"Error in device data sync: {e}")
            return {
                'success': False,
                'message': f'Sync error: {str(e)}',
                'timestamp': datetime.now().isoformat()
            }
    
    def test_connection(self) -> Dict[str, Any]:
        """
        Test device and server connections
        
        Returns:
            Dict containing test results
        """
        try:
            results = {
                'device_connection': False,
                'server_connection': False,
                'timestamp': datetime.now().isoformat()
            }
            
            # Test device connection
            if self.api_service.test_connection():
                results['device_connection'] = True
                logger.info("Device connection test successful")
            else:
                logger.error("Device connection test failed")
            
            # Test server connection
            server_config = self.config.get_server_config()
            try:
                headers = {
                    'Authorization': f'Bearer {server_config["token"]}',
                    'Accept': 'application/json'
                }
                
                response = requests.get(
                    server_config['url'].replace('/import', '/health'),
                    headers=headers,
                    timeout=server_config['timeout'],
                    verify=False
                )
                
                if response.status_code in [200, 404]:  # 404 is acceptable for health check
                    results['server_connection'] = True
                    logger.info("Server connection test successful")
                else:
                    logger.error(f"Server connection test failed: {response.status_code}")
                    
            except Exception as e:
                logger.error(f"Server connection test failed: {e}")
            
            return results
            
        except Exception as e:
            logger.error(f"Error in connection test: {e}")
            return {
                'device_connection': False,
                'server_connection': False,
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }
    
    def get_device_status_only(self) -> Optional[Dict[str, Any]]:
        """
        Get only device status information (lightweight)
        
        Returns:
            Dict containing device status or None if failed
        """
        try:
            return self.api_service.get_device_status()
        except Exception as e:
            logger.error(f"Error getting device status: {e}")
            return None 