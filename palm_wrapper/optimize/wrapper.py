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

from ax import Trial

from optiwrap import (
    BaseWrapper,
    get_trial_dir,
    make_trial_dir,
    write_configs,
)

from palm_wrapper.job_submission.run import create_input_files, get_config


class Wrapper(BaseWrapper):
    _processes = []
    def __init__(self, ex_settings, model_settings, experiment_dir):
        self.ex_settings = ex_settings
        self.model_settings = model_settings
        self.experiment_dir = experiment_dir

    def write_configs(self, trial: Trial) -> None:
        config = get_config()
        pass

    def run_model(self, trial: Trial):

        trial_dir = make_trial_dir(self.experiment_dir, trial.index)

        config_dir = write_configs(trial_dir, trial.arm.parameters, self.model_settings)

        model_dir = self.ex_settings["model_dir"]

        # with cd_and_cd_back(model_dir):
        os.chdir(model_dir)

        cmd = (f"python main.py --config_path {config_dir} --data_path"
               f" {self.ex_settings['data_path']} --output_path {trial_dir}")

        args = cmd.split()
        popen = subprocess.Popen(
            args, stdout=subprocess.PIPE, universal_newlines=True
        )
        self._processes.append(popen)

    def set_trial_status(self, trial: Trial) -> None:
        """ "Get status of the job by a given ID. For simplicity of the example,
        return an Ax `TrialStatus`.
        """
        log_file = get_trial_dir(self.experiment_dir, trial.index) / "fetch3.log"

        if log_file.exists():
            with open(log_file, "r") as f:
                contents = f.read()
            if "Error completing Run! Reason:" in contents:
                trial.mark_failed()
            elif "run complete" in contents:
                trial.mark_completed()

    def fetch_trial_data(self, trial: Trial, *args, **kwargs):

        modelfile = (
            get_trial_dir(self.experiment_dir, trial.index) / self.ex_settings["output_fname"]
        )

        y_pred, y_true = get_model_obs(
            modelfile,
            self.ex_settings["obsfile"],
            self.ex_settings,
            self.model_settings,
            trial.arm.parameters,
        )
        return dict(y_pred=y_pred, y_true=y_true)


def exit_handler():
    for process in Fetch3Wrapper._processes:
        process.kill()

atexit.register(exit_handler)