import json
import sbatchman as sbm
import pandas as pd
import matplotlib.pyplot as plt

# -----------------------------------------------------------------------------
# Parsing
# -----------------------------------------------------------------------------

def job_filter(job: sbm.Job):
    return job.get_stdout() is not None

def parse_stdout(job: sbm.Job):
    return dict(json.loads(job.get_stdout()))

df: pd.DataFrame = sbm.jobs_to_dataframe(
    status=[sbm.Status.COMPLETED],
    job_filter=job_filter,
    extractors=[
        parse_stdout,
    ],
    include_job_fields=True,
)

print(df)






# -----------------------------------------------------------------------------
# Aggregate results
# -----------------------------------------------------------------------------
# Compute mean runtime grouped by:
#   - cluster
#   - backend
#   - matrix size
#   - make_it_slow
summary = (
    df.groupby([
        "cluster_name",
        "backend",
        "matrix_size",
        "make_it_slow"
    ])["time_seconds"]
    .mean()
    .reset_index()
)

# -----------------------------------------------------------------------------
# Plot
# -----------------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(10, 6))

# Create one line per (cluster, backend, make_it_slow)
for (cluster, backend, slow), group in summary.groupby([
    "cluster_name",
    "backend",
    "make_it_slow"
]):

    group = group.sort_values("matrix_size")

    label = f"{cluster} | {backend} | slow={slow}"

    ax.plot(
        group["matrix_size"],
        group["time_seconds"],
        marker="o",
        label=label
    )

# -----------------------------------------------------------------------------
# Styling
# -----------------------------------------------------------------------------
ax.set_title("Matrix Multiplication Runtime")
ax.set_xlabel("Matrix Size")
ax.set_xticks(df['matrix_size'].unique())
ax.set_ylabel("Time (seconds)")
# ax.set_yscale("log")
ax.grid(True)
ax.legend()

plt.tight_layout()
plt.show()