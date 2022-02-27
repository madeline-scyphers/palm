import argparse
import json

import numpy as np

from .domain import Domain, House, Cell, setup_domain
from .load_run_config import default_config, USER_CODE_MODULE
from .generate_canopy import get_lad_netcdf
from .utils import get_factors_rev, make_dirs
from .generate_job_config import generate_job_config
from definitions import JOBS_DIR
from __version__ import __version__ as VERSION


def init_argparse() -> argparse.ArgumentParser:

    parser = argparse.ArgumentParser(

        usage="%(prog)s [OPTION] [FILE]...",

        description="Generate input values for palm"

    )

    parser.add_argument(
        "-V", "--version", action="version",
        version = f"{parser.prog} version {VERSION}"
    )
    parser.add_argument(
        "-n", "--job_name", type=str
        )
    parser.add_argument(
        "-px", "--plot_size_x", type=int
        )
    parser.add_argument(
        "-py", "--plot_size_y", type=int
        )
    parser.add_argument(
        "-st", "--output_start_time", type=int
        )
    parser.add_argument(
        "-et", "--output_end_time", type=int
        )

    return parser
    
def write_output(domain: Domain, config, job_config, ds):
    
    jobs = JOBS_DIR / config['job_name']
    input_path = jobs / "INPUT"
    user_code_path = jobs / "USER_CODE"
    wrapper_config_path = jobs / "wrapper_config"
    dir_to_make = [input_path, user_code_path, wrapper_config_path]
    make_dirs(dir_to_make)
    
    with open(input_path / f"{config['job_name']}_topo", "w") as f:
        f.write(str(domain))
        
    with open(input_path / f"{config['job_name']}_p3d", "w") as f:
        f.write(job_config)
        
    with open(user_code_path / "user_module.f90", "w") as f:
        user_code_module = open(USER_CODE_MODULE).read()
        f.write(user_code_module)
        
    ds.to_netcdf(input_path / f"{config['job_name']}_static", format="NETCDF3_64BIT")

    domain.save_matrix(wrapper_config_path / "topo.csv")
    domain.save_matrix(wrapper_config_path / "canopy.csv",  matrix_name="trees_matrix")
    domain.subplot.save_matrix(wrapper_config_path / "cell.csv")
    domain.subplot.subplot.save_matrix(wrapper_config_path / "house.csv")
    with open(wrapper_config_path / "wrapper_config.json", "w") as f:
        json.dump(config, f)

def parse_args(parser: argparse.ArgumentParser, kwargs):
    args = parser.parse_args()
    # kwargs = _parse_single_arg("plot_size_x", args, kwargs)
    # kwargs = _parse_single_arg("plot_size_y", args, kwargs)
    # kwargs = _parse_single_arg("job_name", args, kwargs)
    # kwargs = _parse_single_arg("output_start_time", args, kwargs)
    # kwargs = _parse_single_arg("output_end_time", args, kwargs)
    return kwargs

def _parse_single_arg(arg: str, args: argparse.Namespace, kwargs):
    if arg not in kwargs:
        kwargs[arg] = getattr(args, arg)
    return kwargs

def validate_domain(domain, config):
    try:
        # assert (
        #     (domain.x * domain.y) // domain.subplot.tree_domain_fraction == domain.trees_matrix.sum() if domain.subplot.tree_domain_fraction is not None
        #     else 0 == domain.trees_matrix.sum()
        #     ), (
        #     f"Number of trees in trees matrix \n{domain.subplot.trees} \n(size: {domain.trees_matrix.sum()}) not expected number of trees: "
        #     f"{(domain.x * domain.y) // domain.subplot.tree_domain_fraction}")
        assert domain.matrix.shape == (config["domain"]["y"], config["domain"]["x"])
        # assert np.count_nonzero(domain.matrix) == (config["domain"]["x"] * config["domain"]["y"]) / config["house"]["domain_fraction"]
        # assert np.count_nonzero(domain.trees_matrix) == (
        #     (config["domain"]["y"] * config["domain"]["x"]) / config["trees"]["domain_fraction"] if config["trees"]["domain_fraction"]
        #     else 0
        #     )
    except AssertionError as e:
        raise TypeError("Invalid domain configuration") from e

def get_config(**kwargs):
    parser = init_argparse()
    
    kwargs = parse_args(parser, kwargs)

    config = default_config(**kwargs)
    return config

def create_input_files(config):

    domain = setup_domain(config)
    validate_domain(domain, config)
    job_config = generate_job_config(config)
    ds = get_lad_netcdf(job_name=config["job_name"], tree_matrix=domain.trees_matrix)
    write_output(domain, config, job_config, ds)

def main(**kwargs):
    
    config = get_config(**kwargs)

    create_input_files(config)
    
    return config

if __name__ == "__main__":
    print(main())