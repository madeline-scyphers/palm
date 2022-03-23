from pathlib import Path

import numpy as np
import xarray as xr
from xarray.core.dataset import Dataset

from canopy_generator.generate_canopy import generate_canopy

CANOPY_FILE = (Path(__file__).parent / "homogenous_canopy.nc").resolve()

# CANOPY_FILE = "homogenous_canopy.nc"


def get_new_lad(old_lad, tree_matrix, **kwargs):

    z_height = old_lad.shape[0]

    trees = np.tile(tree_matrix, (z_height, 1, 1))
    new_lad = np.multiply(trees, old_lad)

    return new_lad


def get_lad_netcdf(job_name, tree_matrix, dx, dy, dz, mean_lai, **kwargs):
    trees = tree_matrix * -1
    zlad = [0, *range(1, 15, dz)]
    new_lad_ds = generate_canopy(
        trees.T, zlad=zlad, dz=dz, mean_lai=mean_lai
    )  #  todo cleanup the having to traspose things
    ds = new_lad_ds.drop(labels=["lai", "height", "patch", "flux", "DBHc"])
    ds = set_ds_attrs_and_coords(ds, dx, dy)
    return ds


def set_ds_attrs_and_coords(ds: xr.Dataset, dx: float, dy: float):
    attrs = dict(
        Conventions="CF-1.7",
        origin_lat=40.16339309801363,  # outskirts of Columbus ohio
        origin_lon=-83.16731841749935,
        origin_time="2022-02-27 12:00:00 +00",
        origin_x=315432.564,
        origin_y=4448144.558,
        origin_z=275.0,
        rotation_angle=0.0,
    )
    nx = ds.x.size
    ny = ds.y.size
    x = np.arange(dx / 2, nx * dx, dx, dtype=float)
    y = np.arange(dx / 2, ny * dy, dy, dtype=float)
    ds = ds.assign_attrs(**attrs)
    ds = ds.assign_coords(x=x, y=y)
    return ds


# def generate_dataaray(values):
#     da_u = xr.DataArray(
#         data=values,
#         dims=["z", "y", "x"],
#         coords=dict(
#             z=ds.u.zu_3d.values,
#             y=ds.u.y.values,
#             x=ds.u.xu.values,
#         ),
#         attrs=dict(
#             lod=2,
#             long_name="initial wind component in x direction",
#             units="m/s",
#         )
#         )
