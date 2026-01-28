/*
 * Exercise 2: Matrix Multiplication with Loop Order Comparison
 *
 * Compares ijk vs ikj loop orderings to demonstrate cache effects.
 * Usage: ./mxm N loop_order
 *   N          - matrix size (NxN matrices)
 *   loop_order - "ijk" or "ikj"
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

/* Matrix multiplication using ijk loop order */
void mxm_ijk(double *A, double *B, double *C, int N) {
    int i, j, k;
    for (i = 0; i < N; i++) {
        for (j = 0; j < N; j++) {
            for (k = 0; k < N; k++) {
                C[i * N + j] += A[i * N + k] * B[k * N + j];
            }
        }
    }
}

/* Matrix multiplication using ikj loop order (cache-friendly) */
void mxm_ikj(double *A, double *B, double *C, int N) {
    int i, j, k;
    for (i = 0; i < N; i++) {
        for (k = 0; k < N; k++) {
            for (j = 0; j < N; j++) {
                C[i * N + j] += A[i * N + k] * B[k * N + j];
            }
        }
    }
}

int main(int argc, char *argv[]) {
    int N;
    char *loop_order;
    double *A, *B, *C;
    int i, j;
    clock_t start, end;
    double time_sec;
    double gflops;

    /* Parse command line arguments */
    if (argc != 3) {
        fprintf(stderr, "Usage: %s N loop_order\n", argv[0]);
        fprintf(stderr, "  N          - matrix size\n");
        fprintf(stderr, "  loop_order - \"ijk\" or \"ikj\"\n");
        return 1;
    }

    N = atoi(argv[1]);
    loop_order = argv[2];

    if (N <= 0) {
        fprintf(stderr, "Error: N must be positive\n");
        return 1;
    }

    if (strcmp(loop_order, "ijk") != 0 && strcmp(loop_order, "ikj") != 0) {
        fprintf(stderr, "Error: loop_order must be \"ijk\" or \"ikj\"\n");
        return 1;
    }

    /* Allocate matrices as 1D arrays (row-major order) */
    A = (double *)malloc(N * N * sizeof(double));
    B = (double *)malloc(N * N * sizeof(double));
    C = (double *)calloc(N * N, sizeof(double));  /* Initialize C to zero */

    if (A == NULL || B == NULL || C == NULL) {
        fprintf(stderr, "Error: Memory allocation failed\n");
        return 1;
    }

    /* Initialize matrices */
    /* A[i][j] = i + j */
    /* B[i][j] = i * j */
    for (i = 0; i < N; i++) {
        for (j = 0; j < N; j++) {
            A[i * N + j] = (double)(i + j);
            B[i * N + j] = (double)(i * j);
        }
    }

    /* Perform matrix multiplication with timing */
    start = clock();

    if (strcmp(loop_order, "ijk") == 0) {
        mxm_ijk(A, B, C, N);
    } else {
        mxm_ikj(A, B, C, N);
    }

    end = clock();

    /* Calculate elapsed time in seconds */
    time_sec = (double)(end - start) / CLOCKS_PER_SEC;

    /* Calculate GFLOPS */
    /* Matrix multiplication requires 2*N^3 floating point operations */
    /* (N^3 multiplications + N^3 additions) */
    gflops = (2.0 * (double)N * (double)N * (double)N) / (time_sec * 1e9);

    /* Output CSV line: N, loop_order, time_sec, GFLOPS */
    printf("%d,%s,%.6f,%.4f\n", N, loop_order, time_sec, gflops);

    /* Free allocated memory */
    free(A);
    free(B);
    free(C);

    return 0;
}
