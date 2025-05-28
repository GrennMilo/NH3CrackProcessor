import os
import sys
import traceback
import logging
from logging.handlers import RotatingFileHandler

# Set up logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        RotatingFileHandler('app_debug.log', maxBytes=10000000, backupCount=5),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger('app')

try:
    from app import app
    
    # Register error handler for 500 errors
    @app.errorhandler(500)
    def handle_500_error(e):
        error_traceback = traceback.format_exc()
        logger.error(f"500 error: {str(e)}\n{error_traceback}")
        return "500 Internal Server Error: Check logs for details", 500
    
    # Configure the app for debugging
    app.config['DEBUG'] = True
    app.config['TESTING'] = True
    app.config['PROPAGATE_EXCEPTIONS'] = True
    
    logger.info("Starting Flask app in debug mode...")
    # Run the app on all network interfaces
    app.run(host='0.0.0.0', port=8080, debug=True, use_reloader=False)
    
except Exception as e:
    error_traceback = traceback.format_exc()
    logger.error(f"Failed to start app: {str(e)}\n{error_traceback}")
    print(f"CRITICAL ERROR: {str(e)}")
    print(f"Traceback:\n{error_traceback}") 