"""
Script to regenerate plots for a specific experiment
"""
import os
import json
import pandas as pd
from datetime import datetime
from Main_Web_ProcessorNH3Crack import ExperimentalDataProcessor

def fix_experiment_plots(experiment_name):
    """Fix plots for a specific experiment"""
    print(f"Fixing plots for experiment: {experiment_name}")
    
    # Initialize processor
    processor = ExperimentalDataProcessor(
        input_folder="uploads",
        output_folder="Reports"
    )
    
    experiment_dir = os.path.join("Reports", experiment_name)
    if not os.path.exists(experiment_dir):
        print(f"Error: Experiment directory not found: {experiment_dir}")
        return
    
    # Get stage directories
    stage_folders = []
    for folder in os.listdir(experiment_dir):
        if folder.startswith('stage_') and os.path.isdir(os.path.join(experiment_dir, folder)):
            stage_folders.append(folder)
    
    if not stage_folders:
        print(f"Error: No stage folders found in {experiment_dir}")
        return
    
    # Process each stage
    stage_numbers = []
    stages_data = {}
    
    for folder in stage_folders:
        try:
            stage_num = int(folder.replace('stage_', ''))
            stage_numbers.append(stage_num)
            
            # Load stage data
            stage_dir = os.path.join(experiment_dir, folder)
            stage_data_file = os.path.join(stage_dir, f"stage_{stage_num}_data.json")
            
            if not os.path.exists(stage_data_file):
                print(f"Warning: Stage data file not found: {stage_data_file}")
                continue
            
            # Load data and convert to DataFrame
            with open(stage_data_file, 'r') as f:
                stage_data = json.load(f)
            
            stage_df = pd.DataFrame(stage_data)
            stages_data[stage_num] = stage_df
            
            # Generate plot files for this stage
            print(f"Generating plots for stage {stage_num}")
            processor.create_stage_plotly_json(
                stage_df, 
                stage_num, 
                experiment_name, 
                stage_dir
            )
            
        except Exception as e:
            print(f"Error processing stage {folder}: {str(e)}")
    
    # Create overall plots
    if stages_data:
        print(f"Generating overall plots for {len(stages_data)} stages")
        processor.create_plotly_json(
            stages_data,
            experiment_name,
            datetime.now().strftime("%Y%m%d_%H%M%S"),
            experiment_dir
        )
        print("Overall plots generated successfully")
    else:
        print("No stage data loaded, skipping overall plots")

if __name__ == "__main__":
    # Fix the problematic experiment
    fix_experiment_plots("25_02_28 14_02_06 Exp 011_Blak_Silcotek_New_SiO2_TC_QRZ") 