import os
import sys

print(f'The first CLI arg is: "{sys.argv[1]}"\n\n')

omp_threads = os.environ.get("OMP_NUM_THREADS")
if omp_threads is not None:
    print(f"OMP_NUM_THREADS = {omp_threads} (out of {os.cpu_count()} total cores available)")
else:
    print("OMP_NUM_THREADS is not set")
    print(f"Available CPU cores: {os.cpu_count()}")