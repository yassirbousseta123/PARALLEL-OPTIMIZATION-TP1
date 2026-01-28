#!/usr/bin/env python3
"""
Exercise 2: Plot Matrix Multiplication Results

Reads results.csv and creates comparison plots for ijk vs ikj loop orders.
Generates:
  - mxm_time.png: Execution time comparison
  - mxm_gflops.png: Performance (GFLOPS) comparison
"""

import csv
import matplotlib.pyplot as plt
import numpy as np

def read_results(filename):
    """Read results from CSV file."""
    data = {'ijk': {'N': [], 'time': [], 'gflops': []},
            'ikj': {'N': [], 'time': [], 'gflops': []}}

    with open(filename, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            if len(row) >= 4:
                # Skip header row
                if row[0] == 'size':
                    continue
                n = int(row[0])
                loop_order = row[1]
                time_sec = float(row[2])
                gflops = float(row[3])

                if loop_order in data:
                    data[loop_order]['N'].append(n)
                    data[loop_order]['time'].append(time_sec)
                    data[loop_order]['gflops'].append(gflops)

    return data

def plot_time_comparison(data, output_file):
    """Create grouped bar chart for execution time."""
    fig, ax = plt.subplots(figsize=(10, 6))

    n_values = data['ijk']['N']
    x = np.arange(len(n_values))
    width = 0.35

    bars1 = ax.bar(x - width/2, data['ijk']['time'], width, label='ijk', color='steelblue')
    bars2 = ax.bar(x + width/2, data['ikj']['time'], width, label='ikj', color='coral')

    ax.set_xlabel('Matrix Size (N)', fontsize=12)
    ax.set_ylabel('Time (seconds)', fontsize=12)
    ax.set_title('Matrix Multiplication: Execution Time Comparison\n(ijk vs ikj loop order)', fontsize=14)
    ax.set_xticks(x)
    ax.set_xticklabels([str(n) for n in n_values])
    ax.legend(title='Loop Order')
    ax.grid(True, axis='y', alpha=0.3)

    # Add value labels on bars
    for bar in bars1:
        height = bar.get_height()
        ax.annotate(f'{height:.2f}s',
                    xy=(bar.get_x() + bar.get_width()/2, height),
                    xytext=(0, 3),
                    textcoords="offset points",
                    ha='center', va='bottom', fontsize=8)

    for bar in bars2:
        height = bar.get_height()
        ax.annotate(f'{height:.2f}s',
                    xy=(bar.get_x() + bar.get_width()/2, height),
                    xytext=(0, 3),
                    textcoords="offset points",
                    ha='center', va='bottom', fontsize=8)

    plt.tight_layout()
    plt.savefig(output_file, dpi=150)
    plt.close()
    print(f"Saved: {output_file}")

def plot_gflops_comparison(data, output_file):
    """Create grouped bar chart for GFLOPS performance."""
    fig, ax = plt.subplots(figsize=(10, 6))

    n_values = data['ijk']['N']
    x = np.arange(len(n_values))
    width = 0.35

    bars1 = ax.bar(x - width/2, data['ijk']['gflops'], width, label='ijk', color='steelblue')
    bars2 = ax.bar(x + width/2, data['ikj']['gflops'], width, label='ikj', color='coral')

    ax.set_xlabel('Matrix Size (N)', fontsize=12)
    ax.set_ylabel('GFLOPS', fontsize=12)
    ax.set_title('Matrix Multiplication: Performance Comparison\n(ijk vs ikj loop order)', fontsize=14)
    ax.set_xticks(x)
    ax.set_xticklabels([str(n) for n in n_values])
    ax.legend(title='Loop Order')
    ax.grid(True, axis='y', alpha=0.3)

    # Add value labels on bars
    for bar in bars1:
        height = bar.get_height()
        ax.annotate(f'{height:.2f}',
                    xy=(bar.get_x() + bar.get_width()/2, height),
                    xytext=(0, 3),
                    textcoords="offset points",
                    ha='center', va='bottom', fontsize=8)

    for bar in bars2:
        height = bar.get_height()
        ax.annotate(f'{height:.2f}',
                    xy=(bar.get_x() + bar.get_width()/2, height),
                    xytext=(0, 3),
                    textcoords="offset points",
                    ha='center', va='bottom', fontsize=8)

    plt.tight_layout()
    plt.savefig(output_file, dpi=150)
    plt.close()
    print(f"Saved: {output_file}")

def main():
    """Main function to read data and generate plots."""
    results_file = 'results.csv'

    print("Reading results from", results_file)
    data = read_results(results_file)

    if not data['ijk']['N'] or not data['ikj']['N']:
        print("Error: No data found in results.csv")
        print("Run 'make run' first to generate results.")
        return

    print(f"Found {len(data['ijk']['N'])} data points for each loop order")

    # Print summary
    print("\nResults Summary:")
    print("-" * 60)
    print(f"{'N':>6} | {'ijk Time':>10} | {'ikj Time':>10} | {'Speedup':>8}")
    print("-" * 60)
    for i in range(len(data['ijk']['N'])):
        n = data['ijk']['N'][i]
        ijk_time = data['ijk']['time'][i]
        ikj_time = data['ikj']['time'][i]
        speedup = ijk_time / ikj_time if ikj_time > 0 else 0
        print(f"{n:>6} | {ijk_time:>9.3f}s | {ikj_time:>9.3f}s | {speedup:>7.2f}x")
    print("-" * 60)

    # Generate plots
    print("\nGenerating plots...")
    plot_time_comparison(data, 'mxm_time.png')
    plot_gflops_comparison(data, 'mxm_gflops.png')

    print("\nDone! The ikj loop order should be faster due to better cache utilization.")
    print("In ikj order, the innermost loop accesses contiguous memory in both B and C.")

if __name__ == '__main__':
    main()
