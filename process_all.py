#!/usr/bin/env python
"""
NH3 Cracking Batch Processor
----------------------------
This script processes all text files in the uploads folder using the ExperimentalDataProcessor.
"""
import os
import sys
import glob
import argparse

# Ensure Processors directory is in the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import the processor class
try:
    from Processors import ExperimentalDataProcessor
except ImportError:
    # Fallback for backwards compatibility
    from Main_Web_ProcessorNH3Crack import ExperimentalDataProcessor

def parse_arguments():
    """Parse command-line arguments"""
    parser = argparse.ArgumentParser(description='NH3 Cracking Batch Processor')
    parser.add_argument('--upload-folder', default='uploads', help='Folder containing raw data files')
    parser.add_argument('--reports-folder', default='Reports', help='Folder for processed results')
    parser.add_argument('--pattern', default='*.txt', help='File pattern to process (default: *.txt)')
    return parser.parse_args()

def main():
    """Main entry point"""
    # Parse arguments
    args = parse_arguments()
    
    # Ensure folders exist
    os.makedirs(args.upload_folder, exist_ok=True)
    os.makedirs(args.reports_folder, exist_ok=True)
    
    # Initialize processor
    processor = ExperimentalDataProcessor(
        input_folder=args.upload_folder,
        output_folder=args.reports_folder
    )
    
    # Get all text files in uploads folder
    file_pattern = os.path.join(args.upload_folder, args.pattern)
    files = glob.glob(file_pattern)
    
    if not files:
        print(f"[!] No files matching pattern '{args.pattern}' found in {args.upload_folder}")
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
    
    print(f"\n[+] Results saved to: {os.path.abspath(args.reports_folder)}")

if __name__ == "__main__":
    main() 