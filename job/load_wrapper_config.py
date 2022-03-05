from pathlib import Path
import datetime as dt

import yaml

__all__ = ["config", "get_wrapper_config", "USER_CODE_MODULE"]

current_dir = Path(__file__).resolve().parent

USER_CODE_MODULE = current_dir / "user_module.f90"

TEMPLATE_DIR = str((current_dir / "palm_config_template.txt").resolve())


def get_config(file: str = "wrapper_config.yaml") -> dict:
    with open(current_dir / file, "r") as f:
        config = yaml.safe_load(f)
    return config


config = get_config()
del get_config
del current_dir


def get_wrapper_config(
        domain_x=int(192 / 6),
        domain_y=int(432 / 6),
        dx=3 * 6,
        dy=3 * 6,
        dz=3,
        urban_ratio=0.8,
        house_plot_ratio=2/7,
        plot_footprint=700,
        plot_ratio=0.70,
        output_start_time=0,
        output_end_time=300,
        template_path=TEMPLATE_DIR,
        job_name=None):
    job_name = job_name if job_name is not None else dt.datetime.now().strftime("%Y%m%dT%H%M%S")
    config = {
        "job_name": job_name,
        "output_start_time": output_start_time,
        "output_end_time": output_end_time,
        "template_path": template_path,
        "domain": {
            "x": domain_x,
            "y": domain_y,
            "dx": dx,
            "dy": dy,
            "dz": dz,
            "urban_ratio": urban_ratio
        },
        "house": {
            "footprint": int(plot_footprint * house_plot_ratio),  # in square meters
            "height": 2,
        },
        "plot": {
            "plot_footprint": plot_footprint,
            "plot_ratio": plot_ratio
        },
    }
    return config
