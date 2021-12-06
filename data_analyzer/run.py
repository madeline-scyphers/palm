from dataclasses import asdict
from typing import Iterable
import logging
import datetime as dt
from pathlib import Path

import pandas as pd

from analyze_delta_s0 import AnalyzeRun, ConfigTracker
from parameters import job_path, data_path, lad_path, canopy_path, config_path



logging.basicConfig(filename=f'{dt.datetime.now().strftime("%Y%m%dT%H%M%S")}.log', 
                    encoding='utf-8', 
                    level=logging.INFO,
                    format='%(asctime)s | %(name)s | %(levelname)s | %(message)s'
                    )
logging.getLogger().addHandler(logging.StreamHandler())


def get_runner(job):
    data = data_path(job_path(job), job)
    lad = lad_path(job_path(job), job)
    config = config_path(job_path(job))
    canopy = canopy_path(job_path(job))
    
    runner = AnalyzeRun(
        data_path_3d=data,
        data_path_lad=lad,
        run_config=config,
        canopy_csv=canopy
    )
    return runner

def substantiate_runners(runners: Iterable[AnalyzeRun]):
    configs = [runner.substantiate_config_tracker() for runner in runners]
    return configs
    

def run():
    jobs = [
        "20211205T220846",
        "20211205T221030",
        "20211205T221210",
        "20211205T221348",
        "20211205T221528",
        "20211205T222038",
        "20211205T222218",
        
        
        
        # "20211205T233734"
    ]
    
    runners = [get_runner(job=job) for job in jobs]

    cfgs = substantiate_runners(runners)
    
    pd.DataFrame([asdict(cfg) for cfg in cfgs]).to_csv(Path(__file__).parent / f"output/{jobs[0]}-{jobs[-1]}.csv")

if __name__ == "__main__":
    run()
    