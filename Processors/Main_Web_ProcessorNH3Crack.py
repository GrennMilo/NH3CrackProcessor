import pandas as pd
import numpy as np
from scipy.interpolate import interp1d
import json
import os
import sys
from datetime import datetime, timedelta
import plotly.graph_objects as go
from plotly.utils import PlotlyJSONEncoder

# Add the parent directory to sys.path to import config
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config

# Custom JSON encoder to handle NaN values
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

class ExperimentalDataProcessor:
    def __init__(self, input_folder="uploads", output_folder="Reports"):
        self.input_folder = input_folder
        self.output_folder = output_folder
        self.ensure_folders_exist()
        
    def ensure_folders_exist(self):
        """Create folders if they don't exist"""
        os.makedirs(self.input_folder, exist_ok=True)
        os.makedirs(self.output_folder, exist_ok=True)
    
    def read_data_file(self, filename):
        """Read the experimental data file with multiple encoding attempts"""
        filepath = os.path.join(self.input_folder, filename)
        
        # Try multiple encodings
        encodings = ['utf-8', 'latin1', 'cp1252', 'ISO-8859-1']
        
        for encoding in encodings:
            try:
                # Read the file with tab separator
                df = pd.read_csv(filepath, sep='\t', encoding=encoding)
                print(f"Successfully loaded data with {len(df)} rows and {len(df.columns)} columns using {encoding} encoding")
                print(f"Columns: {list(df.columns)}")
                return df
            except UnicodeDecodeError:
                print(f"Failed with encoding {encoding}, trying next...")
                continue
            except Exception as e:
                print(f"Error reading file with {encoding} encoding: {e}")
                # If it's not an encoding error, don't try other encodings
                if not isinstance(e, UnicodeDecodeError):
                    break
        
        print(f"Error reading file: Failed with all encodings")
        return None
    
    def create_time_vector(self, df):
        """Create a proper time vector from the datetime column and track original timestamps"""
        # Assume first column is datetime
        datetime_col = df.columns[0]
        
        try:
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
                    
                    # If conversion succeeded, break the loop
                    break
                except ValueError:
                    continue
            
            # If still not converted, try without specifying format
            if not pd.api.types.is_datetime64_any_dtype(df[datetime_col]):
                df[datetime_col] = pd.to_datetime(df[datetime_col], errors='coerce')
            
            # Create time vector in minutes from start
            start_time = df[datetime_col].min()
            df['Time_Minutes'] = (df[datetime_col] - start_time).dt.total_seconds() / 60
            
            # Store the original timestamps to track real vs interpolated data
            df['Original_Point'] = True
            
            return df
        except Exception as e:
            print(f"Error processing datetime: {e}")
            # Fallback: create sequential time vector
            df['Time_Minutes'] = np.arange(len(df))
            df['Original_Point'] = True
            return df
    
    def perform_interpolation(self, df, target_interval_minutes=1):
        """Perform cubic interpolation for all numeric columns and mark original points"""
        # Create target time vector with 1-minute intervals
        time_min = df['Time_Minutes'].min()
        time_max = df['Time_Minutes'].max()
        target_time = np.arange(time_min, time_max + target_interval_minutes, target_interval_minutes)
        
        # Create new dataframe for interpolated data
        interpolated_df = pd.DataFrame({'Time_Minutes': target_time})
        
        # Add a column to track which points are original vs interpolated
        # Initially mark all as interpolated (False)
        interpolated_df['Original_Point'] = False
        
        # Mark points that are within a small threshold of original data points
        threshold = target_interval_minutes / 10  # 1/10th of the interval as threshold
        for original_time in df['Time_Minutes']:
            mask = abs(interpolated_df['Time_Minutes'] - original_time) < threshold
            interpolated_df.loc[mask, 'Original_Point'] = True
        
        # Get numeric columns (excluding time and stage columns)
        numeric_columns = df.select_dtypes(include=[np.number]).columns.tolist()
        exclude_cols = ['Time_Minutes', 'Original_Point']
        if 'Stage' in df.columns:
            exclude_cols.append('Stage')
        
        numeric_columns = [col for col in numeric_columns if col not in exclude_cols]
        
        # Interpolate each numeric column
        for col in numeric_columns:
            try:
                # Remove NaN values for interpolation
                mask = ~(df['Time_Minutes'].isna() | df[col].isna())
                if mask.sum() > 3:  # Need at least 4 points for cubic interpolation
                    x = df.loc[mask, 'Time_Minutes'].values
                    y = df.loc[mask, col].values
                    
                    # Create interpolation function
                    f = interp1d(x, y, kind='cubic', bounds_error=False, fill_value='extrapolate')
                    interpolated_df[col] = f(target_time)
                else:
                    print(f"Warning: Not enough data points for cubic interpolation of {col}")
                    interpolated_df[col] = np.nan
            except Exception as e:
                print(f"Error interpolating {col}: {e}")
                interpolated_df[col] = np.nan
        
        # Handle Stage column separately (use nearest neighbor)
        if 'Stage' in df.columns:
            try:
                mask = ~(df['Time_Minutes'].isna() | df['Stage'].isna())
                if mask.sum() > 0:
                    x = df.loc[mask, 'Time_Minutes'].values
                    y = df.loc[mask, 'Stage'].values
                    f_stage = interp1d(x, y, kind='nearest', bounds_error=False, fill_value='extrapolate')
                    interpolated_df['Stage'] = f_stage(target_time).astype(int)
                else:
                    interpolated_df['Stage'] = 0
            except Exception as e:
                print(f"Error interpolating Stage: {e}")
                interpolated_df['Stage'] = 0
        
        # Add the original datetime values for points that match original data
        if df.columns[0] in df.columns:
            datetime_col = df.columns[0]
            interpolated_df[datetime_col] = None
            
            # For each original point, find the closest interpolated point and copy the datetime
            for idx, row in df.iterrows():
                closest_idx = abs(interpolated_df['Time_Minutes'] - row['Time_Minutes']).idxmin()
                interpolated_df.loc[closest_idx, datetime_col] = row[datetime_col]
        
        # If configured to exclude interpolated points in config
        if hasattr(config, 'EXCLUDE_INTERPOLATED_POINTS') and config.EXCLUDE_INTERPOLATED_POINTS:
            return interpolated_df[interpolated_df['Original_Point']]
        
        return interpolated_df
    
    def slice_by_stages(self, df):
        """
        Slice data by stages using the second column 'Stage' to identify different stages.
        This column is expected to be present in the tab-delimited input file.
        """
        # Ensure the Stage column exists
        if 'Stage' not in df.columns:
            # Look for stage column in second position (index 1)
            if len(df.columns) > 1:
                stage_col = df.columns[1]
                print(f"Using column '{stage_col}' as the Stage identifier")
                df.rename(columns={stage_col: 'Stage'}, inplace=True)
            else:
                print("Warning: No Stage column found. Creating single stage.")
                df['Stage'] = 1
                return {1: df}
        
        # Group data by stage values
        stages = {}
        stage_groups = df.groupby('Stage')
        
        for stage_num, stage_data in stage_groups:
            stages[int(stage_num)] = stage_data.copy()
        
        print(f"Found {len(stages)} stages: {list(stages.keys())}")
        return stages
    
    def create_column_mapping(self, df):
        """Create a mapping of all columns with their properties"""
        column_mapping = {}
        
        for col in df.columns:
            col_info = {
                'index': df.columns.get_loc(col),
                'dtype': str(df[col].dtype),
                'non_null_count': df[col].count(),
                'null_count': df[col].isnull().sum(),
                'unique_values': df[col].nunique() if df[col].dtype in ['object', 'category'] else None
            }
            
            # Add statistics for numeric columns
            if df[col].dtype in ['int64', 'float64']:
                col_info.update({
                    'min': float(df[col].min()) if not df[col].isnull().all() else None,
                    'max': float(df[col].max()) if not df[col].isnull().all() else None,
                    'mean': float(df[col].mean()) if not df[col].isnull().all() else None,
                    'std': float(df[col].std()) if not df[col].isnull().all() else None
                })
            
            column_mapping[col] = col_info
        
        return column_mapping
    
    def save_stage_data(self, stages, column_mapping, base_filename):
        """Save stage data in multiple formats with a proper folder structure"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Create experiment directory in Reports folder
        exp_dir = os.path.join(self.output_folder, base_filename)
        os.makedirs(exp_dir, exist_ok=True)
        
        # Save complete dataset summary
        summary = {
            'metadata': {
                'processed_at': datetime.now().isoformat(),
                'total_stages': len(stages),
                'stage_numbers': list(stages.keys()),
                'base_filename': base_filename
            },
            'column_mapping': column_mapping,
            'stages_info': {}
        }
        
        # Process each stage
        all_stages_data = {}
        
        for stage_num, stage_df in stages.items():
            stage_info = {
                'row_count': len(stage_df),
                'time_range': {
                    'start': float(stage_df['Time_Minutes'].min()),
                    'end': float(stage_df['Time_Minutes'].max()),
                    'duration': float(stage_df['Time_Minutes'].max() - stage_df['Time_Minutes'].min())
                }
            }
            summary['stages_info'][stage_num] = stage_info
            
            # Convert DataFrame to dict for JSON serialization
            stage_data = {}
            for col in stage_df.columns:
                stage_data[col] = stage_df[col].tolist()
            
            all_stages_data[f"stage_{stage_num}"] = stage_data
            
            # Create stage directory inside experiment directory
            stage_dir = os.path.join(exp_dir, f"stage_{stage_num}")
            os.makedirs(stage_dir, exist_ok=True)
            
            # Save individual stage CSV
            csv_filename = f"stage_{stage_num}_data.csv"
            csv_path = os.path.join(stage_dir, csv_filename)
            stage_df.to_csv(csv_path, index=False)
            print(f"Saved Stage {stage_num} CSV: {csv_path}")
            
            # Save individual stage JSON
            json_filename = f"stage_{stage_num}_data.json"
            json_path = os.path.join(stage_dir, json_filename)
            with open(json_path, 'w') as f:
                json.dump(stage_data, f, indent=2, cls=CustomJSONEncoder)
            print(f"Saved Stage {stage_num} JSON: {json_path}")
            
            # Create Plotly JSON files for stage with different plots
            self.create_stage_plotly_json(stage_df, stage_num, base_filename, stage_dir)
            print(f"Saved Stage {stage_num} Plotly JSON files in: {stage_dir}")
        
        # Save summary JSON in experiment directory
        summary_path = os.path.join(exp_dir, "experiment_summary.json")
        with open(summary_path, 'w') as f:
            json.dump(summary, f, indent=2, cls=CustomJSONEncoder)
        print(f"Saved experiment summary: {summary_path}")
        
        # Save complete JSON with all stages
        json_filename = f"{base_filename}_all_stages.json"
        json_path = os.path.join(exp_dir, json_filename)
        complete_data = {
            'summary': summary,
            'data': all_stages_data
        }
        
        with open(json_path, 'w') as f:
            json.dump(complete_data, f, indent=2, cls=CustomJSONEncoder)
        print(f"Saved complete JSON: {json_path}")
        
        # Save complete CSV (all stages)
        complete_csv_filename = f"{base_filename}_complete.csv"
        complete_csv_path = os.path.join(exp_dir, complete_csv_filename)
        complete_df = pd.concat([df.assign(Stage_ID=stage) for stage, df in stages.items()])
        complete_df.to_csv(complete_csv_path, index=False)
        print(f"Saved complete CSV: {complete_csv_path}")
        
        # Create Plotly-compatible JSON files with different plots for all stages
        self.create_plotly_json(stages, base_filename, timestamp, exp_dir)
        print(f"Saved overall Plotly JSON files in: {exp_dir}")
    
    def create_stage_plotly_json(self, stage_df, stage_num, base_filename, output_dir):
        """Create multiple Plotly-compatible JSON files for a single stage with focused plots"""
        # Create base title
        base_title = f'Stage {stage_num} - {base_filename}'
        
        # Use plot groups from config
        plot_groups = config.STAGE_PLOT_GROUPS
        
        # Create a plot for each group
        for group_name, group_info in plot_groups.items():
            # Filter columns that exist in the dataframe
            if 'column_pattern' in group_info:
                available_columns = [col for col in stage_df.columns if 
                                    group_info['column_pattern'] in col and col.endswith('\u00b0C')]
            else:
                available_columns = [col for col in group_info['columns'] if col in stage_df.columns]
            
            if not available_columns:
                print(f"Warning: No columns found for {group_name} plot in stage {stage_num}")
                continue
            
            # Create traces for each column
            traces = []
            for col in available_columns:
                # Filter by original points if configured to do so
                if hasattr(config, 'PLOT_ONLY_ORIGINAL_POINTS') and config.PLOT_ONLY_ORIGINAL_POINTS:
                    # Filter to original points only and exclude NaN values
                    valid_data = stage_df['Original_Point'] & ~stage_df[col].isna()
                else:
                    # Just filter out NaN values
                    valid_data = ~stage_df[col].isna()
                
                trace = {
                    'x': stage_df.loc[valid_data, 'Time_Minutes'].tolist(),
                    'y': stage_df.loc[valid_data, col].tolist(),
                    'type': 'scatter',
                    'mode': 'lines+markers' if config.PLOT_ONLY_ORIGINAL_POINTS else 'lines',
                    'name': col
                }
                traces.append(trace)
            
            # Create layout
            layout = {
                'title': group_info['title'].format(stage_num=stage_num),
                'xaxis': {'title': 'Time (minutes)'},
                'yaxis': {'title': group_info['y_axis_title']},
                'hovermode': 'closest',
                'template': 'plotly_dark',
                'legend': {'orientation': 'h', 'y': -0.2}
            }
            
            # Create Plotly data
            plotly_data = {
                'data': traces,
                'layout': layout
            }
            
            # Save to file
            output_path = os.path.join(output_dir, group_info['filename'].format(stage_num=stage_num))
            with open(output_path, 'w') as f:
                json.dump(plotly_data, f, indent=2, cls=CustomJSONEncoder)
    
    def create_plotly_json(self, stages, base_filename, timestamp, output_dir):
        """Create multiple Plotly-compatible JSON files for all stages with focused plots"""
        # Define column groups for different plots
        plot_groups = {
            'temperature': {
                'title': f'Temperature Data - {base_filename}',
                'columns': ['R1/2 T set [\u00b0C]', 'R1/2 T read [\u00b0C]', 'R1/2 T power [%]', 'Saturator T read [\u00b0C]'],
                'yaxis_title': 'Temperature (°C) / Power (%)',
                'filename': f'{base_filename}_temp_plotly_data.json'
            },
            'multipoint_temp': {
                'title': f'Multipoint Thermocouples - {base_filename}',
                'column_pattern': 'R-1/2 T',
                'yaxis_title': 'Temperature (°C)',
                'filename': f'{base_filename}_multipoint_temp_plotly_data.json'
            },
            'saturator_temp': {
                'title': f'Saturator Temperature - {base_filename}',
                'columns': ['Saturator T read [\u00b0C]'],
                'yaxis_title': 'Temperature (°C)',
                'filename': f'{base_filename}_saturator_temp_plotly_data.json'
            },
            'pressure': {
                'title': f'Pressure Data - {base_filename}',
                'columns': [
                    'Pressure SETPOINT [bar]', 'Pressure PIC [bar]', 'Pressure reading line [bar]',
                    'Pressure reading R1/2 IN [bar]', 'Pressure reading R1/2 OUT [bar]', 'High pressure NH3 line [bar]'
                ],
                'yaxis_title': 'Pressure (bar)',
                'filename': f'{base_filename}_pressure_plotly_data.json'
            },
            'flow': {
                'title': f'Flow Data - {base_filename}',
                'columns': [
                    'NH3 Actual Set-Point [Nml/min]', 'H2 Actual Flow [Nml/min]', 'Tot flow calc [Nml/min]',
                    'NH3 in %', 'Inert in %', 'H2O in %'
                ],
                'yaxis_title': 'Flow (Nml/min) / Concentration (%)',
                'filename': f'{base_filename}_flow_plotly_data.json'
            },
            'outlet': {
                'title': f'Outlet Stream - {base_filename}',
                'columns': ['NH3 out [%]', 'H2 out [%]', 'H2O out [%]'],
                'yaxis_title': 'Concentration (%)',
                'filename': f'{base_filename}_outlet_plotly_data.json'
            }
        }
        
        # Colors for different stages
        colors = ['red', 'blue', 'green', 'orange', 'purple', 'brown', 'pink', 'gray', 
                 'cyan', 'magenta', 'yellow', 'teal', 'navy', 'olive', 'maroon', 'lime']
        
        # Create a plot for each group
        for group_name, group_info in plot_groups.items():
            plotly_data = {
                'metadata': {
                    'title': group_info['title'],
                    'processed_at': datetime.now().isoformat(),
                    'total_stages': len(stages)
                },
                'data': [],
                'layout': {
                    'title': group_info['title'],
                    'xaxis': {'title': 'Time (minutes)'},
                    'yaxis': {'title': group_info['yaxis_title']},
                    'hovermode': 'closest',
                    'template': 'plotly_dark',
                    'legend': {'orientation': 'h', 'y': -0.2}
                }
            }
            
            for i, (stage_num, stage_df) in enumerate(stages.items()):
                color = colors[i % len(colors)]
                
                # Special handling for multipoint temperature columns
                if group_name == 'multipoint_temp':
                    available_columns = [col for col in stage_df.columns if 
                                        col.startswith('R-1/2 T') and col.endswith('\u00b0C')]
                else:
                    # Filter columns that exist in the dataframe
                    available_columns = [col for col in group_info['columns'] if col in stage_df.columns]
                
                if not available_columns:
                    print(f"Warning: No columns found for {group_name} plot in stage {stage_num}")
                    continue
                
                # Create traces for each column
                for col in available_columns:
                    # Filter by original points if configured to do so
                    if hasattr(config, 'PLOT_ONLY_ORIGINAL_POINTS') and config.PLOT_ONLY_ORIGINAL_POINTS:
                        # Filter to original points only and exclude NaN values
                        valid_data = stage_df['Original_Point'] & ~stage_df[col].isna()
                    else:
                        # Just filter out NaN values
                        valid_data = ~stage_df[col].isna()
                    
                    trace = {
                        'x': stage_df.loc[valid_data, 'Time_Minutes'].tolist(),
                        'y': stage_df.loc[valid_data, col].tolist(),
                        'type': 'scatter',
                        'mode': 'lines+markers' if config.PLOT_ONLY_ORIGINAL_POINTS else 'lines',
                        'name': f'Stage {stage_num} - {col}',
                        'line': {'color': color},
                        'legendgroup': f'stage_{stage_num}'
                    }
                    plotly_data['data'].append(trace)
            
            # Only save if there's data
            if plotly_data['data']:
                # Save Plotly JSON
                output_path = os.path.join(output_dir, group_info['filename'])
                with open(output_path, 'w') as f:
                    json.dump(plotly_data, f, indent=2, cls=CustomJSONEncoder)
            else:
                print(f"Warning: No data available for {group_name} plot")
    
    def create_category_plotly_jsons(self, stages, base_filename, timestamp, exp_dir):
        """Create specialized Plotly-compatible JSON files for different data categories"""
        # Use data categories defined in the config file
        categories = config.DATA_CATEGORIES
        
        # Create a separate plot for each category
        for category_name, category_config in categories.items():
            # Create a plot data object
            title = f"{category_config['title']} - {base_filename}"
            
            # Define bright colors for better visibility on dark background
            colors = config.PLOT_COLORS
            
            # Create traces
            traces = []
            
            for i, (stage_num, stage_df) in enumerate(stages.items()):
                # Skip stages with no data for this category
                has_data = False
                
                # Special handling for multipoint temperature columns or other pattern-based categories
                if 'column_pattern' in category_config:
                    available_columns = [col for col in stage_df.columns if 
                                         category_config['column_pattern'] in col and col.endswith('\u00b0C')]
                else:
                    # Filter columns that exist in the dataframe
                    available_columns = [col for col in category_config['columns'] if col in stage_df.columns]
                
                if not available_columns:
                    continue
                
                # Assign a color for this stage
                stage_color = colors[i % len(colors)]
                
                # Create a trace for each column in this category
                for col in available_columns:
                    # Filter by original points if configured to do so
                    if hasattr(config, 'PLOT_ONLY_ORIGINAL_POINTS') and config.PLOT_ONLY_ORIGINAL_POINTS:
                        # Filter to original points only and exclude NaN values
                        valid_data = stage_df['Original_Point'] & ~stage_df[col].isna()
                    else:
                        # Just filter out NaN values
                        valid_data = ~stage_df[col].isna()
                    
                    trace = {
                        'x': stage_df.loc[valid_data, 'Time_Minutes'].tolist(),
                        'y': stage_df.loc[valid_data, col].tolist(),
                        'type': 'scatter',
                        'mode': 'lines+markers' if config.PLOT_ONLY_ORIGINAL_POINTS else 'lines',
                        'name': f'Stage {stage_num} - {col}',
                        'line': {'color': stage_color, 'width': 2},
                        'legendgroup': f'stage_{stage_num}'
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
                    'title': category_config['y_axis_title'],
                    'gridcolor': config.PLOTLY_GRID_COLOR
                },
                'hovermode': 'closest',
                'template': config.PLOTLY_THEME,
                'paper_bgcolor': config.PLOTLY_PAPER_BGCOLOR,
                'plot_bgcolor': config.PLOTLY_PLOT_BGCOLOR,
                'font': {'color': config.PLOTLY_FONT_COLOR},
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
            
            # Skip if no data
            if not traces:
                print(f"Warning: No data found for category '{category_name}'")
                continue
            
            # Save the category plot
            plot_filename = f"{base_filename}_{category_config['filename_suffix']}"
            plot_path = os.path.join(exp_dir, plot_filename)
            
            with open(plot_path, 'w') as f:
                json.dump(plotly_data, f, indent=2, cls=CustomJSONEncoder)
            
            print(f"Saved {category_name} plot: {plot_path}")
        
        # Create overall plot with all stages and categories
        self.create_plotly_json(stages, base_filename, timestamp, os.path.join(exp_dir, f"{base_filename}_plotly_data.json"))
    
    def process_file(self, filename):
        """Main processing function"""
        print(f"Processing file: {filename}")
        
        # Read data
        df = self.read_data_file(filename)
        if df is None:
            print(f"Failed to process file: {filename}")
            return
        
        # Create time vector
        df = self.create_time_vector(df)
        
        # Ensure Stage column exists (should be the second column)
        if 'Stage' not in df.columns and len(df.columns) > 1:
            # Use the second column as the Stage identifier
            stage_col = df.columns[1]
            print(f"Using column '{stage_col}' as the Stage identifier")
            df.rename(columns={stage_col: 'Stage'}, inplace=True)
        elif 'Stage' not in df.columns:
            print("Warning: No suitable Stage column found. Creating single stage.")
            df['Stage'] = 1
        
        # Perform interpolation
        print("Performing cubic interpolation...")
        interpolated_df = self.perform_interpolation(df)
        
        # Create column mapping
        column_mapping = self.create_column_mapping(interpolated_df)
        
        # Slice by stages
        print("Slicing data by stages using the Stage column...")
        stages = self.slice_by_stages(interpolated_df)
        
        # Save data
        base_filename = os.path.splitext(filename)[0]
        self.save_stage_data(stages, column_mapping, base_filename)
        
        print("Processing completed successfully!")
        
    def fix_plotly_json_files(self, experiment_name):
        """Fix existing Plotly JSON files by removing NaN values"""
        print(f"Fixing Plotly JSON files for {experiment_name}")
        
        # Get experiment directory
        exp_dir = os.path.join(self.output_folder, experiment_name)
        if not os.path.exists(exp_dir):
            print(f"Error: Experiment directory not found at {exp_dir}")
            return False
        
        # Find all JSON files in the experiment directory and its subdirectories
        json_files = []
        for root, dirs, files in os.walk(exp_dir):
            for file in files:
                if file.endswith('.json'):
                    json_files.append(os.path.join(root, file))
        
        print(f"Found {len(json_files)} JSON files to check")
        
        # Process each JSON file
        fixed_count = 0
        
        for file_path in json_files:
            try:
                # Read the file as text
                with open(file_path, 'r') as f:
                    content = f.read()
                
                # Check if file contains NaN
                if 'NaN' in content or 'nan' in content:
                    print(f"Fixing {os.path.basename(file_path)}")
                    
                    # Replace NaN values with null
                    fixed_content = content.replace('NaN', 'null').replace('nan', 'null')
                    fixed_content = fixed_content.replace('Infinity', 'null').replace('infinity', 'null')
                    fixed_content = fixed_content.replace('-Infinity', 'null').replace('-infinity', 'null')
                    
                    # Try to parse the JSON to ensure it's valid
                    try:
                        json.loads(fixed_content)
                    except json.JSONDecodeError as e:
                        print(f"Warning: Could not parse fixed JSON in {file_path}: {e}")
                        continue
                    
                    # Write the fixed content back to the file
                    with open(file_path, 'w') as f:
                        f.write(fixed_content)
                    
                    fixed_count += 1
            except Exception as e:
                print(f"Error processing {file_path}: {e}")
        
        print(f"Fixed {fixed_count} out of {len(json_files)} JSON files")
        return True

