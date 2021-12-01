from domain import Domain, House, Cell
from load_run_config import default_config
from generate_canopy import get_lad_netcdf
from utils import get_factors_rev, safe_open
from generate_job_config import generate_job_config
from definitions import JOBS_PATH
from __version__ import __version__ as VERSION

import argparse


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
        "-n", "--name", type=str
        )
    parser.add_argument(
        "-df", "--house_domain_fraction", type=int, required=True
        )
    parser.add_argument(
        "-px", "--plot_size_x", type=int, required=True
        )
    parser.add_argument(
        "-py", "--plot_size_y", type=int, required=True
        )

    return parser

def setup_domain(cfg):
    house_fraction_denominator = cfg["house"]["domain_fraction"]

    factors = get_factors_rev(house_fraction_denominator)
    x_factor = next(factors)
    y_factor = next(factors)

    plot_size = cfg["plot_size"]

    house = House(plot_size["x"] / x_factor, plot_size["y"] / y_factor, cfg["house"]["height"])

    return Domain.from_domain_config(house, cfg)
    
def write_output(domain: Domain, config, job_config, ds):
    job_path = JOBS_PATH / config['job_name'] / "INPUT"
    with safe_open(job_path / f"{config['job_name']}_topo", "w") as f:
        f.write(str(domain))
        
    with safe_open(job_path / f"{config['job_name']}_p3d", "w") as f:
        f.write(job_config)
        
    # with open("tree.txt", "w") as f:
    #     f.write(domain.print_tree_matrix())

    ds.to_netcdf(job_path / f"{config['job_name']}_static", format="NETCDF3_64BIT")
    

def main():
    parser = init_argparse()

    args = parser.parse_args()
    config = default_config(
        domain_fraction=args.house_domain_fraction,
        plot_size_x=args.plot_size_x,
        plot_size_y=args.plot_size_y,
        job_name=args.name
        )
    domain = setup_domain(config)
    job_config = generate_job_config(config)
    ds = get_lad_netcdf(job_name=config["job_name"], tree_matrix=domain.trees_matrix)
    write_output(domain, config, job_config, ds)

if __name__ == "__main__":
    main()