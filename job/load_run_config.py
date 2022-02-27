from pathlib import Path
import datetime as dt

import yaml


__all__ = ["config", "default_config"]


current_dir = Path(__file__).resolve().parent

USER_CODE_MODULE = current_dir / "user_module.f90"


def get_config(file: str = "job_config.yaml") -> dict:
    with open(current_dir / file, "r") as f:
        config = yaml.safe_load(f)
    return config


# consts = get_config()
config = get_config()
del get_config
del current_dir


def default_config(
                #    plot_size_x, 
                #    plot_size_y,
                   domain_x=192,
                   domain_y=432,
                   dx=3,
                   dy=3,
                   dz=3,
                   house_footprint=200,
                   plot_footprint=700,
                   plot_ratio=0.71,
                   tree_domain_fraction=4,
                   output_start_time=0,
                   output_end_time=300, 
                   job_name=None):
    job_name = job_name if job_name is not None else dt.datetime.now().strftime("%Y%m%dT%H%M%S")
    assert house_footprint is not None, "house_domain_fraction must be specified"
    # assert plot_size_x is not None, "plot_size_x must be specified"
    # assert plot_size_y is not None, "plot_size_y must be specified"
    config = {
        "job_name": job_name,
        "output_start_time": output_start_time,
        "output_end_time": output_end_time,
        "domain": {
            "x": domain_x,
            "y": domain_y,
            "z": 5,
            "dx": dx,
            "dy": dy,
            "dz": dz,
            "urban_ratio": 0.5
        },
        "house": {
            "footprint": int(house_footprint),  # in square meters
            "height": 4,
            "padding": 1,
            
        },
        "plot": {
            "plot_footprint": plot_footprint,
            "plot_ratio": plot_ratio
        },
        "road": {
            "width": 6 / dx
        },
        # "plot_size": {
        #     "x": int(plot_size_x),
        #     "y": int(plot_size_y)
        # },
        "trees": {
            "domain_fraction": tree_domain_fraction
        },
        
    }
    return config