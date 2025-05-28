#!/usr/bin/env python
"""
NH3 Cracking Processor - Quick Start
-----------------------------------
This script processes all files in the uploads folder and then starts the web interface.
"""
import os
import glob
import sys
import subprocess
import argparse
from Main_Web_ProcessorNH3Crack import ExperimentalDataProcessor

def parse_arguments():
    """Parse command-line arguments"""
    parser = argparse.ArgumentParser(description='NH3 Cracking Processor - Quick Start')
    parser.add_argument('--upload-folder', default='uploads', help='Folder containing raw data files')
    parser.add_argument('--reports-folder', default='Reports', help='Folder for processed results')
    parser.add_argument('--skip-processing', action='store_true', help='Skip processing files, just start web interface')
    parser.add_argument('--port', type=int, default=8080, help='Port for web interface')
    parser.add_argument('--pattern', default='*.txt', help='File pattern to process (default: *.txt)')
    return parser.parse_args()

def process_files(upload_folder, reports_folder, pattern):
    """Process all files matching pattern in upload folder"""
    # Initialize processor
    processor = ExperimentalDataProcessor(
        input_folder=upload_folder,
        output_folder=reports_folder
    )
    
    # Get all text files in uploads folder
    file_pattern = os.path.join(upload_folder, pattern)
    files = glob.glob(file_pattern)
    
    if not files:
        print(f"[!] No files matching pattern '{pattern}' found in {upload_folder}")
        return
    
    print(f"[+] Found {len(files)} files to process")
    
    # Process each file
    processed_files = []
    errors = []
    
    for i, file_path in enumerate(files, 1):
        filename = os.path.basename(file_path)
        print(f"[{i}/{len(files)}] Processing {filename}...")
        
        try:
            processor.process_file(filename)
            processed_files.append(filename)
            print(f"[✓] Successfully processed {filename}")
        except Exception as e:
            print(f"[✗] Error processing {filename}: {str(e)}")
            errors.append({
                "file": filename,
                "error": str(e)
            })
    
    # Print summary
    print("\n" + "="*50)
    print(f"[+] Processing complete!")
    print(f"[+] Successfully processed: {len(processed_files)} files")
    print(f"[+] Errors: {len(errors)} files")
    
    if errors:
        print("\n[!] Files with errors:")
        for error in errors:
            print(f"    - {error['file']}: {error['error']}")
    
    print(f"\n[+] Results saved to: {os.path.abspath(reports_folder)}")

def start_web_interface(port):
    """Start the Flask web interface"""
    print("\n" + "="*50)
    print(f"[+] Starting web interface at http://localhost:{port}")
    print(f"[+] Press Ctrl+C to stop the server")
    print("="*50 + "\n")
    
    # Start Flask app
    cmd = [sys.executable, "run.py", "--port", str(port)]
    subprocess.run(cmd)

def main():
    """Main entry point"""
    args = parse_arguments()
    
    # Ensure folders exist
    os.makedirs(args.upload_folder, exist_ok=True)
    os.makedirs(args.reports_folder, exist_ok=True)
    
    # Print header
    print("\n" + "="*50)
    print(f"[+] NH3 Cracking Processor - Quick Start")
    print(f"[+] Upload Folder: {os.path.abspath(args.upload_folder)}")
    print(f"[+] Reports Folder: {os.path.abspath(args.reports_folder)}")
    print("="*50 + "\n")
    
    # Process files if not skipped
    if not args.skip_processing:
        process_files(args.upload_folder, args.reports_folder, args.pattern)
    
    # Start web interface
    start_web_interface(args.port)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n[!] Process interrupted by user")
        sys.exit(0) 