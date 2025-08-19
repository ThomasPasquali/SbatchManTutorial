CC = gcc
CFLAGS = -O3 -fopenmp

all: float double float16

float:
	$(CC) $(CFLAGS) -DTYPE_FLOAT -o compute_pi_float compute_pi.c

double:
	$(CC) $(CFLAGS) -DTYPE_DOUBLE -o compute_pi_double compute_pi.c

float16:
	$(CC) $(CFLAGS) -DTYPE_FLOAT16 -o compute_pi_float16 compute_pi.c

clean:
	rm -f compute_pi_float compute_pi_double compute_pi_float16
