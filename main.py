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

log_dir = Path().resolve() / "logs"
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
    
    
    
    params = [
        {'plot_footprint': 793, 'house_ratio': 0.23399696312844753, 'ground_ratio': 0.712415256537497, 'mean_lai': 3.5729792695492506, 'domain_x': 48, 'domain_y': 144},
        {'plot_footprint': 883, 'house_ratio': 0.13372371066361666, 'ground_ratio': 0.4194803750142455, 'mean_lai': 4.488054119050503, 'domain_x': 48, 'domain_y': 144},
        {'plot_footprint': 453, 'house_ratio': 0.10799476783722639, 'ground_ratio': 0.5507028270512819, 'mean_lai': 2.088366985321045, 'domain_x': 48, 'domain_y': 144},
        {'plot_footprint': 689, 'house_ratio': 0.1954153785482049, 'ground_ratio': 0.7948569608852267, 'mean_lai': 4.824529131874442, 'domain_x': 48, 'domain_y': 144},
        {'plot_footprint': 998, 'house_ratio': 0.35983916465193033, 'ground_ratio': 0.601067315787077, 'mean_lai': 3.9796842988580465, 'domain_x': 48, 'domain_y': 144},
        {'plot_footprint': 382, 'house_ratio': 0.39648958947509527, 'ground_ratio': 0.4932594681158662, 'mean_lai': 3.4438284914940596, 'domain_x': 48, 'domain_y': 144},
        {'plot_footprint': 398, 'house_ratio': 0.2549444977194071, 'ground_ratio': 0.6947077717632055, 'mean_lai': 2.934372689574957, 'domain_x': 48, 'domain_y': 144},
        {'plot_footprint': 603, 'house_ratio': 0.1513266609981656, 'ground_ratio': 0.6187597988173366, 'mean_lai': 3.141808945685625, 'domain_x': 48, 'domain_y': 144},
        {'plot_footprint': 863, 'house_ratio': 0.12163377087563276, 'ground_ratio': 0.47654380463063717, 'mean_lai': 4.094223972409964, 'domain_x': 48, 'domain_y': 144},
        {'plot_footprint': 664, 'house_ratio': 0.3460772568359971, 'ground_ratio': 0.4252256229519844, 'mean_lai': 2.349442543461919, 'domain_x': 48, 'domain_y': 144},
        {'plot_footprint': 760, 'house_ratio': 0.3790088286623359, 'ground_ratio': 0.5439812364056706, 'mean_lai': 4.414590263739228, 'domain_x': 48, 'domain_y': 144},
        {'plot_footprint': 527, 'house_ratio': 0.32524664606899023, 'ground_ratio': 0.5201046532019973, 'mean_lai': 4.965688589960337, 'domain_x': 48, 'domain_y': 144},
        {'plot_footprint': 652, 'house_ratio': 0.17734538298100233, 'ground_ratio': 0.4671788774430752, 'mean_lai': 3.5196363795548677, 'domain_x': 48, 'domain_y': 144},
        {'plot_footprint': 726, 'house_ratio': 0.081920494325459, 'ground_ratio': 0.5625117057934403, 'mean_lai': 2.9663737509399652, 'domain_x': 48, 'domain_y': 144},
        {'plot_footprint': 447, 'house_ratio': 0.291501235216856, 'ground_ratio': 0.3443353408947587, 'mean_lai': 4.056293407455087, 'domain_x': 48, 'domain_y': 144},
        {'plot_footprint': 388, 'house_ratio': 0.2059640735387802, 'ground_ratio': 0.6664238292723894, 'mean_lai': 4.48176146671176, 'domain_x': 48, 'domain_y': 144},
        {'plot_footprint': 960, 'house_ratio': 0.3428603848442435, 'ground_ratio': 0.43801200669258833, 'mean_lai': 2.845814563333988, 'domain_x': 48, 'domain_y': 144},
        {'plot_footprint': 1008, 'house_ratio': 0.1635807929560542, 'ground_ratio': 0.5102092549204826, 'mean_lai': 2.6161319818347692, 'domain_x': 48, 'domain_y': 144},
        {'plot_footprint': 414, 'house_ratio': 0.06442751456052065, 'ground_ratio': 0.3946055443957448, 'mean_lai': 4.71040384285152, 'domain_x': 48, 'domain_y': 144},
        {'plot_footprint': 869, 'house_ratio': 0.3050725869834423, 'ground_ratio': 0.6763042481616139, 'mean_lai': 2.3079389464110136, 'domain_x': 48, 'domain_y': 144},
]
    for param in params:
        run_job(**param)

    # plot_width_factors = 2,2,2,2,2,3

    # plot_height_factors = 2,2,2,3,3,3

    # plot_widths = set(get_possible_plot_sizes(plot_width_factors))
    # plot_heights = set(get_possible_plot_sizes(plot_height_factors))

    # plot_widths = [4, 8, 12, 16]
    # plot_heights = [2, 4, 8, 12, 16, 32]
        
    # for plot_width in plot_widths:
    #     for plot_height in plot_heights:
    #         run_job(plot_width, plot_height)
    

    # run_job()
    # run_job(2, 12, tree_domain_fraction=4)
    # run_job(4, 4, tree_domain_fraction=4)
    # run_job(4, 8, tree_domain_fraction=4)
    # run_job(4, 18, tree_domain_fraction=4)
    # run_job(8, 8, tree_domain_fraction=4)
    # run_job(8, 16, tree_domain_fraction=4)
    # run_job(16, 24, tree_domain_fraction=4)
    # run_job(32, 24, tree_domain_fraction=4)
    
    # run_job(32, 36, tree_domain_fraction=4)
    # run_job(32, 72, tree_domain_fraction=4)
    # run_job(48, 72, tree_domain_fraction=4)
    # run_job(96, 72, tree_domain_fraction=4)
    # run_job(96, 108, tree_domain_fraction=4)
                
def get_possible_plot_sizes(plot_width_factors: Iterable):
    for length, _ in enumerate(plot_width_factors, start=1):
        for subset in itertools.combinations(plot_width_factors, length):
            yield np.prod(subset)

def run_job( **kwargs):
    try:
        os.chdir(f'{os.path.expanduser("~")}/palm')
        # wrapper_config = run.get_config(
        #     plot_size_x=plot_width, plot_size_y=plot_height, house_domain_fraction=4,
        #     output_start_time=OUTPUT_START_TIME, output_end_time=OUTPUT_END_TIME, **kwargs)
        wrapper_config = run.get_config(
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