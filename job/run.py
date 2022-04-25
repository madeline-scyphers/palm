import argparse
import json

import numpy as np
from definitions import JOBS_DIR

from .domain import Cell, Domain, House, setup_domain
from .generate_canopy import get_lad_netcdf
from .generate_job_config import generate_job_config, generate_user_module
from .load_wrapper_config import USER_CODE_MODULE, get_wrapper_config
from .utils import get_factors_rev, make_dirs


def write_output(domain: Domain, config, job_config, ds, job_dir):

    jobs = job_dir / config["job_name"]
    input_path = jobs / "INPUT"
    user_code_path = jobs / "USER_CODE"
    wrapper_config_path = jobs / "wrapper_config"
    make_dirs([input_path, user_code_path, wrapper_config_path])

    with open(input_path / f"{config['job_name']}_topo", "w") as f:
        f.write(str(domain))

    with open(input_path / f"{config['job_name']}_p3d", "w") as f:
        f.write(job_config)

    with open(user_code_path / "user_module.f90", "w") as f:
        # user_code_module = open(USER_CODE_MODULE).read()
        user_code_module = generate_user_module(domain)
        f.write(user_code_module)

    ds.to_netcdf(input_path / f"{config['job_name']}_static", format="NETCDF3_64BIT")

    domain.save_matrix(wrapper_config_path / "topo.csv")
    domain.save_matrix(wrapper_config_path / "canopy.csv", matrix_name="trees_matrix")
    domain.subplot.save_matrix(wrapper_config_path / "cell.csv")
    domain.subplot.subplot.save_matrix(wrapper_config_path / "house.csv")
    with open(wrapper_config_path / "wrapper_config.json", "w") as f:
        json.dump(config, f)


def get_config(**kwargs):
    config = get_wrapper_config(**kwargs)
    return config


def create_input_files(
    config,
    job_dir=JOBS_DIR,
):

    domain = setup_domain(config)
    job_config = generate_job_config(config)
    ds = get_lad_netcdf(
        job_name=config["job_name"],
        tree_matrix=domain.trees_matrix,
        dx=config["domain"]["dx"],
        dy=config["domain"]["dy"],
        dz=config["domain"]["dz"],
        mean_lai=config["canopy"]["mean_lai"],
    )
    write_output(domain, config, job_config, ds, job_dir)


def main(job_dir=JOBS_DIR, **kwargs):

    config = get_config(**kwargs)

    create_input_files(config, job_dir)

    return config


if __name__ == "__main__":
    print(main())
