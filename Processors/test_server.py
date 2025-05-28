import os
import json
from flask import Flask, jsonify, request
import urllib.parse

app = Flask(__name__)

@app.route('/test/overall')
def test_overall():
    """Test endpoint for overall experiment plot data"""
    # Define the experiment name
    experiment_name = "25_02_28 14_02_06 Exp 011_Blak_Silcotek_New_SiO2_TC_QRZ"
    
    # Get plot type from query parameters (default to 'temperature')
    plot_type = request.args.get('type', 'temperature')
    
    # Map of plot types to filenames
    plot_type_map = {
        'temperature': f"{experiment_name}_temp_plotly_data.json",
        'multipoint': f"{experiment_name}_multipoint_temp_plotly_data.json",
        'saturator': f"{experiment_name}_saturator_temp_plotly_data.json",
        'pressure': f"{experiment_name}_pressure_plotly_data.json",
        'flow': f"{experiment_name}_flow_plotly_data.json",
        'outlet': f"{experiment_name}_outlet_plotly_data.json"
    }
    
    # Check if the requested plot type is valid
    if plot_type not in plot_type_map:
        return jsonify({"error": f"Invalid plot type: {plot_type}", "available_types": list(plot_type_map.keys())}), 400
    
    # Get the filename for the requested plot type
    filename = plot_type_map[plot_type]
    
    # Check for overall plotly file
    exp_dir = os.path.join("reports", experiment_name)
    plotly_path = os.path.join(exp_dir, filename)
    
    print(f"Looking for plot file at: {plotly_path}")
    print(f"File exists: {os.path.exists(plotly_path)}")
    
    if not os.path.exists(plotly_path):
        return jsonify({"error": "Overall plot data not found"}), 404
    
    try:
        with open(plotly_path, 'r') as f:
            plot_data = json.load(f)
        return jsonify(plot_data)
    except Exception as e:
        print(f"Error reading plot file: {str(e)}")
        return jsonify({"error": f"Error reading plot data: {str(e)}"}), 500

@app.route('/test/stage/<stage_num>')
def test_stage(stage_num):
    """Test endpoint for specific stage plot data"""
    # Define the experiment name
    experiment_name = "25_02_28 14_02_06 Exp 011_Blak_Silcotek_New_SiO2_TC_QRZ"
    
    # Get plot type from query parameters (default to 'temperature')
    plot_type = request.args.get('type', 'temperature')
    
    # Map of plot types to filenames
    plot_type_map = {
        'temperature': f"stage_{stage_num}_temp_plotly.json",
        'multipoint': f"stage_{stage_num}_multipoint_temp_plotly.json",
        'saturator': f"stage_{stage_num}_saturator_temp_plotly.json",
        'pressure': f"stage_{stage_num}_pressure_plotly.json",
        'flow': f"stage_{stage_num}_flow_plotly.json",
        'outlet': f"stage_{stage_num}_outlet_plotly.json"
    }
    
    # Check if the requested plot type is valid
    if plot_type not in plot_type_map:
        return jsonify({"error": f"Invalid plot type: {plot_type}", "available_types": list(plot_type_map.keys())}), 400
    
    # Get the filename for the requested plot type
    filename = plot_type_map[plot_type]
    
    # Check for stage plotly file
    stage_dir = os.path.join("reports", experiment_name, f"stage_{stage_num}")
    plotly_path = os.path.join(stage_dir, filename)
    
    print(f"Looking for stage plot file at: {plotly_path}")
    print(f"File exists: {os.path.exists(plotly_path)}")
    
    if not os.path.exists(plotly_path):
        return jsonify({"error": f"Stage {stage_num} plot data not found"}), 404
    
    try:
        with open(plotly_path, 'r') as f:
            plot_data = json.load(f)
        return jsonify(plot_data)
    except Exception as e:
        print(f"Error reading stage plot file: {str(e)}")
        return jsonify({"error": f"Error reading stage plot data: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8082, debug=True) 