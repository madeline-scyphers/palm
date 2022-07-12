import copy
import datetime as dt
import subprocess
import json
from pathlib import Path

import numpy as np
import yaml
from ax import Trial
from boa import BaseWrapper, load_yaml


# TODO remove when added to boa
def get_dt_now_as_str(fmt: str = "%Y%m%dT%H%M%S"):
    return dt.datetime.now().strftime(fmt)


class Wrapper(BaseWrapper):
    def __init__(self, config):
        self.config = config

        self.model_settings = self.config["model_options"]
        self.ex_settings = self.config["optimization_options"]

        self.wrapper_config = None

    def write_configs(self, trial: Trial) -> None:
        cwd = Path.cwd()
        job_name = get_dt_now_as_str()
        wrapper_config_dir = cwd / "output" / job_name / "wrapper_config.yaml"

        wrapper_config = copy.deepcopy(self.config)
        wrapper_config["parameters"] = trial.arm.parameters
        wrapper_config["model_options"]["job_name"] = job_name

        with open(wrapper_config_dir, 'w') as f:
            yaml.dump(wrapper_config, f)

        trial.update_run_metadata(dict(wrapper_config_dir=wrapper_config_dir))

    def run_model(self, trial: Trial):
        wrapper_config = self._load_wrapper_config(trial)

        job_name = wrapper_config["model_options"]["job_name"]
        run_time = wrapper_config["model_options"]["output_end_time"] * wrapper_config["model_options"]["walltime_scalar"]
        io_config = wrapper_config["model_options"]["io_config"]
        to_batch = False

        cmd = f"bash slurm_job.sh {self.wrapper_config} {job_name} {run_time} {io_config} {to_batch}"

        args = cmd.split()
        subprocess.Popen(
            args, stdout=subprocess.PIPE, universal_newlines=True
        )

    def set_trial_status(self, trial: Trial) -> None:
        """Get status of the job by a given ID. For simplicity of the example,
        return an Ax `TrialStatus`.
        """
        wrapper_config = self._load_wrapper_config(trial)

        job_name = wrapper_config["model_options"]["job_name"]
        model_dir = wrapper_config["model_options"]["model_dir"]

        log_file = Path(model_dir) / job_name / "Logs" / f"{job_name}.log"

        if log_file.exists():
            with open(log_file, "r") as f:
                contents = f.read()
            if "palmrun crashed" in contents:
                trial.mark_abandoned()
            elif "error:" in contents:
                trial.mark_failed()
            if "all OUTPUT-files saved" in contents:
                trial.mark_completed()

    def fetch_trial_data(self, trial: Trial, *args, **kwargs):
        job_saving_dir = Path(trial.run_metadata["wrapper_config_dir"]).parent
        data_filepath = job_saving_dir / "output" / "r_ca.json"

        with open(data_filepath, 'r') as f:
            data = json.load(f)
        r_ca = np.array(data["1"])
        return dict(a=r_ca)

    @staticmethod
    def _load_wrapper_config(trial: Trial):
        wrapper_config_dir = trial.run_metadata["wrapper_config_dir"]
        wrapper_config = load_yaml(wrapper_config_dir, normalize=False)
        return wrapper_config
