#!/usr/bin/env python3

import argparse
import json
import os
import time
import numpy as np


def manual_matmul(A, B):
    n = len(A)
    C = [[0.0 for _ in range(n)] for _ in range(n)]

    for i in range(n):
        for j in range(n):
            s = 0.0
            for k in range(n):
                s += A[i][k] * B[k][j]
            C[i][j] = s

    return C


def main():
    parser = argparse.ArgumentParser(
        description="Square matrix-matrix multiplication benchmark"
    )

    parser.add_argument(
        "--size",
        type=int,
        required=True,
        help="Matrix size N (NxN matrices)"
    )

    parser.add_argument(
        "--backend",
        choices=["numpy", "manual"],
        required=True,
        help="Backend implementation"
    )

    args = parser.parse_args()

    n = args.size
    backend = args.backend

    # Generate random matrices
    if backend == "numpy":
        A = np.random.rand(n, n)
        B = np.random.rand(n, n)
    else:
        A = np.random.rand(n, n).tolist()
        B = np.random.rand(n, n).tolist()

    make_it_slow = os.getenv("MAKE_IT_SLOW") is not None

    # Benchmark
    start = time.perf_counter()

    if backend == "numpy":
        C = A @ B
    else:
        C = manual_matmul(A, B)

    # Optional artificial slowdown
    if make_it_slow:
        time.sleep(1)

    end = time.perf_counter()

    result = {
        "size": n,
        "backend": backend,
        "make_it_slow": make_it_slow,
        "time_seconds": end - start
    }

    print(json.dumps(result, indent=4))


if __name__ == "__main__":
    main()