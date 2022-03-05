from __future__ import annotations

from pathlib import Path


def generate_job_config(config: dict) -> dict:
    with open(config["template_path"]) as template:
        job_config = template.read()
    job_cfg = job_config.format(domain_x=config["domain"]["x"] - 1, domain_y=config["domain"]["y"] - 1,
                                output_start_time=config["output_start_time"], output_end_time=config["output_end_time"],
                                dx=config["domain"]["dx"], dy=config["domain"]["dy"], dz=config["domain"]["dz"]
                                )
    return job_cfg
