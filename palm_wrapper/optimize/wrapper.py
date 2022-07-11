"""
Optimization wrapper for FETCH3.

These functions provide the interface between the optimization tool and FETCH3
- Setting up optimization experiment
- Creating directories for model outputs of each iteration
- Writing model configuration files for each iteration
- Starting model runs for each iteration
- Reading model outputs and observation data for model evaluation
- Defines objective function for optimization, and other performance metrics of interest
- Defines how results of each iteration should be evaluated
"""

import yaml
import pandas as pd
import xarray as xr
import numpy as np
import atexit

from pathlib import Path
import datetime as dt

import subprocess
import os
from pathlib import Path

from ax import Trial

from boa import (
    BaseWrapper,
    get_trial_dir,
    make_trial_dir,
    write_configs,
)

from palm_wrapper.job_submission.run import create_input_files, get_config
from palm_wrapper.data_analyzer.analyze import analye_data


class Wrapper(BaseWrapper):
    def __init__(self, ex_settings, model_settings, experiment_dir):
        self.ex_settings = ex_settings
        self.model_settings = model_settings
        self.experiment_dir = experiment_dir

    def write_configs(self, trial: Trial) -> None:
        job_dir = self.model_settings["job_dir"]
        config = get_config()
        create_input_files(config, job_dir)

    def run_model(self, trial: Trial):
        model_dir = self.model_settings["model_dir"]
        job_name = self.model_settings["job_name"]
        run_time = self.model_settings["run_time"]

        os.chdir(model_dir)

        # cmd = (f"bash start_palm.sh {job_name} {run_time}")
        cmd = (f"bash start_palm.sh {job_name} {run_time}")
        # cmd = (f"palm_run -a -b {job_name} {run_time}")

        args = cmd.split()
        subprocess.Popen(
            args, stdout=subprocess.PIPE, universal_newlines=True
        )

    def set_trial_status(self, trial: Trial) -> None:
        """Get status of the job by a given ID. For simplicity of the example,
        return an Ax `TrialStatus`.
        """
        model_dir = self.model_settings["model_dir"]
        job_name = self.model_settings["job_name"]

        log_file = Path(model_dir) / job_name / "Logs" / f"{job_name}.log"

        if log_file.exists():
            with open(log_file, "r") as f:
                contents = f.read()
            if "Run Failed" in contents:
                trial.mark_failed()
            elif "all OUTPUT-files saved" in contents:
                trial.mark_completed()

    def fetch_trial_data(self, trial: Trial, *args, **kwargs):
        model_dir = self.model_settings["model_dir"]
        job_name = self.model_settings["job_name"]

        modelfile = model_dir / job_name / "OUTPUT" / f"{job_name}_3d.nc"

        return analye_data(modelfile)
