from pathlib import Path
import datetime as dt

import yaml


__all__ = ["config", "default_config"]


current_dir = Path(__file__).resolve().parent


def get_config(file: str = "job_config.yaml") -> dict:
    with open(current_dir / file, "r") as f:
        config = yaml.safe_load(f)
    return config


# consts = get_config()
config = get_config()
del get_config
del current_dir


def default_config(house_domain_fraction, plot_size_x, plot_size_y, job_name=None):
    job_name = job_name if job_name is not None else dt.datetime.now().strftime("%Y%m%dT%H%M")
    assert house_domain_fraction is not None, "house_domain_fraction must be specified"
    assert plot_size_x is not None, "plot_size_x must be specified"
    assert plot_size_y is not None, "plot_size_y must be specified"
    config = {
        "job_name": job_name,
        "domain": {
            "x": 96,
            "y": 216,
            "z": 5
        },
        "house": {
            "domain_fraction": house_domain_fraction,
            "height": 4
        },
        "plot_size": {
            "x": plot_size_x,
            "y": plot_size_y
        },
        "trees": {
            "domain_fraction": 8
        },
        
    }
    return config