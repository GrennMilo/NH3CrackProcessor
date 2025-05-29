#!/usr/bin/env python
"""
Fix NaN values in JSON files
---------------------------
This script fixes JSON files containing 'NaN' values, which cause parsing errors in JavaScript.
It replaces 'NaN' with 'null', which is a valid JSON value.
"""

import os
import sys
import json
import argparse

# Ensure Processors directory is in the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import the processor class
try:
    from Processors import ExperimentalDataProcessor
except ImportError:
    # Fallback for backwards compatibility
    from Main_Web_ProcessorNH3Crack import ExperimentalDataProcessor

def main():
    parser = argparse.ArgumentParser(description='Fix JSON files with NaN values')
    parser.add_argument('experiment', nargs='?', help='Name of the experiment to fix (if omitted, all experiments will be processed)')
    parser.add_argument('--reports-dir', default='Reports', help='Path to the Reports directory')
    parser.add_argument('--uploads-dir', default='uploads', help='Path to the uploads directory')
    args = parser.parse_args()

    # Initialize processor
    processor = ExperimentalDataProcessor(input_folder=args.uploads_dir, output_folder=args.reports_dir)
    
    if args.experiment:
        # Fix a single experiment
        print(f"=== Fixing JSON files for experiment: {args.experiment} ===")
        success = processor.fix_plotly_json_files(args.experiment)
        if success:
            print(f"Successfully fixed JSON files for {args.experiment}")
        else:
            print(f"Failed to fix JSON files for {args.experiment}")
    else:
        # Fix all experiments
        print("=== Fixing JSON files for all experiments ===")
        success_count = 0
        error_count = 0
        
        # Find all experiment directories
        experiments = []
        try:
            for item in os.listdir(args.reports_dir):
                exp_dir = os.path.join(args.reports_dir, item)
                if os.path.isdir(exp_dir):
                    experiments.append(item)
                    
            print(f"Found {len(experiments)} experiments")
            
            # Process each experiment
            for experiment in experiments:
                print(f"\nProcessing {experiment}...")
                try:
                    success = processor.fix_plotly_json_files(experiment)
                    if success:
                        success_count += 1
                    else:
                        error_count += 1
                except Exception as e:
                    print(f"Error processing {experiment}: {e}")
                    error_count += 1
                    
            print(f"\n=== Summary ===")
            print(f"Successfully processed {success_count} experiments")
            print(f"Failed to process {error_count} experiments")
        except Exception as e:
            print(f"Error listing experiments: {e}")
            return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main()) 