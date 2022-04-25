import datetime as dt
import logging
import os
import shutil
import subprocess
from pathlib import Path
from pprint import pformat

import click
from job_submission import run
from optiwrap import read_experiment_config

ONE_MIN = 60
TEN_MIN = 10 * ONE_MIN
ONE_HOUR = 60 * ONE_MIN

OUTPUT_START_TIME = 6 * ONE_HOUR
OUTPUT_END_TIME = 6 * ONE_HOUR + TEN_MIN

OUTPUT_START_TIME = 0
OUTPUT_END_TIME = int(30 * ONE_MIN)

JOB_RUN_TIMEOUT_SCALER = 6

log_dir = Path().resolve() / "logs"
log_dir.mkdir(exist_ok=True)

logging.basicConfig(
    filename=log_dir / f'{dt.datetime.now().strftime("%Y%m%dT%H%M%S")}.log',
    encoding="utf-8",
    level=logging.INFO,
    format="%(asctime)s | %(name)s | %(levelname)s | %(message)s",
)
logging.getLogger().addHandler(logging.StreamHandler())

summary = """
----------------- JOB WRAPPER CONFIG -----------------

"""


@click.command()
@click.option(
    "-n",
    "--job_name",
    type=str,
    default="42",
    help="Which job name this job is in a run of jobs.",
)
@click.option(
    "-f",
    "--config_file",
    type=click.Path(exists=True, dir_okay=False, path_type=Path),
    default=str(Path(__file__).parent / "wrapper_config.yaml"),
    help="Path to configuration YAML file.",
)
def main(job_name, config_file):
    config = read_experiment_config(config_file)
    params = config["model_options"]
    run_job(job_name, ex_settings=config["optimization_options"], **params)


def run_job(job_name, ex_settings, **kwargs):
    input_dir = Path(ex_settings["input_dir"])
    working_dir = Path(ex_settings.get("working_dir", "~/palm"))
    try:
        os.chdir(working_dir.expanduser())

        wrapper_config = run.get_config(
            output_start_time=OUTPUT_START_TIME, output_end_time=OUTPUT_END_TIME, job_name=job_name, **kwargs
        )

        _run_job(wrapper_config, input_dir, ex_settings)
    except TypeError as e:
        logging.exception(e)

        input_dir_to_remove = input_dir / wrapper_config["job_name"]
        if input_dir_to_remove.exists():
            shutil.rmtree(input_dir_to_remove)


def _run_job(wrapper_config, input_dir, ex_settings):
    run.create_input_files(wrapper_config, input_dir)

    if not ex_settings["dry_run"]:
        logging.info("Starting new job %s", wrapper_config["job_name"])

        os.chdir("current_version")

        cmd = (
            f'palmrun -r $job_name -c default -X48 -T24 -q parallel -t 120 -a"{ex_settings.get("job_type", "d3#")}" -v'
        )
        args = cmd.split()

        result = subprocess.run(
            args,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

        logging.info("stdout: \n%s", str(result.stdout))

        logging.info(summary)
        logging.info(pformat(wrapper_config))

        logging.info("\nscript done")


if __name__ == "__main__":
    logging.info("Starting script at %s", dt.datetime.now().strftime("%Y%m%dT%H%M%S"))

    main()
