import itertools
import os
import subprocess
import logging
import datetime as dt
import shutil
from typing import Iterable

from pathlib import Path
from pprint import pformat

import numpy as np

from job import run
from definitions import JOBS_DIR

ONE_MIN = 60
TEN_MIN = 10 * ONE_MIN
ONE_HOUR = 60 * ONE_MIN

OUTPUT_START_TIME = 6 * ONE_HOUR
OUTPUT_END_TIME = 6 * ONE_HOUR + TEN_MIN

log_dir = Path().resolve() / "run_logs"
log_dir.mkdir(exist_ok=True)

logging.basicConfig(filename=log_dir / f'{dt.datetime.now().strftime("%Y%m%dT%H%M%S")}.log', 
                    encoding='utf-8', 
                    level=logging.INFO,
                    format='%(asctime)s | %(name)s | %(levelname)s | %(message)s'
                    )
logging.getLogger().addHandler(logging.StreamHandler())

summary = """
----------------- JOB WRAPPER CONFIG -----------------

"""

def main():

    plot_width_factors = 2,2,2,2,2,3

    plot_height_factors = 2,2,2,3,3,3

    plot_widths = set(get_possible_plot_sizes(plot_width_factors))
    plot_heights = set(get_possible_plot_sizes(plot_height_factors))

    # plot_widths = [4, 8, 12, 16]
    # plot_heights = [2, 4, 8, 12, 16, 32]
        
    # for plot_width in plot_widths:
    #     for plot_height in plot_heights:
    #         run_job(plot_width, plot_height)
    

    run_job(2, 8, tree_domain_fraction=4)
    run_job(2, 12, tree_domain_fraction=4)
    run_job(4, 4, tree_domain_fraction=4)
    run_job(4, 8, tree_domain_fraction=4)
    run_job(4, 18, tree_domain_fraction=4)
    run_job(8, 8, tree_domain_fraction=4)
    run_job(8, 16, tree_domain_fraction=4)
    run_job(16, 24, tree_domain_fraction=4)
    run_job(32, 24, tree_domain_fraction=4)
    
    run_job(32, 36, tree_domain_fraction=4)
    run_job(32, 72, tree_domain_fraction=4)
    run_job(48, 72, tree_domain_fraction=4)
    run_job(96, 72, tree_domain_fraction=4)
    run_job(96, 108, tree_domain_fraction=4)
                
def get_possible_plot_sizes(plot_width_factors: Iterable):
    for length, _ in enumerate(plot_width_factors, start=1):
        for subset in itertools.combinations(plot_width_factors, length):
            yield np.prod(subset)

def run_job(plot_width, plot_height, **kwargs):
    try:
        os.chdir(f'{os.path.expanduser("~")}/palm')
        wrapper_config = run.get_config(
            plot_size_x=plot_width, plot_size_y=plot_height, house_domain_fraction=4,
            output_start_time=OUTPUT_START_TIME, output_end_time=OUTPUT_END_TIME, **kwargs)
    
        _run_job(wrapper_config)
    except TypeError as e:
        logging.exception(e)
        
        job_dir_to_remove = JOBS_DIR / wrapper_config['job_name']
        if job_dir_to_remove.exists():
            shutil.rmtree(job_dir_to_remove)

def _run_job(wrapper_config):
    run.create_input_files(wrapper_config)
    
    logging.info("Starting new job %s", wrapper_config["job_name"])


    os.chdir("current_version")

    result = subprocess.run(["sh", "start_job.sh", wrapper_config["job_name"], str(wrapper_config["output_end_time"])], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    logging.info("stdout: \n%s", str(result.stdout))

    logging.info(summary)
    logging.info(pformat(wrapper_config))

    logging.info("\nscript done")


if __name__ == "__main__":
    logging.info("Starting script at %s", dt.datetime.now().strftime("%Y%m%dT%H%M%S"))

    main()