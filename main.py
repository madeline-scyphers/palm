import itertools
import os
import subprocess
from typing import Iterable
import logging
import datetime as dt

from pprint import pformat

import numpy as np

from job import run


OUTPUT_START_TIME = 1500
OUTPUT_END_TIME = 1800


logging.basicConfig(filename=f'{dt.datetime.now().strftime("%Y%m%dT%H%M%S")}.log', 
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
    
    for plot_width in plot_widths:
        for plot_height in plot_heights:
            try:
                os.chdir(f'{os.path.expanduser("~")}/palm')
                run_job(plot_width, plot_height)
            except TypeError as e:
                logging.exception(e)
                
def get_possible_plot_sizes(plot_width_factors: Iterable):
    for length, _ in enumerate(plot_width_factors, start=1):
        for subset in itertools.combinations(plot_width_factors, length):
            yield np.prod(subset)

def run_job(plot_width, plot_height):
    wrapper_config = run.main(house_domain_fraction=4, plot_size_x=plot_width, plot_size_y=plot_height, 
                            output_start_time=OUTPUT_START_TIME, output_end_time=OUTPUT_END_TIME)
        
    
    logging.info("Starting new job %s", wrapper_config["job_name"])


    os.chdir("current_version")

    result = subprocess.run(["sh", "start_job.sh", wrapper_config["job_name"], str(wrapper_config["output_end_time"])], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    logging.info("stdout: \n%s", str(result.stdout))

    logging.info(summary)
    logging.info(pformat(wrapper_config))

    logging.info("\nscript done")


if __name__ == "__main__":
    logging.info("Starting script at %s", dt.datetime.now().strftime("%Y%m%dT%H%M%S"))
    # logging.info("Starting script at test")
    
    main()