#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#define SIZE 100000
#define ITERATIONS 1000

int main() {
    // Allocate array of doubles
    double *array = (double *)malloc(SIZE * sizeof(double));
    if (array == NULL) {
        fprintf(stderr, "Memory allocation failed\n");
        return 1;
    }

    // Initialize array with some values
    for (int i = 0; i < SIZE; i++) {
        array[i] = (double)(i % 100) * 0.01;
    }

    // Print CSV header
    printf("stride,time_ms,bandwidth_MB_s,sum\n");

    // Test strides from 1 to 20
    for (int stride = 1; stride <= 20; stride++) {
        double sum = 0.0;

        // Start timing
        clock_t start = clock();

        // Perform iterations
        for (int iter = 0; iter < ITERATIONS; iter++) {
            for (int i = 0; i < SIZE; i += stride) {
                sum += array[i];
            }
        }

        // End timing
        clock_t end = clock();

        // Calculate time in milliseconds
        double time_seconds = (double)(end - start) / CLOCKS_PER_SEC;
        double time_ms = time_seconds * 1000.0;

        // Calculate number of elements accessed per iteration
        long elements_per_iter = (SIZE + stride - 1) / stride;

        // Calculate total bytes accessed
        double total_bytes = (double)ITERATIONS * elements_per_iter * sizeof(double);

        // Calculate bandwidth in MB/s
        double bandwidth_MB_s = 0.0;
        if (time_seconds > 0) {
            bandwidth_MB_s = total_bytes / (time_seconds * 1e6);
        }

        // Output CSV line
        printf("%d,%.4f,%.2f,%.6f\n", stride, time_ms, bandwidth_MB_s, sum);
    }

    // Free allocated memory
    free(array);

    return 0;
}
