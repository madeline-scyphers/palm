import datetime as dt
import itertools
import logging
import os
import shutil
import subprocess
from pathlib import Path
from pprint import pformat
from typing import Iterable
from parser import parser
import click

import numpy as np

from definitions import JOBS_DIR
from job import run

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
    "-id",
    "--input_dir",
    type=click.Path(path_type=Path),
    default=JOBS_DIR,
    help="directory to save configuration files to",
)
@click.option(
    "-n",
    "--job_name",
    type=str,
    default="42",
    help="Which job name this job is in a run of jobs.",
)
def main(input_dir, job_name):
    print(input_dir, job_name)
    # params = [
    params = {
            "plot_footprint": 366,
            "house_ratio": 0.17704884335398674,
            "ground_ratio": 0.508383123204112,
            "mean_lai": 3.1202627243474126,
        }
        # {
        #     "plot_footprint": 779,
        #     "house_ratio": 0.29129079822450876,
        #     "ground_ratio": 0.5895595084875822,
        #     "mean_lai": 4.535055342130363,
        # },
        # {
        #     "plot_footprint": 461,
        #     "house_ratio": 0.10465617198497057,
        #     "ground_ratio": 0.43243145383894444,
        #     "mean_lai": 4.513731939718127,
        # },
        # {
        #     "plot_footprint": 731,
        #     "house_ratio": 0.15050092432647943,
        #     "ground_ratio": 0.7963994303718209,
        #     "mean_lai": 2.6298176627606153,
        # },
        # {
        #     "plot_footprint": 566,
        #     "house_ratio": 0.08257363922894001,
        #     "ground_ratio": 0.5652173357084394,
        #     "mean_lai": 2.431219285354018,
        # },
        # {
        #     "plot_footprint": 941,
        #     "house_ratio": 0.44876968022435904,
        #     "ground_ratio": 0.5174893783405423,
        #     "mean_lai": 3.910500142723322,
        # },
        # {
        #     "plot_footprint": 1037,
        #     "house_ratio": 0.27141167782247066,
        #     "ground_ratio": 0.4098602244630456,
        #     "mean_lai": 2.493575076572597,
        # },
        # {
        #     "plot_footprint": 863,
        #     "house_ratio": 0.19023516401648521,
        #     "ground_ratio": 0.7306853020563722,
        #     "mean_lai": 3.654823502525687,
        # },
        # {
        #     "plot_footprint": 876,
        #     "house_ratio": 0.12096619512885809,
        #     "ground_ratio": 0.8494819048792124,
        #     "mean_lai": 2.924783040769398,
        # },
        # {
        #     "plot_footprint": 623,
        #     "house_ratio": 0.13565291743725538,
        #     "ground_ratio": 0.48493407759815454,
        #     "mean_lai": 4.037136648781598,
        # },
        # {
        #     "plot_footprint": 963,
        #     "house_ratio": 0.08621279243379831,
        #     "ground_ratio": 0.4492392996326089,
        #     "mean_lai": 3.8059845492243767,
        # },
        # # # I think this is as far as it got
        # {
        #     "plot_footprint": 408,
        #     "house_ratio": 0.20121390279382467,
        #     "ground_ratio": 0.3466413440182805,
        #     "mean_lai": 2.6082018688321114,
        # },
        # {
        #     "plot_footprint": 580,
        #     "house_ratio": 0.274577927775681,
        #     "ground_ratio": 0.5444309758022428,
        #     "mean_lai": 3.743815534748137,
        # },
        # {
        #     "plot_footprint": 912,
        #     "house_ratio": 0.1310371831059456,
        #     "ground_ratio": 0.6234120326116681,
        #     "mean_lai": 2.2229125713929534,
        # },
        # {
        #     "plot_footprint": 818,
        #     "house_ratio": 0.1811916744336486,
        #     "ground_ratio": 0.38119750656187534,
        #     "mean_lai": 4.640058918856084,
        # },
        # {
        #     "plot_footprint": 487,
        #     "house_ratio": 0.28765164501965046,
        #     "ground_ratio": 0.4584666881710291,
        #     "mean_lai": 3.2013245234265924,
        # },
        # {
        #     "plot_footprint": 665,
        #     "house_ratio": 0.23602234572172165,
        #     "ground_ratio": 0.6513172406703234,
        #     "mean_lai": 4.269555360078812,
        # },
        # {
        #     "plot_footprint": 717,
        #     "house_ratio": 0.10148992203176022,
        #     "ground_ratio": 0.5507906954735518,
        #     "mean_lai": 3.2224684804677963,
        # },
        # {
        #     "plot_footprint": 977,
        #     "house_ratio": 0.22761376574635506,
        #     "ground_ratio": 0.5400458388030529,
        #     "mean_lai": 2.6904906583949924,
        # },
        # {
        #     "plot_footprint": 799,
        #     "house_ratio": 0.3107391279190779,
        #     "ground_ratio": 0.35014111176133156,
        #     "mean_lai": 3.8487979527562857,
        # },
    # ]
    # params = params[:1]
    # for param in params:
    run_job(input_dir, job_name, **params)


def run_job(input_dir, job_name, **kwargs):
    try:
        os.chdir(f'{os.path.expanduser("~")}/palm')

        wrapper_config = run.get_config(output_start_time=OUTPUT_START_TIME, output_end_time=OUTPUT_END_TIME, job_name=job_name, **kwargs)

        _run_job(wrapper_config, input_dir, job_name)
    except TypeError as e:
        logging.exception(e)

        input_dir_to_remove = input_dir / wrapper_config["job_name"]
        if input_dir_to_remove.exists():
            shutil.rmtree(input_dir_to_remove)


def _run_job(wrapper_config, input_dir, job_name):
    run.create_input_files(wrapper_config, input_dir)

    # logging.info("Starting new job %s", wrapper_config["job_name"])

    # os.chdir("current_version")

    # result = subprocess.run(
    #     [
    #         "sh",
    #         "start_job.sh",
    #         wrapper_config["job_name"],
    #         str(JOB_RUN_TIMEOUT_SCALER * wrapper_config["output_end_time"]),
    #         "--b"
    #     ],
    #     stdin=subprocess.PIPE,
    #     stdout=subprocess.PIPE,
    #     stderr=subprocess.PIPE,
    # )

    # logging.info("stdout: \n%s", str(result.stdout))

    # logging.info(summary)
    # logging.info(pformat(wrapper_config))

    # logging.info("\nscript done")


if __name__ == "__main__":
    logging.info("Starting script at %s", dt.datetime.now().strftime("%Y%m%dT%H%M%S"))

    main()
