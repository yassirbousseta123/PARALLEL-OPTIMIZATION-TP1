#!/usr/bin/env python3
"""
Plot stride benchmark results comparing O0 and O2 optimization levels.
"""

import matplotlib.pyplot as plt
import csv

def read_csv(filename):
    """Read CSV file and return data as dictionary of lists."""
    data = {
        'stride': [],
        'time_ms': [],
        'bandwidth_MB_s': [],
        'sum': []
    }

    with open(filename, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            data['stride'].append(int(row['stride']))
            data['time_ms'].append(float(row['time_ms']))
            data['bandwidth_MB_s'].append(float(row['bandwidth_MB_s']))
            data['sum'].append(float(row['sum']))

    return data

def main():
    # Read data from both CSV files
    try:
        data_O0 = read_csv('results_O0.csv')
        data_O2 = read_csv('results_O2.csv')
    except FileNotFoundError as e:
        print(f"Error: {e}")
        print("Please run 'make run' first to generate the CSV files.")
        return

    # Set up plot style
    plt.style.use('seaborn-v0_8-whitegrid') if 'seaborn-v0_8-whitegrid' in plt.style.available else None

    # Plot 1: Stride vs Time (ms)
    plt.figure(figsize=(10, 6))
    plt.plot(data_O0['stride'], data_O0['time_ms'], 'b-o', label='O0 (no optimization)', linewidth=2, markersize=6)
    plt.plot(data_O2['stride'], data_O2['time_ms'], 'r-s', label='O2 (optimized)', linewidth=2, markersize=6)
    plt.xlabel('Stride', fontsize=12)
    plt.ylabel('Time (ms)', fontsize=12)
    plt.title('Memory Access Stride vs Execution Time', fontsize=14)
    plt.legend(loc='best', fontsize=10)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.xticks(range(1, 21))
    plt.tight_layout()
    plt.savefig('stride_time.png', dpi=150)
    print("Saved: stride_time.png")
    plt.close()

    # Plot 2: Stride vs Bandwidth (MB/s)
    plt.figure(figsize=(10, 6))
    plt.plot(data_O0['stride'], data_O0['bandwidth_MB_s'], 'b-o', label='O0 (no optimization)', linewidth=2, markersize=6)
    plt.plot(data_O2['stride'], data_O2['bandwidth_MB_s'], 'r-s', label='O2 (optimized)', linewidth=2, markersize=6)
    plt.xlabel('Stride', fontsize=12)
    plt.ylabel('Bandwidth (MB/s)', fontsize=12)
    plt.title('Memory Access Stride vs Bandwidth', fontsize=14)
    plt.legend(loc='best', fontsize=10)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.xticks(range(1, 21))
    plt.tight_layout()
    plt.savefig('stride_bandwidth.png', dpi=150)
    print("Saved: stride_bandwidth.png")
    plt.close()

    print("\nPlots generated successfully!")
    print("- stride_time.png: Shows execution time vs stride")
    print("- stride_bandwidth.png: Shows bandwidth vs stride")

if __name__ == '__main__':
    main()
