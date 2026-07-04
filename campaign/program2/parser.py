import sbatchman as sbm
import json

def parse(job: sbm.Job):
  res = dict(json.loads(job.get_stdout()))
  res.update(job.variables)
  res.update(job.get_fields())
  return { 'matmul': res }