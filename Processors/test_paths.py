import os
import urllib.parse
import json

def check_experiment_files(experiment_name):
    """Check if plot files exist for the given experiment."""
    print(f"Checking files for experiment: {experiment_name}")
    
    # Define the reports folder
    reports_folder = "reports"
    
    # URL decode the experiment name
    decoded_name = urllib.parse.unquote(experiment_name)
    print(f"Decoded experiment name: {decoded_name}")
    
    # Map of plot types to filenames
    plot_type_map = {
        'temperature': f"{decoded_name}_temp_plotly_data.json",
        'multipoint': f"{decoded_name}_multipoint_temp_plotly_data.json",
        'saturator': f"{decoded_name}_saturator_temp_plotly_data.json",
        'pressure': f"{decoded_name}_pressure_plotly_data.json",
        'flow': f"{decoded_name}_flow_plotly_data.json",
        'outlet': f"{decoded_name}_outlet_plotly_data.json"
    }
    
    # Check experiment directory
    exp_dir = os.path.join(reports_folder, decoded_name)
    print(f"Experiment directory: {exp_dir}")
    print(f"Directory exists: {os.path.exists(exp_dir)}")
    
    # Check if each plot file exists
    for plot_type, filename in plot_type_map.items():
        plotly_path = os.path.join(exp_dir, filename)
        exists = os.path.exists(plotly_path)
        print(f"Plot file {plot_type}: {plotly_path}")
        print(f"File exists: {exists}")
        
        if exists:
            try:
                with open(plotly_path, 'r') as f:
                    data = json.load(f)
                print(f"  - JSON valid: Yes")
                print(f"  - Size: {os.path.getsize(plotly_path)} bytes")
            except json.JSONDecodeError:
                print(f"  - JSON valid: No (invalid JSON)")
            except Exception as e:
                print(f"  - Error reading file: {str(e)}")
    
    # Check a couple of stage directories
    for stage_num in [1, 10]:
        stage_dir = os.path.join(exp_dir, f"stage_{stage_num}")
        print(f"\nStage {stage_num} directory: {stage_dir}")
        print(f"Directory exists: {os.path.exists(stage_dir)}")
        
        if os.path.exists(stage_dir):
            # Map of plot types to stage filenames
            stage_plot_type_map = {
                'temperature': f"stage_{stage_num}_temp_plotly.json",
                'multipoint': f"stage_{stage_num}_multipoint_temp_plotly.json",
                'saturator': f"stage_{stage_num}_saturator_temp_plotly.json",
                'pressure': f"stage_{stage_num}_pressure_plotly.json",
                'flow': f"stage_{stage_num}_flow_plotly.json",
                'outlet': f"stage_{stage_num}_outlet_plotly.json"
            }
            
            # Check if each stage plot file exists
            for plot_type, filename in stage_plot_type_map.items():
                plotly_path = os.path.join(stage_dir, filename)
                exists = os.path.exists(plotly_path)
                print(f"Stage plot file {plot_type}: {plotly_path}")
                print(f"File exists: {exists}")
                
                if exists:
                    try:
                        with open(plotly_path, 'r') as f:
                            data = json.load(f)
                        print(f"  - JSON valid: Yes")
                        print(f"  - Size: {os.path.getsize(plotly_path)} bytes")
                    except json.JSONDecodeError:
                        print(f"  - JSON valid: No (invalid JSON)")
                    except Exception as e:
                        print(f"  - Error reading file: {str(e)}")

if __name__ == "__main__":
    # Test with the problematic experiment
    check_experiment_files("25_02_28 14_02_06 Exp 011_Blak_Silcotek_New_SiO2_TC_QRZ") 