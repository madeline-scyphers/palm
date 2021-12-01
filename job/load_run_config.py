from pathlib import Path

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


def default_config(domain_fraction, plot_size_x, plot_size_y, job_name=None):
    job_name = job_name if job_name is not None else "default_job_name"
    config = {
        "job_name": job_name,
        "domain": {
            "x": 96,
            "y": 216,
            "z": 5
        },
        "house": {
            "domain_fraction": domain_fraction,
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