#!/usr/bin/env python
"""
NH3 Cracking Processor and Visualizer - Setup and Run Script

This script performs initial setup and runs the application.
It creates necessary folders, checks for required files,
and then runs the application.
"""

import os
import sys
import subprocess
import platform
import argparse

def parse_arguments():
    """Parse command-line arguments"""
    parser = argparse.ArgumentParser(description='Setup and run the NH3 Cracking Processor and Visualizer')
    parser.add_argument('--no-deps', action='store_true', help='Skip dependency installation')
    parser.add_argument('--no-processing', action='store_true', help='Skip file processing')
    parser.add_argument('--port', type=int, default=8080, help='Port to run the web interface on')
    return parser.parse_args()

def print_header(text):
    """Print a formatted header"""
    print("\n" + "=" * 60)
    print(f" {text}")
    print("=" * 60)

def create_directories():
    """Create necessary directories if they don't exist"""
    print_header("Creating directories")
    
    dirs = ['uploads', 'Reports', 'logs']
    for d in dirs:
        if not os.path.exists(d):
            os.makedirs(d)
            print(f"[✓] Created directory: {d}")
        else:
            print(f"[!] Directory already exists: {d}")

def check_files():
    """Check that required files exist"""
    print_header("Checking required files")
    
    required_files = [
        'app.py',
        'Main_Web_ProcessorNH3Crack.py',
        'run.py',
        'quick_start.py',
        'requirements.txt'
    ]
    
    all_present = True
    for f in required_files:
        if os.path.exists(f):
            print(f"[✓] Found {f}")
        else:
            print(f"[✗] ERROR: Missing required file: {f}")
            all_present = False
    
    if not all_present:
        print("\n[✗] Some required files are missing. Please make sure all files are present.")
        sys.exit(1)

def install_dependencies(skip=False):
    """Install required Python dependencies"""
    if skip:
        print_header("Skipping dependency installation")
        return
    
    print_header("Installing dependencies")
    
    try:
        subprocess.run([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'], check=True)
        print("[✓] Dependencies installed successfully")
    except subprocess.CalledProcessError:
        print("[✗] Failed to install dependencies")
        print("    Please try installing them manually with:")
        print("    pip install -r requirements.txt")
        sys.exit(1)

def run_application(skip_processing=False, port=8080):
    """Run the application"""
    print_header("Starting NH3 Cracking Processor and Visualizer")
    
    cmd = [sys.executable, 'quick_start.py', '--port', str(port)]
    if skip_processing:
        cmd.append('--skip-processing')
    
    print(f"[!] Running command: {' '.join(cmd)}")
    print(f"[!] Web interface will be available at: http://localhost:{port}")
    print("[!] Press Ctrl+C to stop the application")
    
    try:
        subprocess.run(cmd)
    except KeyboardInterrupt:
        print("\n[!] Application stopped by user")
    except Exception as e:
        print(f"[✗] Error running application: {e}")
        sys.exit(1)

def main():
    """Main function"""
    args = parse_arguments()
    
    print_header("NH3 Cracking Processor and Visualizer - Setup")
    print(f"[!] Running on {platform.system()} {platform.release()}")
    print(f"[!] Python version: {platform.python_version()}")
    
    create_directories()
    check_files()
    install_dependencies(args.no_deps)
    run_application(args.no_processing, args.port)

if __name__ == "__main__":
    main() 