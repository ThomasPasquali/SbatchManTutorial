import sbatchman as sbm
import re
from typing import Optional, Dict

def parse(job: sbm.Job) -> Optional[Dict]:
    if re.match(r'(float|double|float16)_\d+', job.tag):
        return parse_compute_pi_output(job)
    return None

def parse_compute_pi_output(job: sbm.Job):
    threads = job.variables['threads']
    dtype   = job.variables['dtype']
    samples = job.variables['samples']
    
    # Parse stdout
    stdout = job.get_stdout()
    pi_approx, runtime = None, None

    m = re.search(r"Pi\s*\(\w+\)\s*=\s*([0-9.]+)", stdout)
    if m: pi_approx = float(m.group(1))

    m = re.search(r"Runtime\s*=\s*([0-9.]+)\s*seconds", stdout)
    if m: runtime = float(m.group(1))

    # Emit a new row to table "pi"
    return { "pi": 
        {
            "threads": threads,
            "dtype": dtype,
            "samples": samples,
            "pi_approx": pi_approx,
            "runtime": runtime,
            "job_id": job.job_id,
            "status": job.status,
            "cluster": sbm.get_cluster_name(),
        }
    }

