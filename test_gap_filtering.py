#!/usr/bin/env python
"""
Test Gap Filtering
-----------------
This script demonstrates the gap filtering functionality in the data interpolation process.
It creates a sample dataset with gaps and shows how the filtering works.
"""

import os
import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

# Ensure Processors directory is in the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import the processor class
try:
    from Processors import ExperimentalDataProcessor
except ImportError:
    # Fallback for backwards compatibility
    from Main_Web_ProcessorNH3Crack import ExperimentalDataProcessor

def create_sample_data_with_gaps():
    """Create a sample dataset with time gaps"""
    # Create base datetime series with 1-minute intervals
    start_time = datetime(2023, 1, 1, 0, 0, 0)
    
    # Create a continuous section
    continuous_times = [start_time + timedelta(minutes=i) for i in range(30)]
    
    # Create a gap (10 minutes)
    gap_start = continuous_times[-1] + timedelta(minutes=1)
    gap_end = gap_start + timedelta(minutes=10)
    
    # Create a second continuous section
    continuous_times2 = [gap_end + timedelta(minutes=i) for i in range(30)]
    
    # Combine all times
    all_times = continuous_times + continuous_times2
    
    # Create a sine wave for the values
    time_minutes = [(t - start_time).total_seconds() / 60 for t in all_times]
    values = 100 + 10 * np.sin(np.array(time_minutes) * 0.1)
    
    # Create DataFrame
    df = pd.DataFrame({
        'DateTime': all_times,
        'Stage': [1] * len(all_times),
        'Value': values
    })
    
    return df, time_minutes

def plot_results(original_df, time_minutes, interpolated_df_with_gaps, interpolated_df_no_gaps):
    """Plot the original data and the interpolated data with and without gap filtering"""
    plt.figure(figsize=(15, 8))
    
    # Plot original data
    plt.plot(time_minutes, original_df['Value'], 'bo', label='Original Data')
    
    # Plot interpolated data without gap filtering
    plt.plot(
        interpolated_df_no_gaps['Time_Minutes'], 
        interpolated_df_no_gaps['Value'], 
        'r-', 
        label='Interpolated (No Gap Filtering)'
    )
    
    # Plot interpolated data with gap filtering
    plt.plot(
        interpolated_df_with_gaps['Time_Minutes'], 
        interpolated_df_with_gaps['Value'], 
        'g-', 
        label='Interpolated (With Gap Filtering)'
    )
    
    plt.title('Comparison of Interpolation Methods')
    plt.xlabel('Time (minutes)')
    plt.ylabel('Value')
    plt.legend()
    plt.grid(True)
    
    # Highlight the gap area
    plt.axvspan(30, 40, alpha=0.2, color='gray', label='Data Gap')
    
    # Save the figure
    plt.savefig('gap_filtering_comparison.png')
    print(f"Plot saved to 'gap_filtering_comparison.png'")
    
    # Show the plot if not in a headless environment
    try:
        plt.show()
    except:
        pass

def main():
    """Main function to demonstrate gap filtering"""
    print("=== NH3 Cracking Processor - Gap Filtering Demonstration ===")
    
    # Create sample data with gaps
    print("\nCreating sample data with time gaps...")
    df, time_minutes = create_sample_data_with_gaps()
    print(f"Created sample data with {len(df)} points and a 10-minute gap")
    
    # Initialize processor
    processor = ExperimentalDataProcessor()
    
    # Create time vector
    df = processor.create_time_vector(df)
    
    # Perform interpolation without gap filtering
    print("\nPerforming interpolation WITHOUT gap filtering...")
    interpolated_df_no_gaps = processor.perform_interpolation(df, max_gap_minutes=1000)
    print(f"Interpolated data without gap filtering: {len(interpolated_df_no_gaps)} points")
    
    # Perform interpolation with gap filtering
    print("\nPerforming interpolation WITH gap filtering (max gap: 5 minutes)...")
    interpolated_df_with_gaps = processor.perform_interpolation(df, max_gap_minutes=5)
    print(f"Interpolated data with gap filtering: {len(interpolated_df_with_gaps)} points")
    print(f"Filtered out {len(interpolated_df_no_gaps) - len(interpolated_df_with_gaps)} points")
    
    # Plot results
    print("\nGenerating comparison plot...")
    plot_results(df, time_minutes, interpolated_df_with_gaps, interpolated_df_no_gaps)
    
    print("\n=== Demonstration Complete ===")
    print("The plot shows how gap filtering prevents interpolation across large time gaps,")
    print("improving data quality and avoiding spurious interpolated values.")

if __name__ == "__main__":
    main() 