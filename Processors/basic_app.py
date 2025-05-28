import os
import sys
import traceback

try:
    from flask import Flask, render_template, jsonify
    
    app = Flask(__name__, 
                template_folder='templates',
                static_folder='static')
    
    @app.route('/')
    def index():
        print("Index route accessed")
        return jsonify({"status": "ok", "message": "Basic app is running"})
    
    @app.route('/ping')
    def ping():
        return jsonify({"status": "ok", "message": "pong"})
    
    if __name__ == "__main__":
        print("Starting basic Flask app...")
        app.run(host='127.0.0.1', port=8081, debug=True)
        
except Exception as e:
    print(f"CRITICAL ERROR: {str(e)}")
    traceback.print_exc() 