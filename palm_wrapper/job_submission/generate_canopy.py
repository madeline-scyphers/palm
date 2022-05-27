from pathlib import Path

import numpy as np
import xarray as xr
from palm_wrapper.canopy_generator.generate_canopy import generate_canopy

CANOPY_FILE = (Path(__file__).parent / "homogenous_canopy.nc").resolve()


def get_xarray_ds(job_name, tree_matrix, dx, dy, dz, mean_lai, stack_height, topo, **kwargs):
    trees = tree_matrix * -1
    zlad = [0, *range(1, 15, dz)]
    new_lad_ds = generate_canopy(
        trees.T, zlad=zlad, dz=dz, mean_lai=mean_lai
    )  #  todo cleanup the having to traspose things
    ds = new_lad_ds.drop(labels=["lai", "height", "patch", "flux", "DBHc"])
    ds = set_ds_attrs_and_coords(ds, dx, dy)
    add_topo_dataarray(ds, topo, ds.y, ds.x)
    ssws = setup_surface_scalar_np(topo, stack_height)
    add_surface_scalar_dataarray(ds, ssws, ds.y, ds.x)
    return ds


def add_topo_dataarray(ds, topo, y, x):
    topo_da = xr.DataArray(
        data=topo,
        dims=["y", "x"],
        coords=dict(
            y=y,
            x=x,
        ),
        attrs=dict(
            long_name="terrain height",
            units="m",
        ),
    )
    ds["topo"] = topo_da


def add_surface_scalar_dataarray(ds, ssws, y, x):
    ssws_da = xr.DataArray(
        data=ssws,
        dims=["y", "x"],
        coords=dict(
            y=y,
            x=x,
        ),
        attrs=dict(
            long_name="surface passive scalar flux",
            units="kg m /( kg s )",
        ),
    )
    ds["ssws"] = ssws_da


def setup_surface_scalar_np(topo, stack_height):
    ssws = topo.copy()
    ssws[ssws != stack_height] = 0
    ssws[ssws == stack_height] = 1
    return ssws

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
