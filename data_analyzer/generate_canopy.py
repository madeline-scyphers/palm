import netCDF4
import numpy as np
from pathlib import Path

import xarray as xr

CANOPY_FILE = (Path(__file__).parent / "homogenous_canopy.nc").resolve()

# CANOPY_FILE = "homogenous_canopy.nc"

def get_new_lad(old_lad, tree_matrix, **kwargs):
    
    z_height = old_lad.shape[0]

    trees = np.tile(tree_matrix, (z_height, 1, 1))
    new_lad = np.multiply(trees, old_lad)
    
    return new_lad


def copy_netcdf(job_name, **kwargs):
    ds = xr.open_dataset(CANOPY_FILE)
    old_lad = ds["lad"].data
    lad = get_new_lad(old_lad, **kwargs)
    ds["lad"].data = lad
    ds.to_netcdf(f"{job_name}_static", format="NETCDF3_CLASSIC")