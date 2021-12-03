import itertools
import os
import subprocess
from typing import Iterable
import logging
import datetime as dt

from pprint import pformat

import numpy as np

from job.run import main


logging.basicConfig(filename=f'{dt.datetime.now().strftime("%Y%m%dT%H%M%S")}.log', encoding='utf-8', level=logging.INFO)

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
                run_job(plot_width, plot_height)
            except TypeError as e:
                logging.exception(e)
                
def get_possible_plot_sizes(plot_width_factors: Iterable):
    for length, _ in enumerate(plot_width_factors, start=1):
        for subset in itertools.combinations(plot_width_factors, length):
            yield np.prod(subset)

def run_job(plot_width, plot_height):
    wrapper_config = main(house_domain_fraction=4, plot_size_x=plot_width, plot_size_y=plot_height)
    
    logging.INFO("Starting new job %s", wrapper_config["job_name"])


    os.chdir("current_version")

    # print("process running!")
    result = subprocess.run(["sh", "start_job.sh", wrapper_config["job_name"]], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    logging.INFO("stdout: ", result.stdout)

    logging.INFO(summary)
    logging.INFO(pformat(wrapper_config))

    logging.INFO("\nscript done")