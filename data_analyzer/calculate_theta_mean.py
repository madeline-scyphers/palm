from pathlib import Path

import xarray as xr

data_dir = Path(__file__).parent.parent / "current_version/JOBS"
path_glob = "20220307T*"


data = []
jobs = data_dir.glob(path_glob)
for i, job_path in enumerate(jobs):
    job = job_path.name
    print(job)
    ds = xr.open_dataset(job_path / "OUTPUT" / f"{job}_3d.nc")
    data.append(ds.theta.mean())
    if i >= 5:
        break
print(data)
