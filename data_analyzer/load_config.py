from pathlib import Path

import yaml


__all__ = ["config"]


current_dir = Path(__file__).resolve().parent


def get_config(file: str = "job_config.yaml") -> dict:
    with open(current_dir / file, "r") as f:
        config = yaml.safe_load(f)
    return config


# consts = get_config()
config = get_config()
del get_config
del current_dir
