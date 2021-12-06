from dataclasses import asdict


import pandas as pd

from analyze_delta_s0 import AnalyzeRun, ConfigTracker
from parameters import job_path, data_path, lad_path, canopy_path, config_path

def run():
    JOB = "20211205T141223"
    data = data_path(job_path(JOB), JOB)
    lad = lad_path(job_path(JOB), JOB)
    config = config_path(job_path(JOB))
    canopy = canopy_path(job_path(JOB))
    
    runner = AnalyzeRun(
        data_path_3d=data,
        data_path_lad=lad,
        run_config=config,
        canopy_csv=canopy
    )
    
    cfgs = [runner.substantiate_config_tracker(), runner.substantiate_config_tracker()]
    
    # pd.DataFrame([asdict(cfg) for cfg in cfgs])
    # print("stops")
    # print(config_tracker)

if __name__ == "__main__":
    run()
    