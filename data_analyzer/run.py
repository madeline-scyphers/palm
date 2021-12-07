from dataclasses import asdict
from typing import Iterable
import logging
import datetime as dt
from pathlib import Path

import pandas as pd

from analyze_delta_s0 import AnalyzeRun, ConfigTracker
from parameters import job_path, data_path, lad_path, canopy_path, config_path


log_dir = Path().resolve() / "logs"
log_dir.mkdir(exist_ok=True)

logging.basicConfig(filename=log_dir / f'{dt.datetime.now().strftime("%Y%m%dT%H%M%S")}.log', 
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
    configs = []
    for runner in runners:
        config = runner.substantiate_config_tracker()
        pd.DataFrame([asdict(config)]).to_csv(Path(__file__).parent / f"output/{config.job_name}.csv")
        configs.append(config)
    return configs
    

def run():
    jobs = [
        # "20211205T220846",
        # "20211205T221030",
        # "20211205T221210",
        # "20211205T221348",
        # "20211205T221528",
        # "20211205T222038",
        # "20211205T222218",
       
       
        
        # "20211205T233734",
        # "20211205T233917",
        # "20211205T234103",
        # "20211205T234245",
        # "20211205T234424",
        # "20211205T234606",
        # "20211205T234747",
        # "20211205T234928",
        # "20211205T235110",
        # "20211205T235250",
        # "20211205T235429",
        # "20211205T235609",
        
        # "20211206T045257",
        # "20211206T045439",
        # "20211206T045618",
        # "20211206T045756",
        # "20211206T045934",
        # "20211206T050632",
        # "20211206T050811",
        # "20211206T050951",
        # "20211206T051135",
        # "20211206T051315",
        # "20211206T051455",
        # "20211206T051639",
        # "20211206T051819",
        "20211206T051957",
        "20211206T052144",
        # "20211206T052325",
    ]
    
    runners = [get_runner(job=job) for job in jobs]

    cfgs = substantiate_runners(runners)
    
    pd.DataFrame([asdict(cfg) for cfg in cfgs]).to_csv(Path(__file__).parent / f"output/{jobs[0]}-{jobs[-1]}.csv")

if __name__ == "__main__":
    run()
    