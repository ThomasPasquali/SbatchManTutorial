import matplotlib.pyplot as plt
import numpy as np
import re
import pandas as pd
import sbatchman as sbm


def jobs_to_dataframe(jobs):
    rows = []
    for job in jobs:
        # Threads from config_name like "8_threads"
        m = re.match(r"(\d+)_threads", job.config_name)
        threads = int(m.group(1)) if m else None

        # dtype and samples from tag like "float_100000"
        dtype, samples = None, None
        if job.tag and "_" in job.tag:
            parts = job.tag.split("_")
            if len(parts) == 2:
                dtype, samples = parts[0], int(parts[1])

        # Parse stdout
        stdout = job.get_stdout()
        pi_approx, runtime = None, None

        m = re.search(r"Pi\s*\(\w+\)\s*=\s*([0-9.]+)", stdout)
        if m: pi_approx = float(m.group(1))

        m = re.search(r"Runtime\s*=\s*([0-9.]+)\s*seconds", stdout)
        if m: runtime = float(m.group(1))

        rows.append({
            "threads": threads,
            "dtype": dtype,
            "samples": samples,
            "pi_approx": pi_approx,
            "runtime": runtime,
            "job_id": job.job_id,
            "status": job.status,
            "cluster": sbm.get_cluster_name(),
        })
    
    return pd.DataFrame(rows)


def plot_scaling_and_precision(df):
    true_pi = np.pi

    # Compute error
    df = df.copy()
    df["abs_error"] = (df["pi_approx"] - true_pi).abs()

    # --- Scaling plot: Runtime vs Threads (fixed samples, one per dtype) ---
    plt.figure(figsize=(6,4))
    for dtype, group in df.groupby("dtype"):
        # pick the largest samples to emphasize scaling
        subset = group[group["samples"] == group["samples"].max()]
        plt.plot(subset["threads"], subset["runtime"], marker="o", label=dtype)
    plt.xticks(sorted(df['threads'].unique()))
    plt.xlabel("Threads")
    plt.ylabel("Runtime (s)")
    plt.title(f"Scaling with Threads (samples={df['samples'].max()})")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(f'{sbm.get_cluster_name()}_strong_scaling.png')

    # --- Strong scaling efficiency (optional) ---
    plt.figure(figsize=(6,4))
    for dtype, group in df.groupby("dtype"):
        # pick a fixed samples value
        samples_val = group["samples"].max()
        subset = group[group["samples"] == samples_val].sort_values("threads")
        T1 = subset.loc[subset["threads"]==subset["threads"].min(),"runtime"].values[0]
        speedup = T1 / subset["runtime"]
        efficiency = speedup / subset["threads"]
        plt.plot(subset["threads"], efficiency, marker="o", label=f"{dtype} (N={samples_val})")
    plt.xticks(sorted(df['threads'].unique()))
    plt.xlabel("Threads")
    plt.ylabel("Parallel Efficiency")
    plt.title("Strong Scaling Efficiency")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(f'{sbm.get_cluster_name()}_efficiency.png')
    
    # --- Precision plot: Error vs Samples ---
    plt.figure(figsize=(6,4))
    for dtype, group in df.groupby("dtype"):
        plt.loglog(group["samples"], group["abs_error"], marker="o", label=dtype)
    plt.xlabel("Samples (log scale)")
    plt.ylabel("Absolute Error (log scale)")
    plt.title("Precision vs Samples")
    plt.legend()
    plt.grid(True, which="both")
    plt.tight_layout()
    plt.savefig(f'{sbm.get_cluster_name()}_precision.png')


if __name__ == "__main__":
    df = jobs_to_dataframe(sbm.jobs_list(status=[sbm.Status.COMPLETED]))
    df.sort_values(['dtype', 'threads'], inplace=True)

    # Save for portability
    df.to_csv(f'{sbm.get_cluster_name()}_pi_results.csv', index=False)

    print(df)
    plot_scaling_and_precision(df)