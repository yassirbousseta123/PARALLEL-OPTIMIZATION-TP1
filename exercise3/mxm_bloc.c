/*
 * Exercise 3: Block Matrix Multiplication
 *
 * This program implements block (tiled) matrix multiplication to improve
 * cache utilization. By processing the matrices in blocks that fit in cache,
 * we reduce cache misses and improve performance.
 *
 * Usage: ./mxm_bloc <N> <block_size>
 *   N          - Matrix dimension (NxN matrices)
 *   block_size - Size of blocks for tiled multiplication
 *
 * Output: CSV format - N, block_size, time_seconds, GFLOPS
 */

#include <stdio.h>
#include <stdlib.h>
#include <time.h>

/* Macro to find minimum of two values */
#define MIN(a, b) ((a) < (b) ? (a) : (b))

int main(int argc, char *argv[]) {
    int N, B;           /* Matrix size and block size */
    double *A, *B_mat, *C;  /* Matrices stored as 1D arrays (row-major) */
    int i, j, k;        /* Loop indices for element access */
    int ii, jj, kk;     /* Loop indices for block iteration */
    clock_t start, end;
    double time_seconds;
    double gflops;

    /* Check command line arguments */
    if (argc != 3) {
        fprintf(stderr, "Usage: %s <N> <block_size>\n", argv[0]);
        fprintf(stderr, "  N          - Matrix dimension\n");
        fprintf(stderr, "  block_size - Block size for tiled multiplication\n");
        return 1;
    }

    /* Parse arguments */
    N = atoi(argv[1]);
    B = atoi(argv[2]);

    /* Validate inputs */
    if (N <= 0 || B <= 0) {
        fprintf(stderr, "Error: N and block_size must be positive integers\n");
        return 1;
    }

    if (B > N) {
        fprintf(stderr, "Warning: block_size > N, using block_size = N\n");
        B = N;
    }

    /* Allocate matrices as 1D arrays (row-major order) */
    A = (double *)malloc(N * N * sizeof(double));
    B_mat = (double *)malloc(N * N * sizeof(double));
    C = (double *)malloc(N * N * sizeof(double));

    if (A == NULL || B_mat == NULL || C == NULL) {
        fprintf(stderr, "Error: Memory allocation failed\n");
        free(A);
        free(B_mat);
        free(C);
        return 1;
    }

    /* Initialize matrices */
    /* A[i][j] = i + j */
    /* B_mat[i][j] = i * j */
    /* C[i][j] = 0 */
    for (i = 0; i < N; i++) {
        for (j = 0; j < N; j++) {
            A[i * N + j] = (double)(i + j);
            B_mat[i * N + j] = (double)(i * j);
            C[i * N + j] = 0.0;
        }
    }

    /* Start timing */
    start = clock();

    /*
     * Block Matrix Multiplication
     *
     * The idea is to process the matrices in blocks (tiles) that fit in cache.
     * This improves temporal locality - once we load a block into cache,
     * we reuse it multiple times before moving to the next block.
     *
     * The outer three loops (ii, jj, kk) iterate over blocks.
     * The inner three loops (i, j, k) iterate within each block.
     */
    for (ii = 0; ii < N; ii += B) {
        for (jj = 0; jj < N; jj += B) {
            for (kk = 0; kk < N; kk += B) {
                /* Multiply blocks */
                for (i = ii; i < MIN(ii + B, N); i++) {
                    for (j = jj; j < MIN(jj + B, N); j++) {
                        for (k = kk; k < MIN(kk + B, N); k++) {
                            C[i * N + j] += A[i * N + k] * B_mat[k * N + j];
                        }
                    }
                }
            }
        }
    }

    /* Stop timing */
    end = clock();

    /* Calculate elapsed time in seconds */
    time_seconds = (double)(end - start) / CLOCKS_PER_SEC;

    /*
     * Calculate GFLOPS (Giga Floating Point Operations Per Second)
     * Matrix multiplication of NxN matrices requires:
     * - N^3 multiplications
     * - N^3 additions
     * Total: 2 * N^3 floating point operations
     */
    gflops = (2.0 * (double)N * (double)N * (double)N) / (time_seconds * 1e9);

    /* Output results in CSV format: N, block_size, time_seconds, GFLOPS */
    printf("%d,%d,%.6f,%.4f\n", N, B, time_seconds, gflops);

    /* Free allocated memory */
    free(A);
    free(B_mat);
    free(C);

    return 0;
}
