#!/usr/bin/env python
"""
NH3 Cracking Processor and Visualizer
-------------------------------------
This script runs the Flask web application for processing and visualizing NH3 cracking experimental data.
"""
import os
import argparse
import logging
from logging.handlers import RotatingFileHandler
import sys

def parse_arguments():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description='Run the NH3 Cracking Flask app')
    parser.add_argument('--debug', action='store_true', help='Run in debug mode')
    parser.add_argument('--port', type=int, default=8080, help='Port to run the app on (default: 8080)')
    parser.add_argument('--host', type=str, default='0.0.0.0', help='Host to run the app on (default: 0.0.0.0)')
    return parser.parse_args()

def setup_logging(debug=False):
    """Set up logging configuration"""
    log_level = logging.DEBUG if debug else logging.INFO
    log_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    
    # Create logs directory if it doesn't exist
    if not os.path.exists('logs'):
        os.makedirs('logs')
    
    # Set up file handler
    file_handler = RotatingFileHandler('logs/app.log', maxBytes=1024*1024*10, backupCount=5)
    file_handler.setFormatter(log_formatter)
    file_handler.setLevel(log_level)
    
    # Set up console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(log_formatter)
    console_handler.setLevel(log_level)
    
    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)
    root_logger.addHandler(file_handler)
    root_logger.addHandler(console_handler)
    
    return root_logger

def main():
    """Main entry point for the application"""
    args = parse_arguments()
    logger = setup_logging(args.debug)
    
    try:
        from app import app
        
        # Configure the app
        app.config['DEBUG'] = args.debug
        app.config['PROPAGATE_EXCEPTIONS'] = args.debug
        
        logger.info(f"Starting NH3 Cracking Flask app on {args.host}:{args.port}")
        app.run(host=args.host, port=args.port, debug=args.debug)
        
    except Exception as e:
        logger.error(f"Failed to start app: {e}", exc_info=True)
        sys.exit(1)

if __name__ == "__main__":
    main() 