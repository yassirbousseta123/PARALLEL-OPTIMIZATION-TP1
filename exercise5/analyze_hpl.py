#!/usr/bin/env python3
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Theoretical peak for M4 Max (10 P-cores, ~4.4 GHz, 4 FP64 ops/cycle)
THEORETICAL_PEAK = 176.0  # GFLOPS

def main():
    # Read results
    df = pd.read_csv('hpl_results.csv')

    print("HPL Benchmark Results Analysis")
    print("=" * 50)
    print(f"\nTheoretical Peak: {THEORETICAL_PEAK} GFLOPS")

    # Add efficiency column
    df['Efficiency_%'] = (df['GFLOPS'] / THEORETICAL_PEAK) * 100

    print("\nAll Results:")
    print(df.to_string(index=False))

    # Find optimal configuration
    best = df.loc[df['GFLOPS'].idxmax()]
    print(f"\nOptimal Configuration:")
    print(f"  N = {best['N']}, NB = {best['NB']}")
    print(f"  Performance: {best['GFLOPS']:.2f} GFLOPS")
    print(f"  Efficiency: {best['Efficiency_%']:.1f}%")

    # Plot 1: GFLOPS vs N for different NB
    plt.figure(figsize=(10, 6))
    for nb in df['NB'].unique():
        subset = df[df['NB'] == nb]
        plt.plot(subset['N'], subset['GFLOPS'], 'o-', label=f'NB={nb}')

    plt.axhline(y=THEORETICAL_PEAK, color='r', linestyle='--', label='Theoretical Peak')
    plt.xlabel('Matrix Size (N)')
    plt.ylabel('Performance (GFLOPS)')
    plt.title('HPL Performance vs Matrix Size')
    plt.legend()
    plt.grid(True)
    plt.savefig('hpl_performance.png', dpi=150)
    plt.close()

    # Plot 2: Heatmap of GFLOPS
    pivot = df.pivot(index='NB', columns='N', values='GFLOPS')
    plt.figure(figsize=(10, 6))
    plt.imshow(pivot.values, aspect='auto', cmap='YlOrRd')
    plt.colorbar(label='GFLOPS')
    plt.xticks(range(len(pivot.columns)), pivot.columns)
    plt.yticks(range(len(pivot.index)), pivot.index)
    plt.xlabel('Matrix Size (N)')
    plt.ylabel('Block Size (NB)')
    plt.title('HPL Performance Heatmap')

    # Add text annotations
    for i in range(len(pivot.index)):
        for j in range(len(pivot.columns)):
            val = pivot.values[i, j]
            if not np.isnan(val):
                plt.text(j, i, f'{val:.1f}', ha='center', va='center')

    plt.savefig('hpl_heatmap.png', dpi=150)
    plt.close()

    # Plot 3: Efficiency
    plt.figure(figsize=(10, 6))
    for nb in df['NB'].unique():
        subset = df[df['NB'] == nb]
        plt.plot(subset['N'], subset['Efficiency_%'], 'o-', label=f'NB={nb}')

    plt.axhline(y=100, color='r', linestyle='--', label='100% Efficiency')
    plt.xlabel('Matrix Size (N)')
    plt.ylabel('Efficiency (%)')
    plt.title('HPL Efficiency vs Matrix Size')
    plt.legend()
    plt.grid(True)
    plt.savefig('hpl_efficiency.png', dpi=150)
    plt.close()

    print("\nPlots saved: hpl_performance.png, hpl_heatmap.png, hpl_efficiency.png")

if __name__ == '__main__':
    main()
