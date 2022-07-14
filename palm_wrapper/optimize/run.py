"""
palm_wrapper optimization
-------------------
Runs optimization for wrapper for PALM
Options for the optimization are set in the .yaml file.
This script is meant to be run from the command line, and the optimization configuration .yaml
file is specified as a command line argument, for example::
      python run_optimization.py --config_path /path/to/config/file.yaml
"""

import datetime as dt
import logging
import time
from pathlib import Path


import click
from boa import (
    WrappedJobRunner,
    get_experiment,
    get_scheduler,
    scheduler_to_json_file,
)

from palm_wrapper.optimize.wrapper import Wrapper


@click.command()
@click.option(
    "-f",
    "--config_path",
    type=click.Path(exists=True, dir_okay=False, path_type=Path),
    default=Path(__file__).resolve().parent / "opt_config.yaml",
    help="Path to configuration YAML file.",
)
def main(config_path):
    """This is my docstring
    Args:
        config (os.PathLike): Path to configuration YAML file
    """
    start = time.time()

    wrapper = Wrapper()
    config = wrapper.load_config(config_path)

    log_format = "%(levelname)s %(asctime)s - %(message)s"
    logging.basicConfig(
        filename=Path(wrapper.experiment_dir) / "optimization.log",
        filemode="w",
        format=log_format,
        level=logging.DEBUG,
    )
    logging.getLogger().addHandler(logging.StreamHandler())
    logger = logging.getLogger(__file__)
    logger.info("Start time: %s", dt.datetime.now().strftime("%Y%m%dT%H%M%S"))

    experiment = get_experiment(config, WrappedJobRunner(wrapper=wrapper), wrapper)
    scheduler = get_scheduler(experiment, config=config)

    try:
        scheduler.run_all_trials()
    finally:
        logging.info("\nTrials completed! Total run time: %d", time.time() - start)
        scheduler_to_json_file(scheduler, wrapper.experiment_dir / "scheduler.json")
    return scheduler


if __name__ == "__main__":
    main()
