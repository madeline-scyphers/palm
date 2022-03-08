from pathlib import Path

import xarray as xr


raw_data_path = (Path("/users/PAS0409/madelinescyphers/palm/current_version/JOBS/20220307T204058/OUTPUT/20220307T204058_3d.nc")).resolve()


ds = xr.open_dataset(raw_data_path)
print(ds.theta.values)