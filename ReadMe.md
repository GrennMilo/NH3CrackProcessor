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
    - [API Endpoints](#api-endpoints)
    - [Data Formats](#data-formats)
    - [Error Handling](#error-handling)
    - [API Usage Examples](#api-usage-examples)
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
- [Recent Updates](#recent-updates)

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

The NH3 Cracking Processor and Visualizer provides a comprehensive RESTful API for programmatic access to its functionality. This allows integration with other systems and automation of data processing and visualization tasks.

#### API Endpoints

| Endpoint | Method | Description | Parameters |
|----------|--------|-------------|------------|
| `/api/experiments` | GET | Get a list of all processed experiments | None |
| `/api/experiment/<experiment_name>/overall` | GET | Get overall plot data for an experiment | `type`: Plot type (temperature, multipoint, saturator, pressure, flow, outlet) |
| `/api/experiment/<experiment_name>/stage/<stage_num>` | GET | Get plot data for a specific stage | `type`: Plot type (temperature, multipoint, saturator, pressure, flow, outlet) |
| `/api/process/<experiment_name>` | GET | Process a specific experiment | None |
| `/api/process-all` | GET | Process all experiments in the uploads folder | None |
| `/api/visualize/<experiment_name>` | GET | Generate visualizations for an experiment | None |
| `/api/experiment/<experiment_name>/fix-json` | GET | Fix JSON files with NaN values for a specific experiment | None |

##### Experiment List Endpoint

```
GET /api/experiments
```

Returns a list of all processed experiments with their metadata.

**Response Example:**

```json
[
  {
    "name": "24_06_10 13_21_12",
    "summary": {
      "metadata": {
        "processed_at": "2025-05-29T20:23:15.301851",
        "total_stages": 1,
        "stage_numbers": [2],
        "base_filename": "24_06_10 13_21_12"
      }
    },
    "stages": 1
  },
  {
    "name": "25_02_28 14_02_06 Exp 011_Blak_Silcotek_New_SiO2_TC_QRZ",
    "summary": {
      "metadata": {
        "processed_at": "2025-05-30T10:45:32.123456",
        "total_stages": 3,
        "stage_numbers": [1, 2, 3],
        "base_filename": "25_02_28 14_02_06 Exp 011_Blak_Silcotek_New_SiO2_TC_QRZ"
      }
    },
    "stages": 3
  }
]
```

##### Overall Plot Data Endpoint

```
GET /api/experiment/<experiment_name>/overall?type=<plot_type>
```

Returns the Plotly JSON data for the specified plot type. Default plot type is "temperature" if not specified.

**Parameters:**
- `experiment_name`: Name of the experiment (URL-encoded if it contains spaces)
- `type`: Plot type (one of: temperature, multipoint, saturator, pressure, flow, outlet)

**Response Example (abbreviated):**

```json
{
  "metadata": {
    "title": "Temperature Data - 24_06_10 13_21_12",
    "processed_at": "2025-05-29T20:23:15.390748",
    "total_stages": 1
  },
  "data": [
    {
      "x": [0.0, 1.0, 2.0, 3.0, /* ... */],
      "y": [163.3, 165.14, 167.11, 169.02, /* ... */],
      "type": "scatter",
      "mode": "lines",
      "name": "R1/2 T set [°C]"
    },
    {
      "x": [0.0, 1.0, 2.0, 3.0, /* ... */],
      "y": [156.20, 158.31, 160.54, 162.84, /* ... */],
      "type": "scatter",
      "mode": "lines",
      "name": "R1/2 T read [°C]"
    }
  ],
  "layout": {
    "title": "Temperature Data - 24_06_10 13_21_12",
    "xaxis": {
      "title": "Time (minutes)"
    },
    "yaxis": {
      "title": "Temperature (°C) / Power (%)"
    }
  }
}
```

##### Stage Plot Data Endpoint

```
GET /api/experiment/<experiment_name>/stage/<stage_num>?type=<plot_type>
```

Returns the Plotly JSON data for a specific stage and plot type.

**Parameters:**
- `experiment_name`: Name of the experiment (URL-encoded if it contains spaces)
- `stage_num`: Stage number (integer)
- `type`: Plot type (one of: temperature, multipoint, saturator, pressure, flow, outlet)

**Response Example (abbreviated):**

```json
{
  "data": [
    {
      "x": [0.0, 1.0, 2.0, 3.0, /* ... */],
      "y": [163.3, 165.14, 167.11, 169.02, /* ... */],
      "type": "scatter",
      "mode": "lines",
      "name": "R1/2 T set [°C]"
    },
    {
      "x": [0.0, 1.0, 2.0, 3.0, /* ... */],
      "y": [156.20, 158.31, 160.54, 162.84, /* ... */],
      "type": "scatter",
      "mode": "lines",
      "name": "R1/2 T read [°C]"
    }
  ],
  "layout": {
    "title": "Stage 2 - Temperature",
    "xaxis": {
      "title": "Time (minutes)"
    },
    "yaxis": {
      "title": "Temperature (°C) / Power (%)"
    }
  }
}
```

##### Process Experiment Endpoint

```
GET /api/process/<experiment_name>
```

Processes the specified experiment data file. This endpoint finds the matching file in the uploads folder and processes it.

**Parameters:**
- `experiment_name`: Name of the experiment to process (URL-encoded if it contains spaces)

**Response Example:**

```json
{
  "success": true,
  "message": "Processed 1 files for experiment '24_06_10 13_21_12'",
  "processed_files": ["24_06_10 13_21_12.txt"]
}
```

##### Process All Experiments Endpoint

```
GET /api/process-all
```

Processes all experiment data files in the uploads folder.

**Response Example:**

```json
{
  "success": true,
  "message": "Processed 3 files with 0 errors",
  "processed_files": [
    "24_06_10 13_21_12.txt",
    "25_02_28 14_02_06 Exp 011_Blak_Silcotek_New_SiO2_TC_QRZ.txt",
    "25_03_21 09_35_25 Exp 012_2682.txt"
  ],
  "errors": []
}
```

##### Visualize Experiment Endpoint

```
GET /api/visualize/<experiment_name>
```

Generates Plotly visualizations for the specified experiment. This is useful when you need to regenerate visualizations after updating the experiment data.

**Parameters:**
- `experiment_name`: Name of the experiment (URL-encoded if it contains spaces)

**Response Example:**

```json
{
  "success": true,
  "message": "Visualizations created for 1 stages"
}
```

##### Fix JSON Files Endpoint

```
GET /api/experiment/<experiment_name>/fix-json
```

Fixes JSON files with NaN values for a specific experiment, replacing them with null values.

**Parameters:**
- `experiment_name`: Name of the experiment (URL-encoded if it contains spaces)

**Response Example:**

```json
{
  "success": true,
  "message": "Successfully fixed JSON files for experiment '24_06_10 13_21_12'"
}
```

#### Data Formats

The API uses the following data formats:

1. **Experiment List Format**: An array of experiment objects, each containing metadata about the experiment.
2. **Plotly JSON Format**: A JSON object that follows the Plotly.js format with `data` (traces) and `layout` sections.
3. **Process Response Format**: A JSON object with success status, message, and processed files information.

##### Plotly JSON Structure

The Plotly JSON format is designed to be directly usable by Plotly.js on the frontend:

```json
{
  "metadata": {
    "title": "Title of the plot",
    "processed_at": "Timestamp when the plot was generated",
    "total_stages": "Number of stages in the experiment"
  },
  "data": [
    {
      "x": [array of x values (time in minutes)],
      "y": [array of y values (measurements)],
      "type": "scatter",
      "mode": "lines",
      "name": "Name of the trace (column name)"
    },
    // Additional traces for other columns
  ],
  "layout": {
    "title": "Plot title",
    "xaxis": {
      "title": "X-axis title (Time (minutes))"
    },
    "yaxis": {
      "title": "Y-axis title (units)"
    },
    "template": "plotly_dark",
    "paper_bgcolor": "#1e1e1e",
    "plot_bgcolor": "#2d2d2d",
    "font": {"color": "#e0e0e0"}
  }
}
```

#### Error Handling

The API returns appropriate HTTP status codes and error messages when something goes wrong:

- **400 Bad Request**: When the request parameters are invalid
- **404 Not Found**: When the requested experiment or plot type is not found
- **500 Internal Server Error**: When an unexpected error occurs during processing

Error responses follow this format:

```json
{
  "error": "Error message describing what went wrong",
  "available_types": ["List of available plot types (for invalid plot type errors)"]
}
```

#### API Usage Examples

##### Python Example: Processing All Experiments and Retrieving Plot Data

```python
import requests
import json
import matplotlib.pyplot as plt
import plotly.io as pio
import plotly.graph_objects as go

# Base URL for the API
base_url = "http://localhost:8080"

# Process all experiments
response = requests.get(f"{base_url}/api/process-all")
result = response.json()
print(f"Processing result: {result['message']}")

# Get list of experiments
response = requests.get(f"{base_url}/api/experiments")
experiments = response.json()
print(f"Found {len(experiments)} experiments")

# Get temperature plot data for the first experiment
experiment_name = experiments[0]['name']
response = requests.get(f"{base_url}/api/experiment/{experiment_name}/overall?type=temperature")
plot_data = response.json()

# Create Plotly figure
fig = go.Figure()
for trace in plot_data['data']:
    fig.add_trace(go.Scatter(x=trace['x'], y=trace['y'], name=trace['name'], mode=trace['mode']))

fig.update_layout(
    title=plot_data['metadata']['title'],
    xaxis_title="Time (minutes)",
    yaxis_title=plot_data['layout']['yaxis']['title']
)

# Show the figure
fig.show()

# Save plot data to file
with open(f"{experiment_name}_temperature.json", "w") as f:
    json.dump(plot_data, f, indent=2)
```

##### JavaScript Example: Fetching and Displaying a Plot

```javascript
// Base URL for the API
const baseUrl = "http://localhost:8080";

// Function to fetch and display a plot
async function fetchAndDisplayPlot(experimentName, plotType = 'temperature') {
  try {
    // Fetch the plot data
    const response = await fetch(`${baseUrl}/api/experiment/${encodeURIComponent(experimentName)}/overall?type=${plotType}`);
    
    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(`Error: ${errorData.error}`);
    }
    
    const plotData = await response.json();
    
    // Create the plot
    Plotly.newPlot('plot-container', plotData.data, plotData.layout);
    
  } catch (error) {
    console.error('Failed to fetch plot data:', error);
    document.getElementById('plot-container').innerHTML = `<div class="error">${error.message}</div>`;
  }
}

// Example usage
document.addEventListener('DOMContentLoaded', () => {
  const experimentSelector = document.getElementById('experiment-selector');
  const plotTypeSelector = document.getElementById('plot-type-selector');
  
  // Populate the experiment selector
  fetch(`${baseUrl}/api/experiments`)
    .then(response => response.json())
    .then(experiments => {
      experiments.forEach(experiment => {
        const option = document.createElement('option');
        option.value = experiment.name;
        option.textContent = experiment.name;
        experimentSelector.appendChild(option);
      });
      
      // Fetch the first experiment plot if available
      if (experiments.length > 0) {
        fetchAndDisplayPlot(experiments[0].name);
      }
    });
  
  // Event listeners for selectors
  experimentSelector.addEventListener('change', () => {
    fetchAndDisplayPlot(experimentSelector.value, plotTypeSelector.value);
  });
  
  plotTypeSelector.addEventListener('change', () => {
    fetchAndDisplayPlot(experimentSelector.value, plotTypeSelector.value);
  });
});
```

## Data Processing

The NH3 Cracking Processor and Visualizer implements a sophisticated data processing pipeline that transforms raw experimental data into structured, analyzable datasets and interactive visualizations.

### Input Data Format

The processor expects tab-separated text files (.txt) with the following structure:

1. **First column**: Date/time information in various formats (e.g., DD/MM/YY HH:MM:SS)
2. **Second column**: Stage identifier (integer values to identify different experimental stages)
3. **Remaining columns**: Numeric measurement data for various parameters

Example of expected input format:

```
DateTime            Stage    R1/2 T set [°C]    R1/2 T read [°C]    Pressure [bar]    Flow [Nml/min]
01/06/24 12:34:56    1        450.2              451.3               25.3              380.5
01/06/24 12:35:56    1        451.3              452.4               25.4              380.2
01/06/24 12:36:56    1        450.8              451.9               25.2              380.4
01/06/24 12:37:56    2        460.1              461.2               26.0              381.0
01/06/24 12:38:56    2        461.5              462.6               26.1              381.2
```

The application supports multiple date/time formats:
- DD/MM/YY HH:MM:SS
- YYYY-MM-DD HH:MM:SS
- DD/MM/YYYY HH:MM:SS
- MM/DD/YY HH:MM:SS
- MM/DD/YYYY HH:MM:SS

And multiple file encodings:
- UTF-8
- Latin1 (ISO-8859-1)
- CP1252
- ISO-8859-1

### Processing Pipeline

The data processing pipeline consists of the following steps:

1. **File Reading**: The application reads the tab-separated file using pandas, automatically detecting the correct encoding.

   ```python
   def read_data_file(self, filename):
       filepath = os.path.join(self.input_folder, filename)
       
       # Try multiple encodings
       encodings = ['utf-8', 'latin1', 'cp1252', 'ISO-8859-1']
       
       for encoding in encodings:
           try:
               # Read the file with tab separator
               df = pd.read_csv(filepath, sep='\t', encoding=encoding)
               return df
           except UnicodeDecodeError:
               continue
   ```

2. **Time Vector Creation**: The application converts datetime strings to a consistent time vector in minutes.

3. **Stage Detection**: The application identifies different experimental stages based on the Stage column.

4. **Data Interpolation**: The application performs cubic interpolation to create a consistent time grid with 1-minute intervals.

5. **Data Organization**: The application organizes the data into different categories (temperature, pressure, flow, etc.).

6. **Plotly JSON Generation**: The application generates Plotly JSON files for different data views.

7. **Data Export**: The application exports processed data in CSV and JSON formats.

### Time Vector Handling

Time vector handling is a critical aspect of the processing pipeline. The application converts various datetime formats into a consistent relative time vector in minutes, making it easier to analyze and visualize the data.

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
    
    for date_format in date_formats:
        try:
            # Convert datetime strings to datetime objects
            df[datetime_col] = pd.to_datetime(df[datetime_col], format=date_format)
            break
        except ValueError:
            continue
    
    # Create time vector in minutes from start
    start_time = df[datetime_col].min()
    df['Time_Minutes'] = (df[datetime_col] - start_time).dt.total_seconds() / 60
```

If datetime parsing fails, the application creates a sequential time vector as a fallback:

```python
# Fallback: create sequential time vector
df['Time_Minutes'] = np.arange(len(df))
```

### Stage Detection

The application detects different experimental stages by examining the second column of the input data, which is expected to contain stage identifiers (integer values). This allows the application to separate the data into different stages for analysis and visualization.

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

Each stage is stored as a separate dataset and processed independently, allowing for stage-specific analysis and visualization.

### Data Interpolation

To ensure a consistent time grid across all measurements, the application performs cubic interpolation for all numeric columns. This is particularly important for creating smooth visualizations and for comparing data across different stages.

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
```

The application uses cubic interpolation when there are at least 4 data points, which provides smooth curves. For the Stage column, the application uses nearest-neighbor interpolation to maintain the integrity of the stage identifiers.

### Plotly JSON Generation

The application generates JSON files that follow the Plotly.js format, making it easy to create interactive visualizations on the web interface. The JSON files contain both the data (traces) and the layout information.

```python
def create_stage_plotly_json(self, stage_df, stage_num, base_filename, output_dir):
    """Generate Plotly JSON files for a specific stage"""
    
    # Process each plot group
    for group_key, group_config in config.STAGE_PLOT_GROUPS.items():
        # Get the plot title and filename
        title = group_config['title'].format(stage_num=stage_num)
        filename = group_config['filename'].format(stage_num=stage_num)
        
        # Get columns to include in this plot
        if 'column_pattern' in group_config:
            # For multipoint thermocouples, find columns matching the pattern
            pattern = group_config['column_pattern']
            plot_cols = [col for col in stage_df.columns if pattern in col]
        else:
            # For regular plots, use the specified columns
            plot_cols = [col for col in group_config['columns'] if col in stage_df.columns]
        
        if not plot_cols:
            continue  # Skip if no matching columns
        
        # Create traces for each column
        traces = []
        for i, col in enumerate(plot_cols):
            color = config.PLOT_COLORS[i % len(config.PLOT_COLORS)]
            trace = {
                'x': stage_df['Time_Minutes'].tolist(),
                'y': stage_df[col].tolist(),
                'type': 'scatter',
                'mode': 'lines',
                'name': col,
                'line': {'color': color, 'width': 2}
            }
            traces.append(trace)
        
        # Create layout
        layout = {
            'title': title,
            'xaxis': {
                'title': 'Time (minutes)',
                'gridcolor': config.PLOTLY_GRID_COLOR
            },
            'yaxis': {
                'title': group_config['y_axis_title'],
                'gridcolor': config.PLOTLY_GRID_COLOR
            },
            'template': config.PLOTLY_THEME,
            'paper_bgcolor': config.PLOTLY_PAPER_BGCOLOR,
            'plot_bgcolor': config.PLOTLY_PLOT_BGCOLOR,
            'font': {'color': config.PLOTLY_FONT_COLOR},
            'hovermode': 'closest',
            'legend': {
                'orientation': 'v',
                'bgcolor': 'rgba(0,0,0,0.5)',
                'bordercolor': 'rgba(255,255,255,0.2)',
                'borderwidth': 1
            }
        }
        
        # Create Plotly data
        plotly_data = {
            'data': traces,
            'layout': layout
        }
        
        # Save to file
        output_path = os.path.join(output_dir, filename)
        with open(output_path, 'w') as f:
            json.dump(plotly_data, f, indent=2, cls=CustomJSONEncoder)
```

For the overall experiment plots, the application combines data from all stages and generates a comprehensive visualization:

```python
def create_plotly_json(self, stages, base_filename, timestamp, output_dir):
    """Generate Plotly JSON files for the overall experiment"""
    
    # Create plots for different categories
    self.create_category_plotly_jsons(stages, base_filename, timestamp, output_dir)
```

The `create_category_plotly_jsons` method generates specialized plots for different data categories (temperature, pressure, flow, etc.) based on the configuration in `config.py`.

### Category-Based Data Organization

The application organizes the data into different categories based on the column names and patterns. This makes it easier to analyze and visualize related measurements together.

Categories defined in `config.py`:

```python
DATA_CATEGORIES = {
    "temperature": {
        "title": "Temperature Measurements",
        "y_axis_title": "Temperature (°C) / Power (%)",
        "columns": [
            "R1/2 T set [°C]", 
            "R1/2 T read [°C]", 
            "R1/2 T power [%]", 
            "Saturator T read [°C]"
        ],
        "filename_suffix": "temp_plotly_data.json"
    },
    "multipoint": {
        "title": "Multipoint Temperature Measurements",
        "y_axis_title": "Temperature (°C)",
        "column_pattern": "R-1/2 T",
        "filename_suffix": "multipoint_temp_plotly_data.json"
    },
    "saturator": {
        "title": "Saturator Temperature",
        "y_axis_title": "Temperature (°C)",
        "columns": ["Saturator T read [°C]"],
        "filename_suffix": "saturator_temp_plotly_data.json"
    },
    "pressure": {
        "title": "Pressure Measurements",
        "y_axis_title": "Pressure (bar)",
        "columns": [
            "Pressure SETPOINT [bar]", 
            "Pressure PIC [bar]", 
            "Pressure reading line [bar]",
            "Pressure reading R1/2 IN [bar]", 
            "Pressure reading R1/2 OUT [bar]", 
            "High pressure NH3 line [bar]"
        ],
        "filename_suffix": "pressure_plotly_data.json"
    },
    "flow": {
        "title": "Flow Measurements",
        "y_axis_title": "Flow (Nml/min) / Concentration (%)",
        "columns": [
            "NH3 Actual Set-Point [Nml/min]", 
            "H2 Actual Flow [Nml/min]", 
            "Tot flow calc [Nml/min]",
            "NH3 in %", 
            "Inert in %", 
            "H2O in %"
        ],
        "filename_suffix": "flow_plotly_data.json"
    },
    "outlet": {
        "title": "Outlet Stream Composition",
        "y_axis_title": "Composition (%)",
        "columns": [
            "NH3 out [%]", 
            "H2 out [%]", 
            "H2O out [%]"
        ],
        "filename_suffix": "outlet_plotly_data.json"
    }
}
```

For each category, the application generates a separate Plotly JSON file with the appropriate columns and layout.

### NaN Handling in JSON

JSON does not support NaN (Not a Number) values, which can cause issues when the data contains missing or invalid measurements. The application uses a custom JSON encoder to handle NaN values:

```python
class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (np.integer, np.floating, np.bool_)):
            return obj.item()
        if pd.isna(obj):
            return None
        if np.isnan(obj):
            return None
        if np.isinf(obj):
            return None
        return super().default(obj)
```

This encoder converts NaN values to `null`, which is a valid JSON value and can be properly handled by JavaScript.

### Full Processing Example

Here's an example of the complete processing flow for a single file:

```python
from Main_Web_ProcessorNH3Crack import ExperimentalDataProcessor

# Initialize processor
processor = ExperimentalDataProcessor(
    input_folder="uploads",
    output_folder="Reports"
)

# Process a file
processor.process_file("24_06_10 13_21_12.txt")
```

This will:
1. Read the file from the uploads folder
2. Create a time vector in minutes
3. Detect stages in the data
4. Perform cubic interpolation for all numeric columns
5. Generate separate datasets for each stage
6. Create Plotly JSON files for each stage and data category
7. Save all processed data to the Reports folder

## Visualization

The NH3 Cracking Processor and Visualizer uses Plotly.js to create interactive, publication-quality visualizations of experimental data. These visualizations allow researchers to explore and analyze their data in detail.

### Plotly Integration

[Plotly.js](https://plotly.com/javascript/) is a high-level, declarative charting library that provides a wide range of interactive visualizations. The application uses Plotly.js to create interactive plots that allow users to:

- Zoom in/out on specific regions
- Pan across the data
- Hover over data points to see exact values
- Toggle visibility of data series
- Download plots as PNG images

The integration works as follows:

1. The backend (Python) generates Plotly-compatible JSON files for different data views
2. The frontend (JavaScript) loads these JSON files via the API
3. Plotly.js renders the JSON data as interactive visualizations

Example of the JavaScript code used to render Plotly visualizations:

```javascript
function renderPlot(plotData, containerId) {
  // Create Plotly plot
  Plotly.newPlot(containerId, plotData.data, plotData.layout, {
    responsive: true,
    displayModeBar: true,
    modeBarButtonsToRemove: ['lasso2d', 'select2d']
  });
}

// Load plot data from API
async function loadPlotData(experimentName, plotType = 'temperature') {
  const response = await fetch(`/api/experiment/${encodeURIComponent(experimentName)}/overall?type=${plotType}`);
  const plotData = await response.json();
  renderPlot(plotData, 'plot-container');
}
```

### Data Categories

The application organizes measurements into logical categories to facilitate analysis and visualization. Each category focuses on a specific aspect of the experiment:

#### Temperature Category

![Temperature Plot](https://via.placeholder.com/800x400?text=Temperature+Plot)

The temperature category includes:
- R1/2 T set [°C]: Temperature setpoint
- R1/2 T read [°C]: Actual temperature reading
- R1/2 T power [%]: Power percentage
- Saturator T read [°C]: Saturator temperature

```javascript
// Example of temperature data structure
{
  "data": [
    {
      "x": [0, 1, 2, ...],  // Time in minutes
      "y": [450.2, 451.3, 450.8, ...],  // Temperature setpoint values
      "type": "scatter",
      "mode": "lines",
      "name": "R1/2 T set [°C]"
    },
    {
      "x": [0, 1, 2, ...],
      "y": [449.5, 450.8, 450.2, ...],
      "type": "scatter",
      "mode": "lines",
      "name": "R1/2 T read [°C]"
    }
  ]
}
```

#### Multipoint Temperature Category

![Multipoint Temperature Plot](https://via.placeholder.com/800x400?text=Multipoint+Temperature+Plot)

The multipoint temperature category includes temperature measurements at multiple points, with column names matching the pattern "R-1/2 T".

#### Pressure Category

![Pressure Plot](https://via.placeholder.com/800x400?text=Pressure+Plot)

The pressure category includes:
- Pressure SETPOINT [bar]: Pressure setpoint
- Pressure PIC [bar]: Pressure controller reading
- Pressure reading line [bar]: Line pressure
- Pressure reading R1/2 IN [bar]: Reactor inlet pressure
- Pressure reading R1/2 OUT [bar]: Reactor outlet pressure
- High pressure NH3 line [bar]: Ammonia line pressure

#### Flow Category

![Flow Plot](https://via.placeholder.com/800x400?text=Flow+Plot)

The flow category includes:
- NH3 Actual Set-Point [Nml/min]: Ammonia flow setpoint
- H2 Actual Flow [Nml/min]: Hydrogen flow
- Tot flow calc [Nml/min]: Total calculated flow
- NH3 in %: Ammonia inlet concentration
- Inert in %: Inert gas concentration
- H2O in %: Water concentration

#### Outlet Composition Category

![Outlet Composition Plot](https://via.placeholder.com/800x400?text=Outlet+Composition+Plot)

The outlet composition category includes:
- NH3 out [%]: Ammonia outlet concentration
- H2 out [%]: Hydrogen outlet concentration
- H2O out [%]: Water outlet concentration

### Visualization Types

The application provides several types of visualizations:

#### 1. Overall Experiment Plots

These plots show data across all stages of the experiment, providing a comprehensive view of the entire experiment. Each data category has its own overall plot.

Example API call:
```
GET /api/experiment/24_06_10 13_21_12/overall?type=temperature
```

#### 2. Stage-Specific Plots

These plots focus on a specific stage of the experiment, allowing for detailed analysis of each stage. Each data category has stage-specific plots.

Example API call:
```
GET /api/experiment/24_06_10 13_21_12/stage/2?type=temperature
```

#### 3. Category-Based Plots

These plots organize data by category (temperature, pressure, flow, etc.), allowing for focused analysis of specific aspects of the experiment.

Example: Temperature category plot showing temperature setpoint, actual temperature, and power percentage.

#### 4. Customized Plots

The web interface allows users to customize visualizations in real-time:

- **Plot Type**: Switch between line plots and scatter plots
- **Theme**: Choose between dark and light themes
- **Visibility**: Toggle the visibility of specific data series
- **Zoom Level**: Zoom in on specific time periods
- **Data Range**: Focus on specific data ranges

### Interactive Plot Features

The interactive plots provide several advanced features:

#### Hover Information

Hover over any data point to see exact values:
- X value (time in minutes)
- Y value (measurement)
- Series name

#### Zoom and Pan

- Zoom in on specific regions by clicking and dragging
- Double-click to reset the zoom
- Click and drag the plot to pan

#### Plot Controls

The modebar provides additional controls:
- Download plot as PNG
- Zoom in/out
- Pan
- Reset axes
- Toggle spike lines
- Toggle hover mode

#### Responsive Design

The plots are designed to be responsive, adapting to different screen sizes and devices.

### Dark Mode Optimization

The plots are optimized for dark mode, with a dark background and high-contrast colors for better visibility in low-light environments.

Default theme settings:
```python
PLOTLY_THEME = "plotly_dark"
PLOTLY_PAPER_BGCOLOR = "#1e1e1e"
PLOTLY_PLOT_BGCOLOR = "#2d2d2d"
PLOTLY_FONT_COLOR = "#e0e0e0"
PLOTLY_GRID_COLOR = "rgba(255, 255, 255, 0.1)"
```

### Plot Generation Process

The application generates plots through the following process:

1. **Data Preparation**: The processed data is organized by stage and category
2. **Trace Creation**: For each data column, a trace (line or scatter) is created
3. **Layout Configuration**: The plot layout is configured with appropriate titles, axes, and styling
4. **JSON Generation**: The plot data and layout are converted to JSON format
5. **Frontend Rendering**: The JSON data is loaded by the frontend and rendered using Plotly.js

Example of the Python code used to generate plots:

```python
def create_plotly_json(self, stages, base_filename, timestamp, output_dir):
    """Generate Plotly JSON files for the overall experiment"""
    
    # Create plots for different categories
    self.create_category_plotly_jsons(stages, base_filename, timestamp, output_dir)
```

### Customization Options

The visualizations can be customized in several ways:

#### Backend Customization

Edit `config.py` to change:
- Plot colors
- Theme settings
- Data categories
- Column mappings

#### Frontend Customization

The web interface provides controls to:
- Switch between line and scatter plots
- Change the theme
- Toggle series visibility
- Focus on specific time periods

Example:
```javascript
function updatePlotType(plotType) {
    // Update trace modes based on plot type
    const updatedData = plotData.data.map(trace => ({
        ...trace,
        mode: plotType === 'line' ? 'lines' : 'markers'
    }));
    
    Plotly.react('plot-container', updatedData, plotData.layout);
}

document.getElementById('plot-type-selector').addEventListener('change', (event) => {
    updatePlotType(event.target.value);
});
```

### Export Options

The interactive plots can be exported in several formats:

- **PNG**: High-quality raster image
- **SVG**: Scalable vector graphic
- **JSON**: Raw plot data and layout for further processing

To export a plot as PNG:
```javascript
document.getElementById('export-png').addEventListener('click', () => {
    Plotly.downloadImage('plot-container', {
        format: 'png',
        filename: 'experiment_plot',
        width: 1200,
        height: 800
    });
});
```

### Advanced Visualization Techniques

#### Multi-Axis Plots

For comparing measurements with different units and scales, you can create multi-axis plots:

```javascript
// Create a plot with multiple y-axes
const layout = {
    title: 'Temperature and Pressure',
    yaxis: {
        title: 'Temperature (°C)',
        side: 'left'
    },
    yaxis2: {
        title: 'Pressure (bar)',
        overlaying: 'y',
        side: 'right'
    }
};

// Configure traces to use different axes
const temperatureTrace = {
    y: temperatureData,
    name: 'Temperature',
    yaxis: 'y'
};

const pressureTrace = {
    y: pressureData,
    name: 'Pressure',
    yaxis: 'y2'
};

Plotly.newPlot('multi-axis-plot', [temperatureTrace, pressureTrace], layout);
```

#### Annotation and Highlighting

You can add annotations and highlighting to emphasize important aspects of the data:

```javascript
// Add annotations
const layout = {
    annotations: [
        {
            x: 45,  // Time in minutes
            y: 450,  // Value
            text: 'Peak Temperature',
            showarrow: true,
            arrowhead: 2,
            arrowsize: 1,
            arrowwidth: 2,
            arrowcolor: '#ff0000'
        }
    ]
};
```

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
│       ├── [experiment_name]_multipoint_temp_plotly_data.json # Multipoint temperature data
│       ├── [experiment_name]_saturator_temp_plotly_data.json # Saturator temperature data
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

The NH3 Cracking Processor and Visualizer generates a structured hierarchy of files to organize the processed data and visualizations. Understanding this structure is crucial for working with the application and integrating it with other systems.

### Directory Structure

For each processed experiment, the application creates a dedicated directory in the Reports folder, named after the experiment:

```
Reports/
└── 24_06_10 13_21_12/                     # Experiment directory
    ├── experiment_summary.json            # Experiment metadata and summary
    ├── 24_06_10 13_21_12_complete.csv     # Complete experiment data in CSV format
    ├── 24_06_10 13_21_12_all_stages.json  # Complete experiment data in JSON format
    ├── 24_06_10 13_21_12_temp_plotly_data.json        # Temperature plot data
    ├── 24_06_10 13_21_12_multipoint_temp_plotly_data.json # Multipoint temperature plot data
    ├── 24_06_10 13_21_12_saturator_temp_plotly_data.json  # Saturator temperature plot data
    ├── 24_06_10 13_21_12_pressure_plotly_data.json    # Pressure plot data
    ├── 24_06_10 13_21_12_flow_plotly_data.json        # Flow plot data
    ├── 24_06_10 13_21_12_outlet_plotly_data.json      # Outlet composition plot data
    └── stage_2/                           # Stage-specific directory
        ├── stage_2_data.csv               # Stage data in CSV format
        ├── stage_2_data.json              # Stage data in JSON format
        ├── stage_2_temp_plotly.json       # Stage temperature plot data
        ├── stage_2_multipoint_temp_plotly.json   # Stage multipoint temperature plot data
        ├── stage_2_saturator_temp_plotly.json    # Stage saturator temperature plot data
        ├── stage_2_pressure_plotly.json    # Stage pressure plot data
        ├── stage_2_flow_plotly.json        # Stage flow plot data
        └── stage_2_outlet_plotly.json      # Stage outlet composition plot data
```

### File Formats

The application generates several types of files:

#### 1. Experiment Summary (JSON)

The `experiment_summary.json` file contains metadata about the experiment, including:
- Processing timestamp
- Total number of stages
- Stage numbers
- Column mapping with statistical information

Example:
```json
{
  "metadata": {
    "processed_at": "2025-05-29T20:23:15.301851",
    "total_stages": 1,
    "stage_numbers": [2],
    "base_filename": "24_06_10 13_21_12"
  },
  "column_mapping": {
    "Time_Minutes": {
      "index": 0,
      "dtype": "float64",
      "non_null_count": 129,
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
    }
    // Additional columns...
  },
  "stages_info": {
    "2": {
      "row_count": 129,
      "time_range": {
        "start": 0.0,
        "end": 128.0,
        "duration": 128.0
      }
    }
  }
}
```

#### 2. Complete Data (CSV)

The `{experiment_name}_complete.csv` file contains all the data from the experiment in CSV format, with each row representing a measurement at a specific time point.

Example:
```csv
Time_Minutes,NH3 Actual Set-Point [Nml/min],NH3 Actual Flow [Nml/min],Inert Actual Set-Point [Nml/min],Inert Actual Flow [Nml/min],H2 Actual Set-Point [Nml/min],H2 Actual Flow [Nml/min],R1/2 T set [°C],R1/2 T read [°C],R1/2 T power [%],Saturator T read [°C],Pressure SETPOINT [bar],Pressure PIC [bar],Pressure reading line [bar],Pressure reading R1/2 IN [bar],Pressure reading R1/2 OUT [bar]
0.0,0.0,0.0,400.0,400.0,0.0,0.0,163.3,156.2050364157259,25.600487144764557,0.0,0.0,0.0,0.1,0.6,-0.2
1.0,0.0,0.0,400.0,400.0,0.0,0.0,165.14063319843282,158.31467932637683,25.475830166855183,0.0,0.0,0.0,0.1,0.6,-0.2
```

#### 3. Complete Data (JSON)

The `{experiment_name}_all_stages.json` file contains all the data from the experiment in JSON format, with each column represented as an array of values.

Example:
```json
{
  "Time_Minutes": [0.0, 1.0, 2.0, 3.0, ...],
  "NH3 Actual Set-Point [Nml/min]": [0.0, 0.0, 0.0, 0.0, ...],
  "NH3 Actual Flow [Nml/min]": [0.0, 0.0, 0.0, 0.0, ...],
  "R1/2 T set [°C]": [163.3, 165.14063319843282, 167.11889377598294, 169.02869189211287, ...],
  "R1/2 T read [°C]": [156.2050364157259, 158.31467932637683, 160.54184267849114, 162.84644397781336, ...],
  "R1/2 T power [%]": [25.600487144764557, 25.475830166855183, 25.363037256320076, 25.24913095257221, ...],
  // Additional columns...
}
```

#### 4. Stage Data (CSV)

The `stage_{stage_num}_data.csv` file contains the data for a specific stage in CSV format.

Example:
```csv
Time_Minutes,NH3 Actual Set-Point [Nml/min],NH3 Actual Flow [Nml/min],Inert Actual Set-Point [Nml/min],Inert Actual Flow [Nml/min],H2 Actual Set-Point [Nml/min],H2 Actual Flow [Nml/min],R1/2 T set [°C],R1/2 T read [°C],R1/2 T power [%],Saturator T read [°C],Pressure SETPOINT [bar],Pressure PIC [bar],Pressure reading line [bar],Pressure reading R1/2 IN [bar],Pressure reading R1/2 OUT [bar]
0.0,0.0,0.0,400.0,400.0,0.0,0.0,163.3,156.2050364157259,25.600487144764557,0.0,0.0,0.0,0.1,0.6,-0.2
1.0,0.0,0.0,400.0,400.0,0.0,0.0,165.14063319843282,158.31467932637683,25.475830166855183,0.0,0.0,0.0,0.1,0.6,-0.2
```

#### 5. Stage Data (JSON)

The `stage_{stage_num}_data.json` file contains the data for a specific stage in JSON format.

Example:
```json
{
  "Time_Minutes": [0.0, 1.0, 2.0, 3.0, ...],
  "NH3 Actual Set-Point [Nml/min]": [0.0, 0.0, 0.0, 0.0, ...],
  "NH3 Actual Flow [Nml/min]": [0.0, 0.0, 0.0, 0.0, ...],
  "R1/2 T set [°C]": [163.3, 165.14063319843282, 167.11889377598294, 169.02869189211287, ...],
  "R1/2 T read [°C]": [156.2050364157259, 158.31467932637683, 160.54184267849114, 162.84644397781336, ...],
  // Additional columns...
}
```

#### 6. Overall Plot Data (JSON)

The `{experiment_name}_{category}_plotly_data.json` files contain the Plotly visualization data for different categories across all stages.

Example (`24_06_10 13_21_12_temp_plotly_data.json`):
```json
{
  "metadata": {
    "title": "Temperature Data - 24_06_10 13_21_12",
    "processed_at": "2025-05-29T20:23:15.390748",
    "total_stages": 1
  },
  "data": [
    {
      "x": [0.0, 1.0, 2.0, 3.0, ...],
      "y": [163.3, 165.14063319843282, 167.11889377598294, 169.02869189211287, ...],
      "type": "scatter",
      "mode": "lines",
      "name": "R1/2 T set [°C]",
      "line": {"color": "#ff6e6e", "width": 2}
    },
    {
      "x": [0.0, 1.0, 2.0, 3.0, ...],
      "y": [156.2050364157259, 158.31467932637683, 160.54184267849114, 162.84644397781336, ...],
      "type": "scatter",
      "mode": "lines",
      "name": "R1/2 T read [°C]",
      "line": {"color": "#5c9eff", "width": 2}
    },
    {
      "x": [0.0, 1.0, 2.0, 3.0, ...],
      "y": [25.600487144764557, 25.475830166855183, 25.363037256320076, 25.24913095257221, ...],
      "type": "scatter",
      "mode": "lines",
      "name": "R1/2 T power [%]",
      "line": {"color": "#6dff6d", "width": 2}
    }
  ],
  "layout": {
    "title": "Temperature Data - 24_06_10 13_21_12",
    "xaxis": {
      "title": "Time (minutes)",
      "gridcolor": "rgba(255, 255, 255, 0.1)"
    },
    "yaxis": {
      "title": "Temperature (°C) / Power (%)",
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

#### 7. Stage Plot Data (JSON)

The `stage_{stage_num}_{category}_plotly.json` files contain the Plotly visualization data for different categories within a specific stage.

Example (`stage_2_temp_plotly.json`):
```json
{
  "data": [
    {
      "x": [0.0, 1.0, 2.0, 3.0, ...],
      "y": [163.3, 165.14063319843282, 167.11889377598294, 169.02869189211287, ...],
      "type": "scatter",
      "mode": "lines",
      "name": "R1/2 T set [°C]",
      "line": {"color": "#ff6e6e", "width": 2}
    },
    {
      "x": [0.0, 1.0, 2.0, 3.0, ...],
      "y": [156.2050364157259, 158.31467932637683, 160.54184267849114, 162.84644397781336, ...],
      "type": "scatter",
      "mode": "lines",
      "name": "R1/2 T read [°C]",
      "line": {"color": "#5c9eff", "width": 2}
    }
  ],
  "layout": {
    "title": "Stage 2 - Temperature",
    "xaxis": {
      "title": "Time (minutes)",
      "gridcolor": "rgba(255, 255, 255, 0.1)"
    },
    "yaxis": {
      "title": "Temperature (°C) / Power (%)",
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

### Accessing the Data Programmatically

You can access the processed data programmatically using Python or any language that can read JSON and CSV files:

#### Python Example: Loading and Analyzing Stage Data

```python
import pandas as pd
import json
import matplotlib.pyplot as plt

# Load stage data
def load_stage_data(experiment_name, stage_num):
    # Load JSON data
    with open(f"Reports/{experiment_name}/stage_{stage_num}/stage_{stage_num}_data.json", "r") as f:
        stage_data = json.load(f)
    
    # Convert to DataFrame
    df = pd.DataFrame(stage_data)
    return df

# Load Plotly visualization data
def load_plotly_data(experiment_name, stage_num, category="temperature"):
    file_path = f"Reports/{experiment_name}/stage_{stage_num}/stage_{stage_num}_{category}_plotly.json"
    with open(file_path, "r") as f:
        plotly_data = json.load(f)
    return plotly_data

# Example usage
experiment_name = "24_06_10 13_21_12"
stage_num = 2

# Load stage data
df = load_stage_data(experiment_name, stage_num)

# Calculate statistics
temp_stats = {
    'mean': df['R1/2 T read [°C]'].mean(),
    'max': df['R1/2 T read [°C]'].max(),
    'min': df['R1/2 T read [°C]'].min(),
    'std': df['R1/2 T read [°C]'].std()
}

print(f"Temperature Statistics for Stage {stage_num}:")
print(f"Mean: {temp_stats['mean']:.2f}°C")
print(f"Max: {temp_stats['max']:.2f}°C")
print(f"Min: {temp_stats['min']:.2f}°C")
print(f"Std Dev: {temp_stats['std']:.2f}°C")

# Plot temperature data
plt.figure(figsize=(12, 6))
plt.plot(df['Time_Minutes'], df['R1/2 T set [°C]'], label='Set Temperature')
plt.plot(df['Time_Minutes'], df['R1/2 T read [°C]'], label='Actual Temperature')
plt.title(f"Temperature Data - Stage {stage_num}")
plt.xlabel("Time (minutes)")
plt.ylabel("Temperature (°C)")
plt.legend()
plt.grid(True, alpha=0.3)
plt.show()
```

#### JavaScript Example: Loading and Displaying Plotly Data

```javascript
// Load and display Plotly data
async function loadAndDisplayPlot(experimentName, stageNum, category = 'temperature') {
  try {
    // Fetch stage plot data
    const response = await fetch(`/api/experiment/${encodeURIComponent(experimentName)}/stage/${stageNum}?type=${category}`);
    
    if (!response.ok) {
      throw new Error(`Failed to load plot data: ${response.statusText}`);
    }
    
    const plotData = await response.json();
    
    // Render the plot
    Plotly.newPlot('plot-container', plotData.data, plotData.layout, {
      responsive: true,
      displayModeBar: true
    });
    
  } catch (error) {
    console.error('Error:', error);
    document.getElementById('plot-container').innerHTML = `<div class="error">${error.message}</div>`;
  }
}

// Usage
document.addEventListener('DOMContentLoaded', () => {
  loadAndDisplayPlot('24_06_10 13_21_12', 2, 'temperature');
});
```

### Data Storage Considerations

The application generates a significant amount of data for each experiment, including both raw data and visualization files. Here are some considerations for managing this data:

1. **Storage Requirements**: For typical experiments, the generated files can range from a few MB to several hundred MB, depending on the number of stages and the complexity of the data.

2. **Backup Strategy**: It's recommended to regularly back up the Reports folder to prevent data loss.

3. **Data Cleanup**: For long-term storage, you might want to compress older experiment folders or move them to an archive location.

4. **File Organization**: The hierarchical structure (experiment > stage > data/visualization) makes it easy to locate specific data, but as the number of experiments grows, you might want to implement additional organizational schemes (e.g., by date, by experiment type, etc.).

5. **Data Sharing**: The JSON and CSV formats make it easy to share data with colleagues or import it into other analysis tools.

## Technical Details

The NH3 Cracking Processor and Visualizer is built with a modern architecture that separates concerns between data processing, API endpoints, and the web interface. This section provides technical details about the implementation, architecture, and key components of the application.

### Architecture Overview

The application follows a layered architecture:

1. **Data Processing Layer**: Handles the parsing, transformation, and storage of experimental data
2. **API Layer**: Provides RESTful endpoints for accessing and manipulating data
3. **Web Interface Layer**: Provides a user-friendly interface for interacting with the application

```
┌───────────────────────────────────────────────────────────────┐
│                      Web Interface Layer                      │
│                                                               │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐   │
│  │   Experiment │  │   Upload    │  │   Documentation     │   │
│  │   Viewer     │  │   Interface │  │   Pages             │   │
│  └─────────────┘  └─────────────┘  └─────────────────────┘   │
└───────────────────────────────────────────────────────────────┘
                            ▲
                            │
                            ▼
┌───────────────────────────────────────────────────────────────┐
│                         API Layer                             │
│                                                               │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐   │
│  │  Experiment │  │  Processing │  │  Visualization      │   │
│  │  Endpoints  │  │  Endpoints  │  │  Endpoints          │   │
│  └─────────────┘  └─────────────┘  └─────────────────────┘   │
└───────────────────────────────────────────────────────────────┘
                            ▲
                            │
                            ▼
┌───────────────────────────────────────────────────────────────┐
│                   Data Processing Layer                       │
│                                                               │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐   │
│  │  File       │  │  Data       │  │  Visualization      │   │
│  │  Parsing    │  │  Processing │  │  Generation         │   │
│  └─────────────┘  └─────────────┘  └─────────────────────┘   │
└───────────────────────────────────────────────────────────────┘
```

### Dependencies

The application requires the following Python libraries:

1. **Web Framework**:
   - **Flask**: Lightweight web application framework
   - **Werkzeug**: WSGI utility library
   - **Jinja2**: Template engine

2. **Data Processing**:
   - **Pandas**: Data manipulation and analysis
   - **NumPy**: Numerical computing
   - **SciPy**: Scientific computing (used for interpolation)

3. **Visualization**:
   - **Plotly**: Interactive visualizations

4. **Utilities**:
   - **MarkupSafe**: Escapes characters for HTML/XML
   - **Click**: Command line interface creation kit
   - **itsdangerous**: Helpers for passing data to untrusted environments
   - **Pathlib**: Object-oriented filesystem paths

### Installation Details

The application can be installed using pip:

```bash
pip install -r requirements.txt
```

A minimal `requirements.txt` file would include:

```
Flask>=2.0.0
pandas>=1.3.0
numpy>=1.20.0
scipy>=1.7.0
plotly>=5.0.0
werkzeug>=2.0.0
jinja2>=3.0.0
markupsafe>=2.0.0
click>=8.0.0
itsdangerous>=2.0.0
```

### File Structure

The application's file structure is organized as follows:

```
NH3CrackProcessor/
├── app.py                  # Main Flask application entry point
├── Main_Web_ProcessorNH3Crack.py  # Core data processing implementation
├── config.py               # Configuration settings
├── process_all.py          # Script to process all experiments
├── fix_json_nan.py         # Utility to fix JSON files with NaN values
├── run.py                  # Script to run the application
├── quick_start.py          # Quick start utility
├── requirements.txt        # Python dependencies
├── ReadMe.md               # Documentation
├── Processors/             # Additional processing utilities
│   ├── fix_plots.py        # Utility to fix or regenerate plots
│   ├── test_paths.py       # Utility to test file paths
│   ├── test_server.py      # Server testing utilities
│   ├── setup_and_run.py    # Setup and deployment utilities
│   ├── test_connection.py  # Network connection test
│   ├── basic_app.py        # Simplified Flask app for testing
│   └── debug_app.py        # Debug version of the app
├── static/                 # Static web assets
│   ├── css/                # Stylesheet files
│   ├── js/                 # JavaScript files
│   └── images/             # Image assets
├── templates/              # Jinja2 HTML templates
│   ├── base.html           # Base template with common elements
│   ├── index.html          # Home page template
│   ├── experiment.html     # Experiment details page
│   ├── upload.html         # File upload page
│   ├── documentation.html  # Documentation page
│   └── error.html          # Error page template
├── uploads/                # Directory for raw data files
└── Reports/                # Directory for processed data and visualizations
```

### Core Components

#### 1. ExperimentalDataProcessor

The `ExperimentalDataProcessor` class in `Main_Web_ProcessorNH3Crack.py` is the core of the data processing pipeline. It handles:

- File reading and parsing
- Time vector creation
- Stage detection
- Data interpolation
- Plotly JSON generation
- Data export

Key methods:

```python
def process_file(self, filename):
    """Process a single file and generate all outputs"""
    # Read the file
    df = self.read_data_file(filename)
    
    # Create time vector
    df = self.create_time_vector(df)
    
    # Slice by stages
    stages = self.slice_by_stages(df)
    
    # Create column mapping
    column_mapping = self.create_column_mapping(df)
    
    # Process each stage
    processed_stages = {}
    for stage_num, stage_df in stages.items():
        # Interpolate data
        interpolated_df = self.perform_interpolation(stage_df)
        processed_stages[stage_num] = interpolated_df
    
    # Save data to files
    base_filename = os.path.splitext(filename)[0]
    self.save_stage_data(processed_stages, column_mapping, base_filename)
    
    # Create visualization files
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    exp_dir = os.path.join(self.output_folder, base_filename)
    self.create_plotly_json(processed_stages, base_filename, timestamp, exp_dir)
```

#### 2. Flask Application

The Flask application in `app.py` defines the web interface and API endpoints:

```python
# Routes
@app.route('/')
def index():
    """Main page with list of experiments"""
    experiments = get_experiments()
    return render_template('index.html', experiments=experiments)

@app.route('/experiment/<experiment_name>')
def experiment(experiment_name):
    """View a specific experiment"""
    decoded_name = urllib.parse.unquote(experiment_name)
    experiment_data = get_experiment_data(decoded_name)
    return render_template('experiment.html', experiment=experiment_data)

# API Routes
@app.route('/api/experiments')
def api_experiments():
    """API endpoint to get all experiments"""
    experiments = get_experiments()
    return jsonify(experiments)
```

#### 3. Configuration

The `config.py` file contains configuration settings for the application:

```python
# Data categories and their configurations
DATA_CATEGORIES = {
    "temperature": {
        "title": "Temperature Measurements",
        "y_axis_title": "Temperature (°C) / Power (%)",
        "columns": [
            "R1/2 T set [°C]", 
            "R1/2 T read [°C]", 
            "R1/2 T power [%]", 
            "Saturator T read [°C]"
        ],
        "filename_suffix": "temp_plotly_data.json"
    },
    # Additional categories...
}
```

### JSON to Plotly Visualization Handling

The application uses a two-step process to convert processed data to interactive Plotly visualizations:

1. **Backend (Python)**:
   - The `ExperimentalDataProcessor` class generates Plotly-compatible JSON files
   - These files contain both data (traces) and layout information

2. **Frontend (JavaScript)**:
   - The web interface loads these JSON files via the API
   - Plotly.js renders the JSON data as interactive visualizations

#### Backend JSON Generation

The backend generates several types of Plotly JSON files:

1. **Stage Plots**: One plot per experimental stage showing all measurements
2. **Category Plots**: Specialized plots for different measurement categories
3. **Overall Plot**: A combined plot showing key measurements across all stages

Example of JSON generation code:

```python
def create_stage_plotly_json(self, stage_df, stage_num, base_filename, output_dir):
    """Generate Plotly JSON files for a specific stage"""
    
    # Process each plot group
    for group_key, group_config in config.STAGE_PLOT_GROUPS.items():
        # Get the plot title and filename
        title = group_config['title'].format(stage_num=stage_num)
        filename = group_config['filename'].format(stage_num=stage_num)
        
        # Get columns to include in this plot
        if 'column_pattern' in group_config:
            # For multipoint thermocouples, find columns matching the pattern
            pattern = group_config['column_pattern']
            plot_cols = [col for col in stage_df.columns if pattern in col]
        else:
            # For regular plots, use the specified columns
            plot_cols = [col for col in group_config['columns'] if col in stage_df.columns]
        
        # Create traces for each column
        traces = []
        for i, col in enumerate(plot_cols):
            color = config.PLOT_COLORS[i % len(config.PLOT_COLORS)]
            trace = {
                'x': stage_df['Time_Minutes'].tolist(),
                'y': stage_df[col].tolist(),
                'type': 'scatter',
                'mode': 'lines',
                'name': col,
                'line': {'color': color, 'width': 2}
            }
            traces.append(trace)
        
        # Create layout
        layout = {
            'title': title,
            'xaxis': {
                'title': 'Time (minutes)',
                'gridcolor': config.PLOTLY_GRID_COLOR
            },
            'yaxis': {
                'title': group_config['y_axis_title'],
                'gridcolor': config.PLOTLY_GRID_COLOR
            },
            'template': config.PLOTLY_THEME,
            'paper_bgcolor': config.PLOTLY_PAPER_BGCOLOR,
            'plot_bgcolor': config.PLOTLY_PLOT_BGCOLOR,
            'font': {'color': config.PLOTLY_FONT_COLOR},
            'hovermode': 'closest',
            'legend': {
                'orientation': 'v',
                'bgcolor': 'rgba(0,0,0,0.5)',
                'bordercolor': 'rgba(255,255,255,0.2)',
                'borderwidth': 1
            }
        }
        
        # Create Plotly data
        plotly_data = {
            'data': traces,
            'layout': layout
        }
        
        # Save to file
        output_path = os.path.join(output_dir, filename)
        with open(output_path, 'w') as f:
            json.dump(plotly_data, f, indent=2, cls=CustomJSONEncoder)
```

#### Frontend Rendering

The frontend renders the JSON data using Plotly.js:

```javascript
// Load plot data from API
async function loadPlotData(experimentName, plotType, stageNum = null) {
    let url;
    
    if (stageNum) {
        url = `/api/experiment/${encodeURIComponent(experimentName)}/stage/${stageNum}?type=${plotType}`;
    } else {
        url = `/api/experiment/${encodeURIComponent(experimentName)}/overall?type=${plotType}`;
    }
    
    const response = await fetch(url);
    const plotData = await response.json();
    
    // Render the plot
    Plotly.newPlot('plot-container', plotData.data, plotData.layout, {
        responsive: true,
        displayModeBar: true
    });
}
```

### Data Flow

The data flow through the application is as follows:

1. **Data Input**:
   - User uploads a tab-separated text file to the uploads folder
   - The application reads the file and parses it into a pandas DataFrame

2. **Data Processing**:
   - The application creates a time vector in minutes
   - The application detects experimental stages
   - The application performs cubic interpolation for all numeric columns
   - The application organizes the data into different categories

3. **Data Storage**:
   - The application saves the processed data to CSV and JSON files
   - The application generates Plotly JSON files for visualization

4. **Data Access**:
   - User accesses the data through the web interface
   - The web interface loads the Plotly JSON files via the API
   - Plotly.js renders the JSON data as interactive visualizations

5. **Data Export**:
   - User can export the visualizations as PNG images
   - User can download the processed data in CSV or JSON format

### NaN Handling

JSON does not support NaN (Not a Number) values, which can cause issues when the data contains missing or invalid measurements. The application uses a custom JSON encoder to handle NaN values:

```python
class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (np.integer, np.floating, np.bool_)):
            return obj.item()
        if pd.isna(obj):
            return None
        if np.isnan(obj):
            return None
        if np.isinf(obj):
            return None
        return super().default(obj)
```

This encoder converts NaN values to `null`, which is a valid JSON value and can be properly handled by JavaScript.

### Handling Large Files

For large experimental data files, the application may encounter memory or performance issues. The application includes several optimizations to handle large files:

1. **Chunked Reading**: For very large files, the application can read the file in chunks:

```python
def read_large_file(self, filename, chunksize=10000):
    """Read a large file in chunks"""
    filepath = os.path.join(self.input_folder, filename)
    
    # Try multiple encodings
    for encoding in config.FILE_ENCODINGS:
        try:
            chunks = []
            for chunk in pd.read_csv(filepath, sep='\t', encoding=encoding, chunksize=chunksize):
                chunks.append(chunk)
            
            # Combine chunks
            df = pd.concat(chunks, ignore_index=True)
            return df
        except Exception as e:
            continue
    
    return None
```

2. **Selective Interpolation**: For files with many columns, the application can selectively interpolate only the necessary columns:

```python
def selective_interpolation(self, df, columns_to_interpolate, target_interval_minutes=1):
    """Interpolate only specific columns"""
    # Create target time vector
    time_min = df['Time_Minutes'].min()
    time_max = df['Time_Minutes'].max()
    target_time = np.arange(time_min, time_max + target_interval_minutes, target_interval_minutes)
    
    # Create new dataframe
    interpolated_df = pd.DataFrame({'Time_Minutes': target_time})
    
    # Interpolate only the specified columns
    for col in columns_to_interpolate:
        if col in df.columns and col != 'Time_Minutes' and col != 'Stage':
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
    
    return interpolated_df
```

3. **Downsampling**: For visualizations, the application can downsample the data to reduce the size of the JSON files:

```python
def downsample_for_visualization(self, df, target_points=1000):
    """Downsample data for visualization"""
    if len(df) <= target_points:
        return df
    
    # Calculate stride
    stride = max(1, len(df) // target_points)
    
    # Downsample
    return df.iloc[::stride].copy()
```

### Error Handling

The application includes comprehensive error handling to gracefully handle issues with data processing and visualization:

1. **File Reading Errors**:
   - The application tries multiple encodings to read the file
   - If all fail, it returns a clear error message

2. **Time Vector Creation Errors**:
   - The application tries multiple date formats
   - If all fail, it falls back to a sequential time vector

3. **Interpolation Errors**:
   - The application checks for sufficient data points before interpolation
   - If not enough points, it skips interpolation for that column

4. **Visualization Errors**:
   - The application checks for the existence of required columns
   - If columns are missing, it skips the corresponding visualizations

5. **API Error Handling**:
   - The API returns appropriate HTTP status codes and error messages
   - The frontend gracefully handles API errors with user-friendly messages

Example of API error handling:

```python
@app.route('/api/experiment/<experiment_name>/overall')
def api_experiment_overall(experiment_name):
    """API endpoint for overall experiment plot data"""
    try:
        # URL decode the experiment name
        decoded_name = urllib.parse.unquote(experiment_name)
        
        # Get plot type from query parameters
        plot_type = request.args.get('type', 'temperature')
        
        # Check if the requested plot type is valid
        if plot_type not in plot_type_map:
            return jsonify({
                "error": f"Invalid plot type: {plot_type}",
                "available_types": list(plot_type_map.keys())
            }), 400
        
        # Get the filename for the requested plot type
        filename = plot_type_map[plot_type]
        
        # Check for overall plotly file
        exp_dir = os.path.join(app.config['REPORTS_FOLDER'], decoded_name)
        plotly_path = os.path.join(exp_dir, filename)
        
        if not os.path.exists(plotly_path):
            # If the specific plot doesn't exist, list available plots
            available_plots = []
            for plot_key, plot_name in plot_type_map.items():
                test_path = os.path.join(exp_dir, plot_name)
                if os.path.exists(test_path):
                    available_plots.append(plot_key)
            
            if not available_plots:
                return jsonify({
                    "error": "No plot data found. Try regenerating visualizations."
                }), 404
            else:
                return jsonify({
                    "error": f"Plot type '{plot_type}' not found",
                    "available_types": available_plots
                }), 404
        
        with open(plotly_path, 'r') as f:
            plot_data = json.load(f)
        
        return jsonify(plot_data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
```

### Performance Considerations

The application is designed to handle large experimental datasets efficiently. Here are some performance considerations:

1. **Memory Usage**:
   - For very large files, use chunked reading
   - Selectively interpolate only necessary columns
   - Downsample data for visualization

2. **Processing Speed**:
   - Use NumPy for numerical operations
   - Use SciPy for efficient interpolation
   - Use pandas for data manipulation

3. **Web Interface Performance**:
   - Load only necessary data on demand
   - Use efficient API endpoints
   - Implement pagination for large datasets

4. **Visualization Performance**:
   - Downsample data for visualization
   - Use efficient Plotly.js rendering
   - Implement progressive loading for large plots

### Security Considerations

The application includes several security features:

1. **File Upload Security**:
   - Validate file extensions
   - Limit file size
   - Sanitize filenames

```python
def allowed_file(filename):
    """Check if a file has an allowed extension"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/upload', methods=['POST'])
def upload_file():
    """Upload a file to the uploads folder"""
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
```

2. **API Security**:
   - Input validation
   - Error handling
   - Rate limiting (if needed)

3. **Data Security**:
   - Sanitize data before storage
   - Validate data before processing
   - Handle NaN values properly

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

## Recent Updates

### Data Gap Filtering Enhancement (2024-05-31)
- Added intelligent gap filtering during data interpolation:
  - The system now detects and excludes time points that are too far from original data points
  - Prevents extrapolation across large time gaps where no measurements exist
  - Configurable gap threshold (default: 5 minutes)
  - Improves data quality by avoiding spurious interpolated values
  - Preserves the integrity of the original measurement points

### Import System Enhancement (2024-05-30)
- Improved the import system in utility scripts to ensure proper module resolution:
  - `process_all.py` now dynamically resolves module imports
  - `fix_json_nan.py` now includes fallback import options
  - Both scripts now include error handling for import exceptions
  - Path resolution is improved to work in different execution contexts

### Documentation Styling Enhancement (2024-05-30)
- Added modern card-based styling to the documentation section:
  - Each documentation section now appears in a visually distinct card
  - Cards feature color-coded borders and headers
  - Improved typography and spacing for better readability
  - Added visual container styling for code diagrams and examples

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