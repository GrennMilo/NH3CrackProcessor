#!/usr/bin/env python
"""
NH3 Cracking Processor and Visualizer
-------------------------------------
Flask web application for processing and visualizing NH3 cracking experimental data.
"""
import os
import sys
import glob
import json
import traceback
import urllib.parse
from datetime import datetime
from pathlib import Path
from flask import Flask, render_template, request, jsonify, send_from_directory, redirect, url_for
import logging
from werkzeug.utils import secure_filename

# Import the processor class
from Processors.Main_Web_ProcessorNH3Crack import ExperimentalDataProcessor

app = Flask(__name__)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('app.log')
    ]
)
logger = logging.getLogger(__name__)

# Configuration
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['REPORTS_FOLDER'] = 'reports'
app.config['MAX_CONTENT_LENGTH'] = 300 * 1024 * 1024  # 300 MB limit
app.config['ALLOWED_EXTENSIONS'] = {'txt'}

# Ensure folders exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['REPORTS_FOLDER'], exist_ok=True)

# Create static folder if it doesn't exist
os.makedirs('static', exist_ok=True)

# Helper to check allowed file extensions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

# Helper to get all processed experiments
def get_experiments():
    """Get all processed experiments from Reports folder"""
    experiments = []
    
    try:
        # List all experiment directories
        for item in os.listdir(app.config['REPORTS_FOLDER']):
            exp_dir = os.path.join(app.config['REPORTS_FOLDER'], item)
            if os.path.isdir(exp_dir):
                try:
                    # Attempt to load experiment summary
                    summary_path = os.path.join(exp_dir, "experiment_summary.json")
                    summary = None
                    
                    if os.path.exists(summary_path):
                        try:
                            with open(summary_path, 'r') as f:
                                summary = json.load(f)
                        except Exception as e:
                            app.logger.error(f"Error loading summary for {item}: {e}")
                    
                    # Get stage count from directory structure
                    stage_count = 0
                    if summary and 'metadata' in summary and 'stage_numbers' in summary['metadata']:
                        stage_count = len(summary['metadata']['stage_numbers'])
                    else:
                        # Count stage subdirectories
                        stage_dirs = glob.glob(os.path.join(exp_dir, "stage_*"))
                        stage_count = len(stage_dirs)
                    
                    # Add experiment to list
                    experiments.append({
                        'name': item,
                        'summary': summary,
                        'stages': stage_count
                    })
                except Exception as e:
                    app.logger.error(f"Error processing experiment {item}: {e}")
                    # Add experiment with error info
                    experiments.append({
                        'name': item,
                        'summary': None,
                        'stages': 0,
                        'error': str(e)
                    })
    except Exception as e:
        app.logger.error(f"Error in get_experiments: {e}")
        return []
    
    # Sort by name
    experiments.sort(key=lambda x: x['name'])
    return experiments

# Helper to get experiment directory
def get_experiment_dir(experiment_name):
    """Get the directory path for an experiment"""
    return os.path.join(app.config['REPORTS_FOLDER'], experiment_name)

# Helper to get single experiment
def get_experiment_data(experiment_name):
    """Get data for a specific experiment"""
    try:
        exp_dir = os.path.join(app.config['REPORTS_FOLDER'], experiment_name)
        if not os.path.exists(exp_dir):
            return None
        
        # Attempt to load experiment summary
        summary_path = os.path.join(exp_dir, "experiment_summary.json")
        summary = None
        
        if os.path.exists(summary_path):
            try:
                with open(summary_path, 'r') as f:
                    summary = json.load(f)
            except Exception as e:
                app.logger.error(f"Error loading summary for {experiment_name}: {e}")
        
        # Get stage information
        stages = []
        stage_dirs = sorted(glob.glob(os.path.join(exp_dir, "stage_*")))
        
        for stage_dir in stage_dirs:
            stage_num = os.path.basename(stage_dir).split('_')[1]
            try:
                stage_num = int(stage_num)
            except ValueError:
                continue
                
            # Check for stage plotly data
            plotly_path = os.path.join(stage_dir, f"stage_{stage_num}_plotly.json")
            has_plotly = os.path.exists(plotly_path)
            
            stages.append({
                'number': stage_num,
                'has_plotly': has_plotly
            })
        
        # Add stage information from summary if available
        if summary and 'stages_info' in summary:
            for stage_num, stage_info in summary['stages_info'].items():
                for stage in stages:
                    if str(stage['number']) == str(stage_num):
                        stage.update(stage_info)
        
        # Sort stages by number
        stages.sort(key=lambda x: x['number'])
        
        return {
            'name': experiment_name,
            'summary': summary,
            'stages': stages
        }
    except Exception as e:
        app.logger.error(f"Error in get_experiment_data for {experiment_name}: {e}")
        return None

# Routes
@app.route('/')
def index():
    """Main page with list of experiments"""
    try:
        experiments = get_experiments()
        return render_template('index.html', experiments=experiments)
    except Exception as e:
        app.logger.error(f"Error in index route: {e}")
        error_details = traceback.format_exc()
        return render_template('error.html', message=f"Error loading experiments: {str(e)}", details=error_details)

@app.route('/experiment/<experiment_name>')
def experiment(experiment_name):
    """View a specific experiment"""
    try:
        # URL decode the experiment name
        decoded_name = urllib.parse.unquote(experiment_name)
        
        # Get experiment data
        experiment_data = get_experiment_data(decoded_name)
        
        if not experiment_data:
            return render_template('error.html', message=f"Experiment '{decoded_name}' not found.")
        
        return render_template('experiment.html', experiment=experiment_data)
    except Exception as e:
        app.logger.error(f"Error in experiment route: {e}")
        error_details = traceback.format_exc()
        return render_template('error.html', message=f"Error viewing experiment: {str(e)}", details=error_details)

@app.route('/static/<path:path>')
def serve_static(path):
    """Serve static files"""
    return send_from_directory('static', path)

# API Routes
@app.route('/api/experiments')
def api_experiments():
    """API endpoint to get all experiments"""
    try:
        experiments = get_experiments()
        return jsonify(experiments)
    except Exception as e:
        app.logger.error(f"Error in api_experiments: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/experiment/<experiment_name>/overall')
def api_experiment_overall(experiment_name):
    """API endpoint for overall experiment plot data"""
    try:
        # URL decode the experiment name
        decoded_name = urllib.parse.unquote(experiment_name)
        app.logger.info(f"API request for experiment overall plot: {decoded_name}, type: {request.args.get('type', 'temperature')}")
        
        # Get plot type from query parameters (default to 'temperature')
        plot_type = request.args.get('type', 'temperature')
        
        # Map of plot types to filenames
        plot_type_map = {
            'temperature': f"{decoded_name}_temp_plotly_data.json",
            'multipoint': f"{decoded_name}_multipoint_temp_plotly_data.json",
            'saturator': f"{decoded_name}_saturator_temp_plotly_data.json",
            'pressure': f"{decoded_name}_pressure_plotly_data.json",
            'flow': f"{decoded_name}_flow_plotly_data.json",
            'outlet': f"{decoded_name}_outlet_plotly_data.json"
        }
        
        # Check if the requested plot type is valid
        if plot_type not in plot_type_map:
            app.logger.warning(f"Invalid plot type requested: {plot_type}")
            return jsonify({"error": f"Invalid plot type: {plot_type}", "available_types": list(plot_type_map.keys())}), 400
        
        # Get the filename for the requested plot type
        filename = plot_type_map[plot_type]
        
        # Check for overall plotly file
        exp_dir = os.path.join(app.config['REPORTS_FOLDER'], decoded_name)
        plotly_path = os.path.join(exp_dir, filename)
        
        app.logger.info(f"Looking for plot file at: {plotly_path}")
        app.logger.info(f"File exists: {os.path.exists(plotly_path)}")
        app.logger.info(f"Absolute path: {os.path.abspath(plotly_path)}")
        
        # Fall back to legacy filename if the new one doesn't exist
        if not os.path.exists(plotly_path) and plot_type == 'temperature':
            legacy_path = os.path.join(exp_dir, f"{decoded_name}_plotly_data.json")
            app.logger.info(f"Checking legacy path: {legacy_path}")
            app.logger.info(f"Legacy file exists: {os.path.exists(legacy_path)}")
            app.logger.info(f"Absolute legacy path: {os.path.abspath(legacy_path)}")
            if os.path.exists(legacy_path):
                plotly_path = legacy_path
                logger.info(f"Using legacy plot file: {legacy_path}")
        
        if not os.path.exists(plotly_path):
            # If the specific plot doesn't exist, list available plots
            available_plots = []
            for plot_key, plot_name in plot_type_map.items():
                test_path = os.path.join(exp_dir, plot_name)
                if os.path.exists(test_path):
                    available_plots.append(plot_key)
            
            # Also check for legacy plot files
            legacy_path = os.path.join(exp_dir, f"{decoded_name}_plotly_data.json")
            if os.path.exists(legacy_path) and 'temperature' not in available_plots:
                available_plots.append('temperature')
            
            if not available_plots:
                logger.warning(f"No plot data found for experiment {decoded_name}")
                return jsonify({"error": "No plot data found. Try regenerating visualizations."}), 404
            else:
                logger.info(f"Plot type '{plot_type}' not found for {decoded_name}, available types: {available_plots}")
                return jsonify({
                    "error": f"Plot type '{plot_type}' not found",
                    "available_types": available_plots
                }), 404
        
        with open(plotly_path, 'r') as f:
            plot_data = json.load(f)
        
        return jsonify(plot_data)
    except Exception as e:
        logger.error(f"Error in api_experiment_overall: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/experiment/<experiment_name>/stage/<stage_num>')
def api_experiment_stage(experiment_name, stage_num):
    """API endpoint for specific stage plot data"""
    try:
        # URL decode the experiment name
        decoded_name = urllib.parse.unquote(experiment_name)
        app.logger.info(f"API request for stage plot: {decoded_name}, stage: {stage_num}, type: {request.args.get('type', 'temperature')}")
        
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
            app.logger.warning(f"Invalid stage plot type requested: {plot_type}")
            return jsonify({"error": f"Invalid plot type: {plot_type}", "available_types": list(plot_type_map.keys())}), 400
        
        # Get the filename for the requested plot type
        filename = plot_type_map[plot_type]
        
        # Check for stage plotly file
        stage_dir = os.path.join(app.config['REPORTS_FOLDER'], decoded_name, f"stage_{stage_num}")
        plotly_path = os.path.join(stage_dir, filename)
        
        app.logger.info(f"Looking for stage plot file at: {plotly_path}")
        app.logger.info(f"Stage plot file exists: {os.path.exists(plotly_path)}")
        app.logger.info(f"Absolute stage path: {os.path.abspath(plotly_path)}")
        
        # Fall back to legacy filename if the new one doesn't exist
        if not os.path.exists(plotly_path) and plot_type == 'temperature':
            legacy_path = os.path.join(stage_dir, f"stage_{stage_num}_plotly.json")
            app.logger.info(f"Checking stage legacy path: {legacy_path}")
            app.logger.info(f"Stage legacy file exists: {os.path.exists(legacy_path)}")
            app.logger.info(f"Absolute stage legacy path: {os.path.abspath(legacy_path)}")
            if os.path.exists(legacy_path):
                plotly_path = legacy_path
                logger.info(f"Using legacy plot file: {legacy_path}")
        
        if not os.path.exists(plotly_path):
            # If the specific plot doesn't exist, list available plots
            available_plots = []
            for plot_key, plot_name in plot_type_map.items():
                test_path = os.path.join(stage_dir, plot_name)
                if os.path.exists(test_path):
                    available_plots.append(plot_key)
            
            # Also check for legacy plot files
            legacy_path = os.path.join(stage_dir, f"stage_{stage_num}_plotly.json")
            if os.path.exists(legacy_path) and 'temperature' not in available_plots:
                available_plots.append('temperature')
            
            if not available_plots:
                logger.warning(f"No plot data found for stage {stage_num} in experiment {decoded_name}")
                return jsonify({"error": f"Stage {stage_num} plot data not found. Try regenerating visualizations."}), 404
            else:
                logger.info(f"Plot type '{plot_type}' not found for stage {stage_num}, available types: {available_plots}")
                return jsonify({
                    "error": f"Plot type '{plot_type}' not found for stage {stage_num}",
                    "available_types": available_plots
                }), 404
        
        with open(plotly_path, 'r') as f:
            plot_data = json.load(f)
        
        return jsonify(plot_data)
    except Exception as e:
        logger.error(f"Error in api_experiment_stage: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/process/<experiment_name>')
def api_process_experiment(experiment_name):
    """API endpoint to process a single experiment"""
    try:
        # URL decode the experiment name
        decoded_name = urllib.parse.unquote(experiment_name)
        
        # Initialize processor
        processor = ExperimentalDataProcessor(
            input_folder=app.config['UPLOAD_FOLDER'],
            output_folder=app.config['REPORTS_FOLDER']
        )
        
        # Find file(s) for this experiment in uploads folder
        files = glob.glob(os.path.join(app.config['UPLOAD_FOLDER'], f"{decoded_name}*.txt"))
        
        if not files:
            return jsonify({
                "success": False,
                "message": f"No files found for experiment '{decoded_name}' in uploads folder"
            })
        
        # Process each file
        processed_files = []
        for file_path in files:
            filename = os.path.basename(file_path)
            try:
                processor.process_file(filename)
                processed_files.append(filename)
            except Exception as e:
                app.logger.error(f"Error processing {filename}: {str(e)}")
        
        if not processed_files:
            return jsonify({
                "success": False,
                "message": f"Failed to process any files for experiment '{decoded_name}'"
            })
        
        return jsonify({
            "success": True,
            "message": f"Processed {len(processed_files)} files for experiment '{decoded_name}'",
            "processed_files": processed_files
        })
        
    except Exception as e:
        app.logger.error(f"Error in api_process_experiment: {str(e)}")
        return jsonify({
            "success": False,
            "message": f"Error: {str(e)}",
            "traceback": traceback.format_exc()
        })

@app.route('/api/process-all')
def api_process_all_experiments():
    """API endpoint to process all experiments"""
    try:
        # Initialize processor
        processor = ExperimentalDataProcessor(
            input_folder=app.config['UPLOAD_FOLDER'],
            output_folder=app.config['REPORTS_FOLDER']
        )
        
        # Get all text files in uploads folder
        files = glob.glob(os.path.join(app.config['UPLOAD_FOLDER'], "*.txt"))
        
        if not files:
            return jsonify({
                "success": False,
                "message": "No files found in uploads folder"
            })
        
        # Process each file
        processed_files = []
        errors = []
        
        for file_path in files:
            filename = os.path.basename(file_path)
            try:
                processor.process_file(filename)
                processed_files.append(filename)
            except Exception as e:
                app.logger.error(f"Error processing {filename}: {str(e)}")
                errors.append({
                    "file": filename,
                    "error": str(e)
                })
        
        return jsonify({
            "success": True,
            "message": f"Processed {len(processed_files)} files with {len(errors)} errors",
            "processed_files": processed_files,
            "errors": errors
        })
        
    except Exception as e:
        app.logger.error(f"Error in api_process_all_experiments: {str(e)}")
        return jsonify({
            "success": False,
            "message": f"Error: {str(e)}",
            "traceback": traceback.format_exc()
        })

@app.route('/api/visualize/<experiment_name>', methods=['GET'])
def api_visualize_experiment(experiment_name):
    """API endpoint to visualize an experiment and create plotly JSON files."""
    try:
        experiment_name = urllib.parse.unquote(experiment_name)
        logger.info(f"Visualizing experiment: {experiment_name}")
        
        experiment_dir = get_experiment_dir(experiment_name)
        if not os.path.exists(experiment_dir):
            return jsonify({'success': False, 'message': 'Experiment not found'}), 404
        
        # Get stage folders
        stage_folders = []
        for folder in os.listdir(experiment_dir):
            if folder.startswith('stage_') and os.path.isdir(os.path.join(experiment_dir, folder)):
                stage_folders.append(folder)
        
        if not stage_folders:
            return jsonify({'success': False, 'message': 'No stage data found for this experiment'}), 404
        
        # Parse stage numbers and sort
        stage_numbers = []
        for folder in stage_folders:
            try:
                stage_num = int(folder.replace('stage_', ''))
                stage_numbers.append(stage_num)
            except ValueError:
                continue
        
        stage_numbers.sort()
        
        # Import the create_stage_plotly_json and create_plotly_json functions directly
        # to avoid circular import issues
        processor = ExperimentalDataProcessor(
            input_folder=app.config['UPLOAD_FOLDER'],
            output_folder=app.config['REPORTS_FOLDER']
        )
        
        # Create JSON files for each stage
        for stage_num in stage_numbers:
            stage_dir = os.path.join(experiment_dir, f"stage_{stage_num}")
            stage_data_file = os.path.join(stage_dir, f"stage_{stage_num}_data.json")
            
            if os.path.exists(stage_data_file):
                try:
                    # Load the stage data
                    with open(stage_data_file, 'r') as f:
                        stage_data = json.load(f)
                    
                    # Convert JSON to DataFrame
                    stage_df = pd.DataFrame(stage_data)
                    
                    # Generate the multiple plot files for this stage
                    logger.info(f"Generating plots for stage {stage_num}")
                    processor.create_stage_plotly_json(
                        stage_df, 
                        int(stage_num), 
                        experiment_name, 
                        stage_dir
                    )
                except Exception as e:
                    logger.error(f"Error generating plots for stage {stage_num}: {str(e)}")
            else:
                logger.warning(f"Stage data file not found for stage {stage_num}")
        
        # Create overall plotly JSON files
        logger.info("Generating overall plots for all stages")
        
        # Load all stage data
        stages_data = {}
        for stage_num in stage_numbers:
            stage_data_file = os.path.join(experiment_dir, f"stage_{stage_num}", f"stage_{stage_num}_data.json")
            if os.path.exists(stage_data_file):
                try:
                    with open(stage_data_file, 'r') as f:
                        stage_data = json.load(f)
                    stages_data[stage_num] = pd.DataFrame(stage_data)
                except Exception as e:
                    logger.error(f"Error loading data for stage {stage_num}: {str(e)}")
        
        if stages_data:
            # Generate overall plots
            processor.create_plotly_json(
                stages_data,
                experiment_name,
                datetime.now().strftime("%Y%m%d_%H%M%S"),
                experiment_dir
            )
        
        return jsonify({
            'success': True, 
            'message': f'Visualizations created for {len(stage_numbers)} stages'
        })
    
    except Exception as e:
        logger.exception(f"Error visualizing experiment: {str(e)}")
        return jsonify({'success': False, 'message': f'Error: {str(e)}'}), 500

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    """Upload a file to the uploads folder"""
    if request.method == 'POST':
        # Check if the post request has the file part
        if 'file' not in request.files:
            return render_template('error.html', message="No file part")
            
        file = request.files['file']
        
        # If user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            return render_template('error.html', message="No selected file")
            
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('index'))
        else:
            return render_template('error.html', message="File type not allowed")
    
    return render_template('upload.html')

# Run the application
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080) 