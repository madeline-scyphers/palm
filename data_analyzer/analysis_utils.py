import xarray as xr

def load_data_set(data_path):
    ds_3d = xr.open_dataset(data_path)
    ds_3d = ds_3d.drop_isel(zu_3d=0, zw_3d=0)  # nan value
    ds_3d = ds_3d.reset_index(["zu_3d", "zw_3d"])
    return ds_3d


def calc_temp_spac_means(ds):
    TempSpacMeanU = ds.u.sum(dim=["xu", "y", "time"]) / (ds.x.size * ds.y.size * ds.time.size)
    TempSpacMeanV = ds.v.sum(dim=["x", "yv", "time"]) / (ds.x.size * ds.y.size * ds.time.size)
    TempSpacMeanW = ds.w.sum(dim=["x", "y", "time"]) / (ds.x.size * ds.y.size * ds.time.size)
    return TempSpacMeanU, TempSpacMeanV, TempSpacMeanW
