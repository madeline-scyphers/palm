from pathlib import Path
import numpy as np
import click

from analysis_utils import load_data_set


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
def analye_data(input_dir, output_dir, job_name):
    job_name = "1"

    lad_path = Path(input_dir) / job_name / f"INPUT/{job_name}_static"

    data_3d_path = sorted(output_dir.glob("*3d*.nc"))[-1]
    data_pr_path = sorted(output_dir.glob("*pr*.nc"))[-1]
    ds_3d = load_data_set(data_3d_path)
    ds_pr = load_data_set(data_pr_path)
    ds_3d = ds_3d.rename({"zu_3d": "z"})
    ds_lad = load_data_set(lad_path)
    ds_lad = ds_lad.rename({"zlad": "z"})
    ds_3d = ds_3d.drop_isel(z=[0, 1, -1], x=-1, y=-1)

    ds_pr = ds_pr.rename({"zwv_01": "z"})
    ds_pr = ds_pr.interp(zwu_01=ds_pr.z)

    dz = 3

    z_scalar = np.arange(150 // dz, 300 // dz)

    urban_ratio = 0.5
    y_domain = np.arange(int(ds_3d.s.y.size * urban_ratio), ds_3d.s.y.size)

    ds_3d = ds_3d.interp(xu=ds_3d.x, yv=ds_3d.y, zw_3d=ds_3d.z)

    ustar = (ds_pr.wu_01**2 + ds_pr.wv_01**2) ** (1 / 4)

    tot = ds_3d.uu + ds_3d.vv + ds_3d.ww

    ubar = tot ** (1 / 2)

    ustar_bar = ustar.isel(z=0).mean()

    DR = ubar.isel(y=y_domain) * ds_3d.s.isel(y=y_domain)

    lai_vals = ds_lad.lad.sum(dim="z").values
    lai = lai_vals[lai_vals != 0].mean()

    ubar_z_scalar = ubar.isel(y=y_domain, z=z_scalar).mean(skipna=True)
    scalar_gradient = ds_3d.isel(y=y_domain, z=z_scalar).s.mean(skipna=True)

    r_a = ubar_z_scalar / (ustar_bar**2) + 6.2 / (ustar_bar ** (2 / 3))
    Depos = DR.mean(skipna=True) * ds_lad.lad.mean(skipna=True)

    r_ca = ustar_bar * lai * (scalar_gradient / Depos - r_a - 1 / (ustar_bar * lai)).compute()
    print(r_ca.values)
    file_path = output_dir / f"r_ca.txt"
    with open(file_path, "w") as f:
        print(f"writing out here: {file_path}")
        f.write(str(r_ca.values))


if __name__ == "__main__":
    analye_data()
