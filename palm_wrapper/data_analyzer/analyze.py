import json
from pathlib import Path
from pprint import pprint
import json
import dask

import click
import numpy as np

from .analysis_utils import load_data_set

dask.config.set({"array.chunk-size": "512 MiB"})


@click.command()
@click.option(
    "-id",
    "--input_dir",
    type=click.Path(path_type=Path),
    help="Directory of input configurations",
)
@click.option(
    "-od",
    "--output_dir",
    type=click.Path(path_type=Path),
    help="Directory of output data.",
)
@click.option(
    "-jn",
    "--job_name",
    default="1",
    type=str,
    help="Name of job.",
)
def analyze_data(input_dir, output_dir, job_name):

    lad_path = Path(input_dir) / job_name / f"INPUT/{job_name}_static"
    config_path = Path(input_dir) / job_name / "wrapper_config/wrapper_config.json"
    with open(config_path, "r") as f:
        config = json.load(f)

    dz = config["domain"]["dz"]

    data_3d_path = sorted(output_dir.glob("*3d*.nc"))[0]
    data_pr_path = sorted(output_dir.glob("*pr*.nc"))[0]
    ds_3d = load_data_set(data_3d_path)
    ds_pr = load_data_set(data_pr_path)
    ds_3d = ds_3d.rename({"zu_3d": "z"})
    ds_lad = load_data_set(lad_path)
    ds_lad = ds_lad.rename({"zlad": "z"})
    ds_3d = ds_3d.drop_isel(z=0, zw_3d=0)

    scalar_exchange_coeff = 1

    ds_3d["xu"] = ds_3d.x
    ds_3d["yv"] = ds_3d.y
    ds_3d["zw_3d"] = ds_3d.z

    ds_3d = ds_3d.interp(xu=ds_3d.x, yv=ds_3d.y, zw_3d=ds_3d.z)

    urban_ratio = config["domain"]["urban_ratio"]
    y_domain = np.arange(int(ds_3d.s.y.size * urban_ratio), ds_3d.s.y.size)

    z_scalar = np.arange(150 // dz, 300 // dz)

    tot = ds_3d.uu + ds_3d.vv + ds_3d.ww
    ubar = tot ** (1 / 2)

    DR = scalar_exchange_coeff * ubar.isel(y=y_domain) * ds_3d.s.isel(y=y_domain) * ds_lad.isel(y=y_domain).lad

    lai_vals = ds_lad.lad.sum(dim="z").values
    lai = lai_vals.mean() * dz

    ubar_z_scalar = ubar.isel(y=y_domain, z=z_scalar).mean(skipna=True)
    scalar_gradient = ds_3d.isel(y=y_domain, z=z_scalar).s.mean(skipna=True)

    masks = ["00", "01", "02"]
    r_cas = []
    for mask in masks:

        ds_pr = ds_pr.rename({f"zwv_{mask}": f"z_{mask}"})
        ds_pr = ds_pr.drop_isel({f"z_{mask}": 0})
        ds_pr = ds_pr.interp({f"zwu_{mask}": ds_pr[f"z_{mask}"]})

        ustar = (ds_pr[f"wu_{mask}"] ** 2 + ds_pr[f"wv_{mask}"] ** 2) ** (1 / 4)
        ustar_bar = ustar.isel({f"z_{mask}": z_scalar}).mean()

        r_a = ubar_z_scalar / (ustar_bar ** 2) + 6.2 / (ustar_bar ** (2 / 3))
        Depos = DR.mean(skipna=True)

        r_ca = ustar_bar * lai * (scalar_gradient / Depos - r_a - 1 / (ustar_bar * lai)).compute()
        r_cas.append(r_ca.values)
        print(f"r_ca value for mask {mask} = {r_ca.values}")
    # print(r_ca.values)
    # data = {"1": r_cas[0], "2": r_cas[2]}
    data = {i + 1: str(r_ca) for i, r_ca in enumerate(r_cas)}
    file_path = output_dir / f"r_ca.json"
    with open(file_path, "w") as f:
        print(f"writing out here: {file_path}")
        pprint(data)
        json.dump(data, f)

    # ustar_above_canopy = ustar.z > ds_lad.z.max()
    # first_ustar_above = ustar.z[ustar_above_canopy][0]
    # ustar_bar = ustar.sel(z=first_ustar_above).mean()


if __name__ == "__main__":
    analyze_data()
