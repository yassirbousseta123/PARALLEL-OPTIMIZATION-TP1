#!/usr/bin/env python3
"""
Exercise 3: Block Matrix Multiplication - Performance Visualization

This script reads the results from block matrix multiplication experiments
and generates plots showing how performance varies with block size.

It creates two plots:
1. Block Size vs Time (seconds)
2. Block Size vs GFLOPS (performance)

The script also identifies and prints the optimal block size.
"""

import sys
import os

try:
    import pandas as pd
    import matplotlib.pyplot as plt
    import numpy as np
except ImportError as e:
    print(f"Error: Required library not found: {e}")
    print("Please install required libraries:")
    print("  pip install pandas matplotlib numpy")
    sys.exit(1)


def read_results(filename='results.csv'):
    """
    Read the results CSV file.

    Expected format: N, block_size, time_sec, GFLOPS
    """
    if not os.path.exists(filename):
        print(f"Error: Results file '{filename}' not found.")
        print("Please run 'make run' first to generate results.")
        sys.exit(1)

    # Read CSV with header
    df = pd.read_csv(filename)
    # Normalize column names
    df.columns = ['N', 'block_size', 'time_sec', 'GFLOPS']

    return df


def find_optimal_block_size(df):
    """
    Find the block size that gives the best performance (highest GFLOPS).
    """
    optimal_idx = df['GFLOPS'].idxmax()
    optimal_row = df.loc[optimal_idx]
    return optimal_row


def plot_time(df, output_file='bloc_time.png'):
    """
    Create a plot of Block Size vs Time.
    """
    plt.figure(figsize=(10, 6))

    # Plot time vs block size
    plt.plot(df['block_size'], df['time_sec'], 'bo-', linewidth=2,
             markersize=10, label='Execution Time')

    # Mark the minimum time point
    min_idx = df['time_sec'].idxmin()
    min_block = df.loc[min_idx, 'block_size']
    min_time = df.loc[min_idx, 'time_sec']
    plt.scatter([min_block], [min_time], color='red', s=200, zorder=5,
                label=f'Minimum: {min_time:.3f}s @ block={min_block}')

    # Formatting
    plt.xlabel('Block Size', fontsize=12)
    plt.ylabel('Time (seconds)', fontsize=12)
    plt.title(f'Block Matrix Multiplication: Block Size vs Execution Time\n'
              f'Matrix Size: {df["N"].iloc[0]}x{df["N"].iloc[0]}', fontsize=14)
    plt.grid(True, alpha=0.3)
    plt.legend(fontsize=10)

    # Set x-axis to show all block sizes
    plt.xticks(df['block_size'])

    # Add some padding to y-axis
    ymin, ymax = plt.ylim()
    plt.ylim(ymin * 0.95, ymax * 1.05)

    plt.tight_layout()
    plt.savefig(output_file, dpi=150)
    plt.close()

    print(f"Time plot saved to: {output_file}")


def plot_gflops(df, output_file='bloc_gflops.png'):
    """
    Create a plot of Block Size vs GFLOPS.
    """
    plt.figure(figsize=(10, 6))

    # Plot GFLOPS vs block size
    plt.plot(df['block_size'], df['GFLOPS'], 'go-', linewidth=2,
             markersize=10, label='Performance (GFLOPS)')

    # Mark the maximum GFLOPS point
    max_idx = df['GFLOPS'].idxmax()
    max_block = df.loc[max_idx, 'block_size']
    max_gflops = df.loc[max_idx, 'GFLOPS']
    plt.scatter([max_block], [max_gflops], color='red', s=200, zorder=5,
                label=f'Maximum: {max_gflops:.2f} GFLOPS @ block={max_block}')

    # Formatting
    plt.xlabel('Block Size', fontsize=12)
    plt.ylabel('GFLOPS', fontsize=12)
    plt.title(f'Block Matrix Multiplication: Block Size vs Performance\n'
              f'Matrix Size: {df["N"].iloc[0]}x{df["N"].iloc[0]}', fontsize=14)
    plt.grid(True, alpha=0.3)
    plt.legend(fontsize=10)

    # Set x-axis to show all block sizes
    plt.xticks(df['block_size'])

    # Add some padding to y-axis
    ymin, ymax = plt.ylim()
    plt.ylim(ymin * 0.95, ymax * 1.05)

    plt.tight_layout()
    plt.savefig(output_file, dpi=150)
    plt.close()

    print(f"GFLOPS plot saved to: {output_file}")


def print_summary(df, optimal):
    """
    Print a summary of the results.
    """
    print("\n" + "="*60)
    print("BLOCK MATRIX MULTIPLICATION - RESULTS SUMMARY")
    print("="*60)
    print(f"\nMatrix Size: {optimal['N']}x{optimal['N']}")
    print(f"Block sizes tested: {sorted(df['block_size'].unique().tolist())}")
    print("\nDetailed Results:")
    print("-"*50)
    print(f"{'Block Size':<12} {'Time (s)':<12} {'GFLOPS':<12}")
    print("-"*50)

    for _, row in df.iterrows():
        print(f"{int(row['block_size']):<12} {row['time_sec']:<12.4f} {row['GFLOPS']:<12.2f}")

    print("-"*50)
    print(f"\nOPTIMAL BLOCK SIZE: {int(optimal['block_size'])}")
    print(f"  - Execution Time: {optimal['time_sec']:.4f} seconds")
    print(f"  - Performance: {optimal['GFLOPS']:.2f} GFLOPS")
    print("="*60)

    # Explain the relationship between block size and cache
    print("\nANALYSIS:")
    print("-"*60)
    print("Block size affects cache utilization:")
    print("  - Too small: Loop overhead dominates, poor instruction-level parallelism")
    print("  - Too large: Blocks don't fit in L1/L2 cache, causing cache misses")
    print("  - Optimal: Blocks fit well in cache, maximizing data reuse")
    print(f"\nFor this system, block size {int(optimal['block_size'])} provides")
    print("the best balance between cache utilization and loop efficiency.")
    print("="*60 + "\n")


def main():
    """
    Main function to read results and generate plots.
    """
    # Read results
    print("Reading results from results.csv...")
    df = read_results('results.csv')

    if df.empty:
        print("Error: No data found in results.csv")
        sys.exit(1)

    # Find optimal block size
    optimal = find_optimal_block_size(df)

    # Generate plots
    print("\nGenerating plots...")
    plot_time(df, 'bloc_time.png')
    plot_gflops(df, 'bloc_gflops.png')

    # Print summary
    print_summary(df, optimal)


if __name__ == '__main__':
    main()
