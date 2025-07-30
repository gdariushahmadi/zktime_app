#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Flask API Server for ZKTeco Device Information System
Provides REST endpoints for device operations
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
import logging
import json
from datetime import datetime

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
CORS(app)  # Enable CORS for all routes

# Initialize controller
device_controller = DeviceController()

@app.route('/')
def index():
    """Root endpoint"""
    return jsonify({
        'message': 'ZKTeco Device Information API',
        'version': '1.0.0',
        'timestamp': datetime.now().isoformat(),
        'endpoints': {
            'GET /api/device/data': 'Get device data',
            'POST /api/device/sync': 'Sync device data to server',
            'GET /api/device/status': 'Get device status',
            'GET /api/device/health': 'Get system health',
            'POST /api/device/test': 'Test connections',
            'GET /api/device/formatted': 'Get formatted data'
        }
    })

@app.route('/api/device/data', methods=['GET'])
def get_device_data():
    """Get device data endpoint"""
    try:
        result = device_controller.get_device_data()
        return jsonify(result), 200 if result['success'] else 500
    except Exception as e:
        logger.error(f"Error in get_device_data endpoint: {e}")
        return jsonify({
            'success': False,
            'message': f'Server error: {str(e)}',
            'timestamp': datetime.now().isoformat()
        }), 500

@app.route('/api/device/sync', methods=['POST'])
def sync_device_data():
    """Sync device data to server endpoint"""
    try:
        result = device_controller.sync_device_data()
        return jsonify(result), 200 if result['success'] else 500
    except Exception as e:
        logger.error(f"Error in sync_device_data endpoint: {e}")
        return jsonify({
            'success': False,
            'message': f'Server error: {str(e)}',
            'timestamp': datetime.now().isoformat()
        }), 500

@app.route('/api/device/status', methods=['GET'])
def get_device_status():
    """Get device status endpoint"""
    try:
        result = device_controller.get_device_status()
        return jsonify(result), 200 if result['success'] else 500
    except Exception as e:
        logger.error(f"Error in get_device_status endpoint: {e}")
        return jsonify({
            'success': False,
            'message': f'Server error: {str(e)}',
            'timestamp': datetime.now().isoformat()
        }), 500

@app.route('/api/device/health', methods=['GET'])
def get_health_status():
    """Get system health status endpoint"""
    try:
        result = device_controller.get_health_status()
        return jsonify(result), 200 if result['success'] else 500
    except Exception as e:
        logger.error(f"Error in get_health_status endpoint: {e}")
        return jsonify({
            'success': False,
            'message': f'Server error: {str(e)}',
            'timestamp': datetime.now().isoformat()
        }), 500

@app.route('/api/device/test', methods=['POST'])
def test_connections():
    """Test device and server connections endpoint"""
    try:
        result = device_controller.test_connections()
        return jsonify(result), 200 if result['success'] else 500
    except Exception as e:
        logger.error(f"Error in test_connections endpoint: {e}")
        return jsonify({
            'success': False,
            'message': f'Server error: {str(e)}',
            'timestamp': datetime.now().isoformat()
        }), 500

@app.route('/api/device/formatted', methods=['GET'])
def get_formatted_data():
    """Get formatted data endpoint"""
    try:
        result = device_controller.get_formatted_data()
        return jsonify(result), 200 if result['success'] else 500
    except Exception as e:
        logger.error(f"Error in get_formatted_data endpoint: {e}")
        return jsonify({
            'success': False,
            'message': f'Server error: {str(e)}',
            'timestamp': datetime.now().isoformat()
        }), 500

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({
        'success': False,
        'message': 'Endpoint not found',
        'timestamp': datetime.now().isoformat()
    }), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return jsonify({
        'success': False,
        'message': 'Internal server error',
        'timestamp': datetime.now().isoformat()
    }), 500

if __name__ == '__main__':
    logger.info("Starting ZKTeco Device Information API Server")
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=False
    ) 