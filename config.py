"""
NH3 Cracking Processor and Visualizer Configuration
--------------------------------------------------
This file contains configuration settings for the NH3 Cracking application.
"""

import os

# Application settings
APP_NAME = "NH3 Cracking Processor and Visualizer"
DEBUG_MODE = True
HOST = "0.0.0.0"
PORT = 8080
VERSION = "1.0.0"

# Directory settings
UPLOAD_FOLDER = "uploads"
REPORTS_FOLDER = "reports"
MAX_CONTENT_LENGTH = 300 * 1024 * 1024  # 300 MB max upload size
ALLOWED_EXTENSIONS = {"txt"}

# Ensure necessary directories exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(REPORTS_FOLDER, exist_ok=True)

# Visualization settings
PLOTLY_THEME = "plotly_dark"
PLOTLY_PAPER_BGCOLOR = "#1e1e1e"
PLOTLY_PLOT_BGCOLOR = "#2d2d2d"
PLOTLY_FONT_COLOR = "#e0e0e0"
PLOTLY_GRID_COLOR = "rgba(255, 255, 255, 0.1)"

# Plot colors for different stages
PLOT_COLORS = [
    "#ff6e6e",  # Red
    "#5c9eff",  # Blue
    "#6dff6d",  # Green
    "#ffdd5c",  # Yellow
    "#ca6dff",  # Purple
    "#ff9e4a",  # Orange
    "#4adfff",  # Cyan
    "#ff4adf",  # Magenta
]

# Data categories and their configurations
DATA_CATEGORIES = {
    "temperature": {
        "title": "Temperature Measurements",
        "y_axis_title": "Temperature (°C) / Power (%)",
        "columns": [
            "R1/2 T set [\u00b0C]", 
            "R1/2 T read [\u00b0C]", 
            "R1/2 T power [%]", 
            "Saturator T read [\u00b0C]"
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
        "columns": ["Saturator T read [\u00b0C]"],
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

# Stage plot configuration for individual stages
STAGE_PLOT_GROUPS = {
    "temperature": {
        "title": "Stage {stage_num} - Temperature",
        "columns": [
            "R1/2 T set [\u00b0C]", 
            "R1/2 T read [\u00b0C]", 
            "R1/2 T power [%]", 
            "Saturator T read [\u00b0C]"
        ],
        "y_axis_title": "Temperature (°C) / Power (%)",
        "filename": "stage_{stage_num}_temp_plotly.json"
    },
    "multipoint_temp": {
        "title": "Stage {stage_num} - Multipoint Thermocouples",
        "column_pattern": "R-1/2 T",
        "y_axis_title": "Temperature (°C)",
        "filename": "stage_{stage_num}_multipoint_temp_plotly.json"
    },
    "saturator_temp": {
        "title": "Stage {stage_num} - Saturator Temperature",
        "columns": ["Saturator T read [\u00b0C]"],
        "y_axis_title": "Temperature (°C)",
        "filename": "stage_{stage_num}_saturator_temp_plotly.json"
    },
    "pressure": {
        "title": "Stage {stage_num} - Pressure",
        "columns": [
            "Pressure SETPOINT [bar]", 
            "Pressure PIC [bar]", 
            "Pressure reading line [bar]",
            "Pressure reading R1/2 IN [bar]", 
            "Pressure reading R1/2 OUT [bar]", 
            "High pressure NH3 line [bar]"
        ],
        "y_axis_title": "Pressure (bar)",
        "filename": "stage_{stage_num}_pressure_plotly.json"
    },
    "flow": {
        "title": "Stage {stage_num} - Flow",
        "columns": [
            "NH3 Actual Set-Point [Nml/min]", 
            "H2 Actual Flow [Nml/min]", 
            "Tot flow calc [Nml/min]",
            "NH3 in %", 
            "Inert in %", 
            "H2O in %"
        ],
        "y_axis_title": "Flow (Nml/min) / Concentration (%)",
        "filename": "stage_{stage_num}_flow_plotly.json"
    },
    "outlet": {
        "title": "Stage {stage_num} - Outlet Stream",
        "columns": [
            "NH3 out [%]", 
            "H2 out [%]", 
            "H2O out [%]"
        ],
        "y_axis_title": "Concentration (%)",
        "filename": "stage_{stage_num}_outlet_plotly.json"
    }
}

# File processing settings
DATE_FORMATS = [
    '%d/%m/%y %H:%M:%S',    # DD/MM/YY HH:MM:SS
    '%Y-%m-%d %H:%M:%S',    # YYYY-MM-DD HH:MM:SS
    '%d/%m/%Y %H:%M:%S',    # DD/MM/YYYY HH:MM:SS
    '%m/%d/%y %H:%M:%S',    # MM/DD/YY HH:MM:SS
    '%m/%d/%Y %H:%M:%S',    # MM/DD/YYYY HH:MM:SS
]

# File encoding options
FILE_ENCODINGS = ['utf-8', 'latin1', 'cp1252', 'ISO-8859-1']

# Interpolation settings
INTERPOLATION_TARGET_INTERVAL = 1  # 1 minute intervals
INTERPOLATION_MIN_POINTS = 4  # Minimum points required for cubic interpolation
MAX_GAP_MINUTES = 5  # Maximum gap in minutes to consider for interpolation

# File encoding options
FILE_ENCODINGS = ['utf-8', 'latin1', 'cp1252', 'ISO-8859-1'] 