#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <omp.h>

#ifndef DTYPE
#define DTYPE double
#endif

typedef DTYPE dtype;

static const char *dtype_name(void) {
    if (sizeof(dtype) == sizeof(char)) {
        return "char";
    } else if (sizeof(dtype) == sizeof(float)) {
        return "float";
    } else if (sizeof(dtype) == sizeof(double)) {
        return "double";
    } else {
        return "unknown";
    }
}

int main(int argc, char const *argv[]) {
    if (argc < 2) {
        fprintf(stderr, "Usage: %s <num_elements>\n", argv[0]);
        return 1;
    }

    size_t n = strtoull(argv[1], NULL, 10);

    dtype *a = (dtype *) malloc(n * sizeof(dtype));
    dtype *b = (dtype *) malloc(n * sizeof(dtype));

    if (!a || !b) {
        fprintf(stderr, "Allocation failed\n");
        free(a);
        free(b);
        return 1;
    }

    // Initialize arrays
    #pragma omp parallel for
    for (size_t i = 0; i < n; i++) {
        a[i] = (dtype) i;
        b[i] = (dtype) (i + 1);
    }

    // Bandwidth test: read a[i], read b[i], write a[i]
    double start = omp_get_wtime();

    #pragma omp parallel for
    for (size_t i = 0; i < n; i++) {
        a[i] = a[i] + b[i];
    }

    double end = omp_get_wtime();

    double seconds = end - start;

    // read a + read b + write a
    size_t bytes_moved = 3ULL * n * sizeof(dtype);

    double bandwidth_gb_s =
        ((double) bytes_moved / seconds) / 1e9;

    int threads = 1;

    #pragma omp parallel
    {
        #pragma omp master
        {
            threads = omp_get_num_threads();
        }
    }

    // JSON output
    printf("{\n");
    printf("  \"datatype\": \"%s\",\n", dtype_name());
    printf("  \"array_size\": %zu,\n", n);
    printf("  \"element_size_bytes\": %zu,\n", sizeof(dtype));
    printf("  \"threads\": %d,\n", threads);
    printf("  \"bytes_moved\": %zu,\n", bytes_moved);
    printf("  \"time_seconds\": %.9f,\n", seconds);
    printf("  \"bandwidth_GBps\": %.3f\n", bandwidth_gb_s);
    printf("}\n");

    free(a);
    free(b);

    return 0;
}