# NH3 Cracking Processor and Visualizer

![NH3 Cracking](https://img.shields.io/badge/NH3-Cracking-blue)
![Python](https://img.shields.io/badge/Python-3.8%2B-brightgreen)
![Flask](https://img.shields.io/badge/Flask-2.0%2B-red)
![Plotly](https://img.shields.io/badge/Plotly-5.0%2B-orange)
![License](https://img.shields.io/badge/License-MIT-green)

A comprehensive web application for processing, analyzing, and visualizing NH3 (ammonia) cracking experimental data. This tool provides a complete pipeline from raw experimental data to interactive visualizations, with specialized views for different data categories.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Usage](#usage)
  - [Web Interface](#web-interface)
  - [Command Line Interface](#command-line-interface)
  - [API Reference](#api-reference)
- [Data Processing](#data-processing)
  - [Input Data Format](#input-data-format)
  - [Processing Pipeline](#processing-pipeline)
  - [Time Vector Handling](#time-vector-handling)
  - [Stage Detection](#stage-detection)
  - [Data Interpolation](#data-interpolation)
- [Visualization](#visualization)
  - [Plotly Integration](#plotly-integration)
  - [Data Categories](#data-categories)
  - [Visualization Types](#visualization-types)
  - [Customization Options](#customization-options)
- [Directory Structure](#directory-structure)
- [Output Data Structure](#output-data-structure)
- [Technical Details](#technical-details)
  - [Dependencies](#dependencies)
  - [JSON to Plotly Visualization Handling](#json-to-plotly-visualization-handling)
  - [Core Components](#core-components)
  - [Data Flow](#data-flow)
- [Examples](#examples)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

## Overview

NH3 Cracking Processor and Visualizer is a specialized tool designed for scientists and engineers working with ammonia cracking experiments. It automates the processing of raw experimental data, detects different experimental stages, performs necessary data transformations, and generates interactive visualizations for analysis.

The application is built with Python using Flask for the web framework, Pandas and NumPy for data processing, and Plotly for interactive data visualization. It provides both a user-friendly web interface and programmatic access through an API.

## Features

- **Automated Data Processing**: Process experimental data from tab-separated text files with a single click
- **Multi-Encoding Support**: Automatically handles files with different text encodings (UTF-8, Latin1, CP1252, ISO-8859-1)
- **Intelligent DateTime Parsing**: Handles multiple date-time formats automatically
- **Stage Detection**: Automatically detect and separate experimental stages based on the Stage column
- **Data Interpolation**: Perform cubic interpolation for a consistent time vector with 1-minute intervals
- **Missing Data Handling**: Gracefully handles missing or incomplete data
- **Category-Based Analysis**: Automatically organizes measurements into logical categories (temperature, pressure, flow, etc.)
- **Interactive Visualization**: Generate Plotly-based interactive visualizations with zoom, pan, and hover capabilities
- **Dark-Mode Optimized UI**: Dark-themed interface with high-contrast plots for better data visibility
- **Specialized Plot Categories**:
  - Temperature measurements
  - Multipoint temperature measurements
  - Saturator temperature
  - Pressure measurements
  - Flow measurements
  - Outlet stream composition
- **Web Interface**: Easy-to-use web interface for data management and visualization
- **RESTful API**: Programmatic access to all functionality
- **Batch Processing**: Process multiple files at once
- **Export Options**: Export data in CSV and JSON formats
- **Responsive Design**: Works on desktop and tablet devices

## Installation

### Requirements

- Python 3.8 or higher
- pip (Python package installer)
- Git (optional, for cloning the repository)

### Dependencies

The application requires several Python libraries:

- **Flask**: Web framework
- **Pandas**: Data manipulation and analysis
- **NumPy**: Numerical computing
- **SciPy**: Scientific computing (used for interpolation)
- **Plotly**: Interactive visualizations
- **Werkzeug**: WSGI utility library for Python
- **Jinja2**: Template engine
- **MarkupSafe**: Escapes characters so text is safe to use in HTML and XML
- **Click**: Command line interface creation kit
- **itsdangerous**: Various helpers to pass data to untrusted environments securely
- **Path**: Path manipulation utilities

### Installation Steps

1. Clone this repository:
```bash
git clone https://github.com/GrennMilo/NH3CrackProcessor.git
cd NH3CrackProcessor
```

2. Create and activate a virtual environment (optional but recommended):
```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

3. Install the required dependencies:
```bash
pip install -r requirements.txt
```

If the requirements.txt file is not available, you can create it with:

```bash
pip install Flask pandas numpy scipy plotly werkzeug jinja2 markupsafe click itsdangerous pathlib
pip freeze > requirements.txt
```

4. Create necessary directories (these will be created automatically when running the app, but you can create them manually):
```bash
mkdir -p uploads Reports
```

## Quick Start

To quickly start the application:

```bash
python app.py
```

This will start the Flask web server on http://localhost:8085 by default. You can then access the web interface by opening this URL in your web browser.

For processing all files in the uploads folder at once:

```bash
python process_all.py
```

For a one-line command to process a specific file and immediately run the web interface:

```bash
python quick_start.py --file your_data_file.txt
```

## Usage

### Web Interface

The NH3 Cracking Processor and Visualizer provides an intuitive web interface for managing experiments.

#### Home Page

The home page displays a list of all processed experiments, with the most recent experiments at the top. For each experiment, you can see:

- Experiment name
- Processing date
- Number of stages
- Quick action buttons

![Home Page](https://via.placeholder.com/800x400?text=NH3+Cracking+Home+Page)

#### Upload Page

The upload page allows you to upload new experimental data files. It supports:

- Drag and drop file upload
- File selection dialog
- Progress indication during upload
- Automatic processing after upload

The application only accepts tab-separated text files (.txt).

#### Experiment Page

The experiment page provides a detailed view of a specific experiment:

- Overall Campaign Data: Shows all measurements across all stages
- DateTime Vector Visualization: Precise time-based visualization
- Specialized Data Categories: Categorized measurements (temperature, pressure, etc.)
- Stage Selection: Individual stage data visualization
- Plot Controls: Customize plot appearance (line/scatter, theme)
- Action Buttons: Process experiment, regenerate visualizations

### Command Line Interface

The application can also be used from the command line.

#### Running the Web Server

```bash
python app.py [--host HOST] [--port PORT] [--debug]
```

Options:
- `--host`: Host to run the server on (default: 0.0.0.0)
- `--port`: Port to run the server on (default: 8085)
- `--debug`: Run in debug mode (default: False)

#### Processing Files

Process a single file:

```bash
python process_file.py --file your_data_file.txt
```

Process all files in the uploads folder:

```bash
python process_all.py
```

### API Reference

The application provides a RESTful API for programmatic access to its functionality.

#### Experiment List

```
GET /api/experiments
```

Returns a list of all processed experiments.

#### Process Experiment

```
GET /api/process/<experiment_name>
```

Processes or reprocesses an experiment.

#### Get Overall Plot Data

```
GET /api/experiment/<experiment_name>/overall
```

Returns the overall plot data for an experiment.

#### Get Category Plot Data

```
GET /api/experiment/<experiment_name>/category/<category>
```

Returns the plot data for a specific category.

#### Get Available Categories

```
GET /api/experiment/<experiment_name>/categories
```

Returns a list of available plot categories for an experiment.

#### Get DateTime Vector Visualization

```
GET /api/experiment/<experiment_name>/datetime
```

Returns the datetime vector visualization data.

#### Get Stage Plot Data

```
GET /api/experiment/<experiment_name>/stage/<stage_num>
```

Returns the plot data for a specific stage.

#### Process All Files

```
GET /api/process-all
```

Processes all files in the uploads folder.

#### Example API Usage with Python

```python
import requests
import json

# Get list of all experiments
response = requests.get("http://localhost:8085/api/experiments")
experiments = response.json()
print(f"Found {len(experiments)} experiments")

# Process a specific experiment
experiment_name = "Exp012_Parameters_R151_2682"
response = requests.get(f"http://localhost:8085/api/process/{experiment_name}")
result = response.json()
print(f"Processing result: {result['message']}")

# Get temperature plot data
response = requests.get(f"http://localhost:8085/api/experiment/{experiment_name}/category/temperature")
plot_data = response.json()

# Save plot data to file
with open(f"{experiment_name}_temperature.json", "w") as f:
    json.dump(plot_data, f, indent=2)
```

## Data Processing

### Input Data Format

The processor expects tab-separated text files with:

- First column: Date/time information in various formats
- Second column: Stage identifier (integer values to identify different experimental stages)
- Remaining columns: Numeric measurement data

Example file format:
```
DateTime            Stage    Temperature    Pressure    Flow
01/05/24 12:34:56    1        450.2        25.3        380.5
01/05/24 12:35:56    1        451.3        25.4        380.2
01/05/24 12:36:56    1        450.8        25.2        380.4
01/05/24 12:37:56    2        460.1        26.0        381.0
01/05/24 12:38:56    2        461.5        26.1        381.2
```

### Processing Pipeline

The data processing pipeline consists of the following steps:

1. **File Reading**: Read the tab-separated file with automatic encoding detection
2. **Time Vector Creation**: Convert datetime strings to a consistent time vector in minutes
3. **Stage Detection**: Identify different experimental stages based on the Stage column
4. **Data Interpolation**: Perform cubic interpolation to create a consistent time grid
5. **Column Mapping**: Analyze and categorize columns based on their content
6. **Data Export**: Export processed data in CSV and JSON formats
7. **Visualization Generation**: Create interactive visualizations for different data views

Here's a code example showing the core processing pipeline:

```python
from Main_Web_ProcessorNH3Crack import ExperimentalDataProcessor

# Initialize processor
processor = ExperimentalDataProcessor(
    input_folder="uploads",
    output_folder="Reports"
)

# Process a file
processor.process_file("your_data_file.txt")
```

### Time Vector Handling

Time vector handling is a critical aspect of the processing pipeline. The application converts various datetime formats into a consistent relative time vector in minutes. This is done in the `create_time_vector` method:

```python
def create_time_vector(self, df):
    # Assume first column is datetime
    datetime_col = df.columns[0]
    
    # Try different datetime formats
    date_formats = [
        '%d/%m/%y %H:%M:%S',  # DD/MM/YY HH:MM:SS
        '%Y-%m-%d %H:%M:%S',  # YYYY-MM-DD HH:MM:SS
        '%d/%m/%Y %H:%M:%S',  # DD/MM/YYYY HH:MM:SS
        '%m/%d/%y %H:%M:%S',  # MM/DD/YY HH:MM:SS
        '%m/%d/%Y %H:%M:%S',  # MM/DD/YYYY HH:MM:SS
    ]
    
    # Try to parse datetime using different formats
    for date_format in date_formats:
        try:
            df[datetime_col] = pd.to_datetime(df[datetime_col], format=date_format)
            break
        except ValueError:
            continue
    
    # Create time vector in minutes from start
    start_time = df[datetime_col].min()
    df['Time_Minutes'] = (df[datetime_col] - start_time).dt.total_seconds() / 60
    
    return df
```

If datetime parsing fails, the application creates a sequential time vector as a fallback:

```python
# Fallback: create sequential time vector
df['Time_Minutes'] = np.arange(len(df))
```

### Stage Detection

Experimental stages are detected using the second column (typically named 'Stage'). If this column exists, the data is grouped by stage values:

```python
def slice_by_stages(self, df):
    # Ensure the Stage column exists
    if 'Stage' not in df.columns:
        # Look for stage column in second position (index 1)
        if len(df.columns) > 1:
            stage_col = df.columns[1]
            df.rename(columns={stage_col: 'Stage'}, inplace=True)
        else:
            df['Stage'] = 1
            return {1: df}
    
    # Group data by stage values
    stages = {}
    stage_groups = df.groupby('Stage')
    
    for stage_num, stage_data in stage_groups:
        stages[int(stage_num)] = stage_data.copy()
    
    return stages
```

### Data Interpolation

To ensure a consistent time grid across all measurements, the application performs cubic interpolation for all numeric columns. This is done in the `perform_interpolation` method:

```python
def perform_interpolation(self, df, target_interval_minutes=1):
    # Create target time vector with 1-minute intervals
    time_min = df['Time_Minutes'].min()
    time_max = df['Time_Minutes'].max()
    target_time = np.arange(time_min, time_max + target_interval_minutes, target_interval_minutes)
    
    # Create new dataframe for interpolated data
    interpolated_df = pd.DataFrame({'Time_Minutes': target_time})
    
    # Get numeric columns (excluding time and stage columns)
    numeric_columns = df.select_dtypes(include=[np.number]).columns.tolist()
    exclude_cols = ['Time_Minutes', 'Stage']
    numeric_columns = [col for col in numeric_columns if col not in exclude_cols]
    
    # Interpolate each numeric column
    for col in numeric_columns:
        # Remove NaN values for interpolation
        mask = ~(df['Time_Minutes'].isna() | df[col].isna())
        if mask.sum() > 3:  # Need at least 4 points for cubic interpolation
            x = df.loc[mask, 'Time_Minutes'].values
            y = df.loc[mask, col].values
            
            # Create interpolation function
            f = interp1d(x, y, kind='cubic', bounds_error=False, fill_value='extrapolate')
            interpolated_df[col] = f(target_time)
        else:
            interpolated_df[col] = np.nan
    
    # Handle Stage column separately (use nearest neighbor)
    if 'Stage' in df.columns:
        mask = ~(df['Time_Minutes'].isna() | df['Stage'].isna())
        if mask.sum() > 0:
            x = df.loc[mask, 'Time_Minutes'].values
            y = df.loc[mask, 'Stage'].values
            f_stage = interp1d(x, y, kind='nearest', bounds_error=False, fill_value='extrapolate')
            interpolated_df['Stage'] = f_stage(target_time).astype(int)
        else:
            interpolated_df['Stage'] = 0
    
    return interpolated_df
```

## Visualization

### Plotly Integration

The application uses Plotly to create interactive visualizations. Plotly data is generated in JSON format and served to the frontend through the API. The JSON format includes:

- `data`: Array of trace objects (each representing a data series)
- `layout`: Object defining the plot layout, axes, labels, etc.

Here's a simplified example of how Plotly data is generated:

```python
def create_stage_plotly_json(self, stage_df, stage_num, base_filename, output_path):
    # Create title
    title = f'Stage {stage_num} - {base_filename}'
    
    # Get numeric columns (excluding Time_Minutes and Stage)
    numeric_cols = stage_df.select_dtypes(include=[np.number]).columns.tolist()
    exclude_cols = ['Time_Minutes', 'Stage', 'Stage_ID']
    plot_cols = [col for col in numeric_cols if col not in exclude_cols]
    
    # Create traces
    traces = []
    for col in plot_cols:
        trace = {
            'x': stage_df['Time_Minutes'].tolist(),
            'y': stage_df[col].tolist(),
            'type': 'scatter',
            'mode': 'lines',
            'name': col
        }
        traces.append(trace)
    
    # Create layout
    layout = {
        'title': title,
        'xaxis': {'title': 'Time (minutes)'},
        'yaxis': {'title': 'Values'},
        'hovermode': 'closest',
        'template': 'plotly_dark',
        'paper_bgcolor': '#1e1e1e',
        'plot_bgcolor': '#2d2d2d',
        'font': {'color': '#e0e0e0'}
    }
    
    # Create Plotly data
    plotly_data = {
        'data': traces,
        'layout': layout
    }
    
    # Save to file
    with open(output_path, 'w') as f:
        json.dump(plotly_data, f, indent=2)
```

### Data Categories

The application categorizes measurements into logical groups:

- **Temperature**: Main temperature measurements (R1/2 T read, Saturator T read, etc.)
- **Multipoint Temperature**: Temperature measurements at multiple points
- **Saturator Temperature**: Specialized view for saturator temperature
- **Pressure**: Pressure measurements across different parts of the system
- **Flow**: Flow rates and related measurements
- **Outlet Composition**: Composition measurements of the outlet stream

These categories are defined in the `create_category_plotly_jsons` method:

```python
def create_category_plotly_jsons(self, stages, base_filename, timestamp, exp_dir):
    # Define data categories with their column patterns
    categories = {
        'temperature': {
            'title': 'Temperature Measurements',
            'y_axis_title': 'Temperature (°C)',
            'columns': [
                "R1/2 T set [°C]", 
                "R1/2 T read [°C]", 
                "R1/2 T power [%]", 
                "Saturator T read [°C]"
            ]
        },
        'pressure': {
            'title': 'Pressure Measurements',
            'y_axis_title': 'Pressure (bar)',
            'columns': [
                "Pressure SETPOINT [bar]", 
                "Pressure PIC [bar]", 
                "Pressure reading line [bar]", 
                # ... other pressure columns
            ]
        },
        # ... other categories
    }
```

### Visualization Types

The application provides several types of visualizations:

1. **Overall Plot**: Shows all measurements across all stages
2. **Category Plots**: Shows measurements grouped by category
3. **Stage Plots**: Shows all measurements for a specific stage
4. **DateTime Vector Visualization**: Shows measurements with precise time positioning

Each visualization type can be customized in the web interface.

### Customization Options

The web interface provides several options for customizing visualizations:

- **Plot Type**: Line or scatter
- **Theme**: Dark or light
- **Stage Visibility**: Show all stages or specific stages only
- **X-Axis Type**: Relative time or date/time

## Directory Structure

The NH3 Cracking Processor and Visualizer project follows a well-organized directory structure:

```
NH3CrackProcessor/
├── app.py                  # Main Flask application entry point
├── process_all.py          # Script to process all experiments in the Uploads folder
├── requirements.txt        # Python dependencies
├── ReadMe.md               # This documentation file
├── .gitignore              # Git ignore configuration
├── Processors/             # Data processing modules and utilities
│   ├── Main_Web_ProcessorNH3Crack.py   # Core data processing implementation
│   ├── fix_plots.py                    # Utility to fix or regenerate plots
│   ├── test_paths.py                   # Utility to test file paths
│   ├── test_server.py                  # Server testing utilities
│   ├── setup_and_run.py                # Setup and deployment utilities
│   ├── run.py                          # Runner script
│   ├── test_connection.py              # Network connection test
│   ├── basic_app.py                    # Simplified Flask app for testing
│   ├── debug_app.py                    # Debug version of the app
│   └── quick_start.py                  # Quick start utility
├── Reports/                # Generated reports and visualizations
│   └── [experiment_name]/  # Each experiment has its own directory
│       ├── [experiment_name]_temp_plotly_data.json      # Temperature plot data
│       ├── [experiment_name]_multipoint_plotly_data.json # Multipoint temperature data
│       ├── [experiment_name]_saturator_plotly_data.json # Saturator temperature data
│       ├── [experiment_name]_pressure_plotly_data.json  # Pressure measurements data
│       ├── [experiment_name]_flow_plotly_data.json      # Flow measurements data
│       ├── [experiment_name]_outlet_plotly_data.json    # Outlet composition data
│       └── stages/         # Stage-specific plots
│           └── stage_[n]/  # Data for each experimental stage
│               ├── stage_[n]_temp_plotly_data.json
│               ├── stage_[n]_multipoint_plotly_data.json
│               └── ...     # Other plot types for this stage
├── static/                 # Static web assets
│   ├── css/                # Stylesheet files
│   ├── js/                 # JavaScript files
│   └── images/             # Image assets
├── templates/              # Jinja2 HTML templates
│   ├── base.html           # Base template with common elements
│   ├── index.html          # Home page template
│   ├── upload.html         # File upload page
│   ├── experiment.html     # Experiment details page
│   └── error.html          # Error page template
├── Uploads/                # Directory for raw experimental data files
│   └── [data_files].txt    # Raw tab-separated experimental data files
└── logs/                   # Application logs
    ├── app.log             # Main application log
    └── app_debug.log       # Debug-level logging
```

### Key Components

1. **app.py**: The main Flask application entry point that defines routes, handles requests, and manages the web interface.

2. **Processors/**: Contains all the data processing logic:
   - **Main_Web_ProcessorNH3Crack.py**: The core implementation of the `ExperimentalDataProcessor` class that handles data loading, processing, and visualization generation.
   - **fix_plots.py**: Utility script to fix or regenerate plots for specific experiments.
   - Various testing and utility scripts to assist with development and troubleshooting.

3. **Reports/**: Contains the processed data and generated visualizations:
   - Each experiment has its own directory named after the experiment.
   - Plot data is stored as JSON files for different categories (temperature, pressure, flow, etc.).
   - Stage-specific data is organized in subdirectories.

4. **static/** and **templates/**: Standard Flask application structure for web assets and HTML templates.

5. **Uploads/**: Directory for raw experimental data files in tab-separated text format.

6. **logs/**: Contains application logs for monitoring and troubleshooting.

This organization separates concerns and follows the principle of having a clear place for each type of file, making the project maintainable and scalable.

## Output Data Structure

The processor generates a hierarchical folder structure to organize the processed data:

```
Reports/
└── ExperimentName/               # One folder per experiment
    ├── experiment_summary.json   # Overall experiment metadata
    ├── ExperimentName_complete.csv   # All stages combined
    ├── ExperimentName_all_stages.json # All data in JSON format
    ├── ExperimentName_plotly_data.json # Visualization data for all stages
    ├── ExperimentName_temperature_plotly.json # Temperature category plot
    ├── ExperimentName_pressure_plotly.json # Pressure category plot
    ├── ExperimentName_flow_plotly.json # Flow category plot
    ├── ExperimentName_outlet_composition_plotly.json # Composition category plot
    ├── ExperimentName_datetime_vector.json # DateTime vector visualization
    ├── stage_1/                  # One subfolder per stage
    │   ├── stage_1_data.csv      # CSV data for stage 1
    │   ├── stage_1_data.json     # JSON data for stage 1
    │   └── stage_1_plotly.json   # Visualization data for stage 1
    ├── stage_2/
    │   ├── stage_2_data.csv
    │   ├── stage_2_data.json
    │   └── stage_2_plotly.json
    └── ...
```

### Experiment Summary JSON

The `experiment_summary.json` file contains metadata about the experiment, including:

```json
{
  "metadata": {
    "processed_at": "2023-04-01T12:34:56.789012",
    "total_stages": 3,
    "stage_numbers": [1, 2, 3],
    "base_filename": "Exp012_Parameters_R151_2682"
  },
  "column_mapping": {
    "DateTime": {
      "index": 0,
      "dtype": "datetime64[ns]",
      "non_null_count": 500,
      "null_count": 0
    },
    "Stage": {
      "index": 1,
      "dtype": "int64",
      "non_null_count": 500,
      "null_count": 0
    },
    "R1/2 T read [°C]": {
      "index": 2,
      "dtype": "float64",
      "non_null_count": 500,
      "null_count": 0,
      "min": 450.2,
      "max": 550.5,
      "mean": 500.3,
      "std": 25.4
    },
    // ... other columns
  },
  "stages_info": {
    "1": {
      "row_count": 180,
      "time_range": {
        "start": 0.0,
        "end": 179.0,
        "duration": 179.0
      }
    },
    "2": {
      "row_count": 320,
      "time_range": {
        "start": 180.0,
        "end": 499.0,
        "duration": 319.0
      }
    }
    // ... other stages
  }
}
```

### Stage Data JSON

Each stage folder contains a `stage_X_data.json` file with the data for that stage:

```json
{
  "DateTime": ["2023-04-01 12:00:00", "2023-04-01 12:01:00", "..."],
  "Stage": [1, 1, 1, "..."],
  "Time_Minutes": [0.0, 1.0, 2.0, "..."],
  "R1/2 T read [°C]": [450.2, 451.3, 450.8, "..."],
  "Pressure reading line [bar]": [25.3, 25.4, 25.2, "..."],
  "NH3 Actual Flow [Nml/min]": [380.5, 380.2, 380.4, "..."],
  // ... other measurements
}
```

### Plotly JSON Format

The `stage_X_plotly.json` and category plot files use the Plotly JSON format:

```json
{
  "data": [
    {
      "x": [0.0, 1.0, 2.0, "..."],
      "y": [450.2, 451.3, 450.8, "..."],
      "type": "scatter",
      "mode": "lines",
      "name": "R1/2 T read [°C]",
      "line": {"color": "#ff6e6e", "width": 2}
    },
    {
      "x": [0.0, 1.0, 2.0, "..."],
      "y": [25.3, 25.4, 25.2, "..."],
      "type": "scatter",
      "mode": "lines",
      "name": "Pressure reading line [bar]",
      "line": {"color": "#5c9eff", "width": 2}
    },
    // ... other traces
  ],
  "layout": {
    "title": "Stage 1 - Exp012_Parameters_R151_2682",
    "xaxis": {
      "title": "Time (minutes)",
      "gridcolor": "rgba(255, 255, 255, 0.1)"
    },
    "yaxis": {
      "title": "Values",
      "gridcolor": "rgba(255, 255, 255, 0.1)"
    },
    "template": "plotly_dark",
    "paper_bgcolor": "#1e1e1e",
    "plot_bgcolor": "#2d2d2d",
    "font": {"color": "#e0e0e0"},
    "hovermode": "closest",
    "legend": {
      "orientation": "v",
      "bgcolor": "rgba(0,0,0,0.5)",
      "bordercolor": "rgba(255,255,255,0.2)",
      "borderwidth": 1
    }
  }
}
```

This format is used by the frontend to render interactive plots using Plotly.js.

## Technical Details

### Dependencies

The application requires the following Python libraries:

- Flask
- Pandas
- NumPy
- SciPy
- Plotly
- Werkzeug
- Jinja2
- MarkupSafe
- Click
- itsdangerous
- Pathlib

### JSON to Plotly Visualization Handling

The application uses a two-step process to convert processed data to interactive Plotly visualizations:

1. **Backend Processing**: The `ExperimentalDataProcessor` class generates Plotly-compatible JSON files for different views of the data.
2. **Frontend Rendering**: The web interface uses Plotly.js to render these JSON files as interactive visualizations.

#### Backend JSON Generation

The backend generates several types of Plotly JSON files:

1. **Stage Plots**: One plot per experimental stage showing all measurements.
2. **Category Plots**: Specialized plots for different measurement categories.
3. **Overall Plot**: A combined plot showing key measurements across all stages.
4. **DateTime Vector Visualization**: A plot using the exact datetime values for precise time positioning.

The JSON generation is handled by methods like `create_stage_plotly_json`, `_create_category_plot`, and `create_plotly_json`.

#### Frontend Rendering

The frontend loads these JSON files via the API and renders them using Plotly.js. The rendering is handled by JavaScript in the `experiment.html` template:

```javascript
function loadOverallPlot() {
    fetch(`/api/experiment/${experimentName}/overall`)
        .then(response => response.json())
        .then(data => {
            overallData = data;
            updateOverallPlot();
        });
}

function updateOverallPlot() {
    if (!overallData || !overallData.data) return;
    
    // Apply plot type changes
    const plotType = overallPlotType.value;
    const updatedData = overallData.data.map(trace => {
        if (trace.type !== 'scatter') return trace;
        return {
            ...trace,
            mode: plotType === 'line' ? 'lines' : 'markers'
        };
    });
    
    // Apply theme changes
    const theme = overallPlotTheme.value;
    const updatedLayout = {
        ...overallData.layout,
        template: theme
    };
    
    Plotly.react('overall-plot', updatedData, updatedLayout, {responsive: true});
}
```

The frontend allows users to customize the visualizations in real-time, changing plot types, themes, and filtering options without requiring server-side processing.

### Core Components

The application consists of the following core components:

- **ExperimentalDataProcessor**: Handles data processing and visualization generation
- **WebInterface**: Provides the user interface for managing experiments and visualizing data
- **API**: Allows programmatic access to the application's functionality

### Data Flow

The data flow through the application is as follows:

1. **Data Input**: Experimental data files are uploaded to the application
2. **Data Processing**: The data is processed and analyzed using the ExperimentalDataProcessor
3. **Data Visualization**: The processed data is visualized using Plotly
4. **Data Export**: The processed data is exported in CSV and JSON formats

## Examples

### Example 1: Processing a Single File

```bash
python process_file.py --file your_data_file.txt
```

This command processes a single experimental data file and generates the necessary data and visualization files.

### Example 2: Processing All Files in the Uploads Folder

```bash
python process_all.py
```

This command processes all experimental data files in the uploads folder and generates the necessary data and visualization files for each experiment.

### Advanced Examples

#### Extending the Processor with Custom Categories

You can extend the `ExperimentalDataProcessor` class to add custom measurement categories:

```python
from Main_Web_ProcessorNH3Crack import ExperimentalDataProcessor

class CustomDataProcessor(ExperimentalDataProcessor):
    def create_category_plotly_jsons(self, stages, base_filename, timestamp, exp_dir):
        # First call the parent method to create standard categories
        super().create_category_plotly_jsons(stages, base_filename, timestamp, exp_dir)
        
        # Add a custom category
        custom_category = {
            'title': 'Custom Measurements',
            'y_axis_title': 'Custom Units',
            'columns': [
                "Custom1",
                "Custom2",
                "Custom3"
            ]
        }
        
        # Create the custom plot
        plotly_data = self._create_category_plot(stages, custom_category, base_filename)
        
        # Save the custom plot
        plot_filename = f"{base_filename}_custom_plotly.json"
        plot_path = os.path.join(exp_dir, plot_filename)
        
        with open(plot_path, 'w') as f:
            json.dump(plotly_data, f, indent=2, cls=PlotlyJSONEncoder)
```

#### Automated Processing Script

Here's an example of a script that automatically processes all files in the uploads folder and generates a report:

```python
import os
import json
from datetime import datetime
from Main_Web_ProcessorNH3Crack import ExperimentalDataProcessor

def process_all_files():
    """Process all files in the uploads folder and generate a report"""
    processor = ExperimentalDataProcessor()
    
    # Get list of files in uploads folder
    upload_files = [f for f in os.listdir(processor.input_folder) if f.endswith('.txt')]
    
    if not upload_files:
        print("No files found in uploads folder.")
        return
    
    print(f"Found {len(upload_files)} files to process.")
    
    # Process each file
    results = []
    for filename in upload_files:
        try:
            print(f"Processing {filename}...")
            processor.process_file(filename)
            
            # Get experiment details
            base_filename = os.path.splitext(filename)[0]
            exp_dir = os.path.join(processor.output_folder, base_filename)
            summary_path = os.path.join(exp_dir, "experiment_summary.json")
            
            with open(summary_path, 'r') as f:
                summary = json.load(f)
            
            # Add to results
            results.append({
                'filename': filename,
                'base_filename': base_filename,
                'stages': summary['metadata']['total_stages'],
                'processed_at': summary['metadata']['processed_at']
            })
            
            print(f"Successfully processed {filename}")
        except Exception as e:
            print(f"Error processing {filename}: {e}")
            results.append({
                'filename': filename,
                'error': str(e)
            })
    
    # Generate report
    report = {
        'generated_at': datetime.now().isoformat(),
        'total_files': len(upload_files),
        'successful': len([r for r in results if 'error' not in r]),
        'failed': len([r for r in results if 'error' in r]),
        'results': results
    }
    
    # Save report
    report_path = os.path.join(processor.output_folder, f"processing_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
    with open(report_path, 'w') as f:
        json.dump(report, f, indent=2)
    
    print(f"Report saved to {report_path}")
    
    return report

if __name__ == "__main__":
    process_all_files()
```

#### Customizing the Web Interface

You can customize the web interface by modifying the templates and static files. For example, to add a custom visualization page:

1. Create a new template file `templates/custom_visualization.html`:

```html
{% extends 'base.html' %}

{% block title %}NH3 Cracking - Custom Visualization{% endblock %}

{% block content %}
<div class="card">
    <a href="{{ url_for('index') }}" class="back-link">← Back to Experiments</a>
    <h2>Custom Visualization</h2>
    
    <div class="custom-controls">
        <!-- Add custom controls here -->
    </div>
    
    <div id="custom-plot" class="plot-container">
        <div class="loading">Loading custom plot...</div>
    </div>
</div>
{% endblock %}

{% block scripts %}
<script>
    // Add custom JavaScript here
    document.addEventListener('DOMContentLoaded', function() {
        // Custom visualization code
    });
</script>
{% endblock %}
```

2. Add a new route to `app.py`:

```python
@app.route('/custom-visualization')
def custom_visualization():
    """Custom visualization page"""
    return render_template('custom_visualization.html')
```

## Troubleshooting

### Common Issues

#### Error: "No such file or directory"

This error occurs when the application can't find a requested file. Make sure:
- The file exists in the specified location
- The file name is correctly spelled (case-sensitive)
- The application has permission to access the file

#### Error: "Failed with all encodings"

This error occurs when the application can't determine the file encoding. Try:
- Saving the file with UTF-8 encoding
- Checking for invalid characters in the file
- Ensuring the file is properly formatted (tab-separated)

#### Error: "Not enough data points for cubic interpolation"

This error occurs when a column doesn't have enough data points for cubic interpolation. The application requires at least 4 data points for cubic interpolation. If this error occurs:
- Check the data file for missing values
- Consider using a different interpolation method (modify the code to use 'linear' instead of 'cubic')

#### Error: "No suitable Stage column found"

This error occurs when the application can't find a column to use as the Stage identifier. Make sure:
- The Stage column is present in the second position
- The Stage values are integers
- The column header is correctly named

### Performance Tips

- **Large Files**: For very large files (>100k rows), consider pre-processing the data to reduce size
- **Memory Usage**: If you experience memory issues, try processing files in smaller batches
- **Visualization Performance**: If plots are slow to render, reduce the number of traces or use downsampling

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

### Development Setup

1. Fork the repository
2. Clone your fork: `git clone https://github.com/yourusername/NH3CrackProcessor.git`
3. Create a new branch: `git checkout -b my-feature-branch`
4. Make your changes
5. Run tests: `python -m unittest discover tests`
6. Commit your changes: `git commit -am 'Add new feature'`
7. Push to the branch: `git push origin my-feature-branch`
8. Submit a Pull Request

### Coding Standards

- Follow PEP 8 style guide
- Write docstrings for all functions, classes, and methods
- Add comments for complex code sections
- Include type hints where appropriate
- Write unit tests for new functionality

## License

This project is licensed under the MIT License - see the LICENSE file for details.

```
MIT License

Copyright (c) 2023 GrennMilo

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

## Acknowledgments

- This tool uses [Plotly](https://plotly.com/) for interactive data visualization
- [Pandas](https://pandas.pydata.org/) and [NumPy](https://numpy.org/) for data processing
- [Flask](https://flask.palletsprojects.com/) for the web application framework
- [SciPy](https://scipy.org/) for scientific computing and interpolation
- All contributors who have helped improve this project