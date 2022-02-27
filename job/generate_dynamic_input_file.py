import xarray as xr

data_path = "representative_domain.nc"

ds = xr.open_dataset(data_path)

da_u = xr.DataArray(
    data=ds.u.values,
    dims=["z", "y", "x"], 
    coords=dict(
        z=ds.u.zu_3d.values,
        y=ds.u.y.values,
        x=ds.u.xu.values,
    ),
    attrs=dict(
        lod=2,
        long_name="initial wind component in x direction",
        units="m/s",
    )
    )