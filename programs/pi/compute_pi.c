#include <stdio.h>
#include <stdlib.h>
#include <omp.h>
#include <time.h>
#include <math.h>

// Choose type based on compile-time macro
#if defined(TYPE_FLOAT16)
    #include <stdint.h>
    typedef _Float16 real_t;
    #define TYPE_NAME "float16"
#elif defined(TYPE_FLOAT)
    typedef float real_t;
    #define TYPE_NAME "float"
#elif defined(TYPE_DOUBLE)
    typedef double real_t;
    #define TYPE_NAME "double"
#else
    #error "Please define one of TYPE_FLOAT16, TYPE_FLOAT, TYPE_DOUBLE"
#endif

int main(int argc, char **argv) {
    long N = 100000000;
    if (argc > 1) N = atol(argv[1]);

    long inside = 0;
    unsigned int seed;

    double start = omp_get_wtime();

    #pragma omp parallel private(seed) reduction(+:inside)
    {
        seed = (unsigned int) time(NULL) ^ omp_get_thread_num();
        #pragma omp for
        for (long i = 0; i < N; i++) {
            real_t x = (real_t) rand_r(&seed) / RAND_MAX;
            real_t y = (real_t) rand_r(&seed) / RAND_MAX;
            if (x*x + y*y <= (real_t) 1.0) inside++;
        }
    }

    double end = omp_get_wtime();
    real_t pi = (real_t) 4.0 * inside / N;

    printf("Pi (%s) = %.*g (N=%ld)\n",
           TYPE_NAME,
           (int)(sizeof(real_t) * 2 + 2),
           (double) pi, N);

    printf("Runtime = %.4f seconds\n", end - start);

    return 0;
}
