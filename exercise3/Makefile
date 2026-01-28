# Makefile for Exercise 3: Block Matrix Multiplication
#
# This Makefile compiles the block matrix multiplication program and
# runs experiments with different block sizes to find the optimal value.

CC = gcc
CFLAGS = -O2

# Matrix size for experiments
MATRIX_SIZE = 2000

# Block sizes to test
BLOCK_SIZES = 8 16 32 64 128 256

# Default target
all: mxm_bloc

# Compile the block matrix multiplication program
mxm_bloc: mxm_bloc.c
	$(CC) $(CFLAGS) -o mxm_bloc mxm_bloc.c

# Run experiments with different block sizes
run: mxm_bloc
	rm -f results.csv
	@echo "Running block matrix multiplication experiments..."
	@echo "Matrix size: $(MATRIX_SIZE)x$(MATRIX_SIZE)"
	@echo "Testing block sizes: $(BLOCK_SIZES)"
	@echo "-------------------------------------------"
	@echo "N,block_size,time_sec,GFLOPS" > results.csv.header
	for b in $(BLOCK_SIZES); do \
		echo "Testing block size: $$b"; \
		./mxm_bloc $(MATRIX_SIZE) $$b >> results.csv; \
	done
	@echo "-------------------------------------------"
	@echo "Results saved to results.csv"
	@cat results.csv

# Run with custom matrix size: make run-custom N=1000
run-custom: mxm_bloc
	rm -f results.csv
	@echo "Running with custom matrix size N=$(N)"
	for b in $(BLOCK_SIZES); do \
		./mxm_bloc $(N) $$b >> results.csv; \
	done
	@cat results.csv

# Generate plots (requires Python with matplotlib and pandas)
plot: results.csv
	python3 plot_bloc.py

# Run experiments and generate plots
all-run: run plot

# Clean up generated files
clean:
	rm -f mxm_bloc results.csv results.csv.header *.png

# Help target
help:
	@echo "Available targets:"
	@echo "  all      - Compile the program (default)"
	@echo "  mxm_bloc - Compile the block matrix multiplication program"
	@echo "  run      - Run experiments with different block sizes"
	@echo "  run-custom N=<size> - Run with custom matrix size"
	@echo "  plot     - Generate performance plots"
	@echo "  all-run  - Run experiments and generate plots"
	@echo "  clean    - Remove generated files"
	@echo "  help     - Show this help message"

.PHONY: all run run-custom plot all-run clean help
