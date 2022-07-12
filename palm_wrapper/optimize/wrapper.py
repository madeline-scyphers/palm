import copy
import datetime as dt
import subprocess
import json
from pathlib import Path

import numpy as np
import yaml
from ax import Trial
from boa import BaseWrapper, load_yaml, get_trial_dir


# TODO remove when added to boa
def get_dt_now_as_str(fmt: str = "%Y%m%dT%H%M%S"):
    return dt.datetime.now().strftime(fmt)

# TODO remove when added to boa
def zfilled_trial_index(trial_index: int, fill_size: int = 6) -> str:
    """Return trial index left passed with zeros of length ``fill_size``"""
    return str(trial_index).zfill(fill_size)


JOB_SCRIPT_PATH = Path(__file__).resolve().parent / "batch_job_template.txt"


class Wrapper(BaseWrapper):
    def __init__(self, config):
        self.config = config

        self.model_settings = self.config["model_options"]
        self.ex_settings = self.config["optimization_options"]

        self.wrapper_config = None

    def write_configs(self, trial: Trial) -> None:
        wrapper_config = copy.deepcopy(self.config)
        job_name = zfilled_trial_index(trial.index)
        optimization_output_dir = Path(self.model_settings["optimization_output_dir"]).expanduser()
        experiment_name = self.ex_settings["experiment"]["name"]
        job_output_dir = optimization_output_dir / experiment_name / job_name
        job_output_dir.mkdir(parents=True)

        log_file = job_output_dir / f"{job_name}_%j.log"
        run_time = wrapper_config["model_options"]["output_end_time"] * wrapper_config["model_options"]["palmrun_walltime_scalar"]
        data_analyses_time = (
                (wrapper_config["model_options"]["output_end_time"] - wrapper_config["model_options"]["output_start_time"])
                * wrapper_config["model_options"]["data_analyse_walltime_scalar"])
        batch_time = run_time + data_analyses_time
        io_config = wrapper_config["model_options"]["io_config"]
        wrapper_config_path = job_output_dir / "wrapper_config.yaml"
        job_script_path = (job_output_dir / "slurm_job.sh").resolve()

        wrapper_config["parameters"] = trial.arm.parameters
        wrapper_config["model_options"]["config_path"] = wrapper_config_path
        wrapper_config["model_options"]["job_script_path"] = job_script_path
        wrapper_config["model_options"]["job_name"] = job_name
        wrapper_config["model_options"]["log_file"] = log_file
        wrapper_config["model_options"]["job_output_dir"] = job_output_dir
        wrapper_config["model_options"]["run_time"] = run_time
        wrapper_config["model_options"]["data_analyses_time"] = data_analyses_time
        wrapper_config["model_options"]["batch_time"] = batch_time
        wrapper_config["model_options"]["io_config"] = io_config

        with open(JOB_SCRIPT_PATH) as template:
            job_script = template.read()
        job_script.format(**wrapper_config["model_options"])

        with open(job_script_path, "w") as f:
            f.write(job_script)

        with open(wrapper_config_path, 'w') as f:
            yaml.dump(wrapper_config, f)
        trial.update_run_metadata(
            dict(wrapper_config_path=wrapper_config_path,
                 job_script_path=job_script_path))

    def run_model(self, trial: Trial):
        wrapper_config = self._load_wrapper_config(trial)

        job_script_path = wrapper_config["model_options"]["job_script_path"]
        cmd = f"sbatch {job_script_path}"

        args = cmd.split()
        subprocess.Popen(
            args, stdout=subprocess.PIPE, universal_newlines=True
        )

    def set_trial_status(self, trial: Trial) -> None:
        """Get status of the job by a given ID. For simplicity of the example,
        return an Ax `TrialStatus`.
        """
        wrapper_config = self._load_wrapper_config(trial)

        log_file = wrapper_config["model_options"]["log_file"]

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
        wrapper_config = trial.run_metadata["wrapper_config_path"]
        job_output_dir = wrapper_config["model_options"]["job_output_dir"]
        data_filepath = job_output_dir / "r_ca.json"

        with open(data_filepath, 'r') as f:
            data = json.load(f)
        r_ca = np.array(data["1"])
        return dict(a=r_ca)

    @staticmethod
    def _load_wrapper_config(trial: Trial):
        wrapper_config_path = trial.run_metadata["wrapper_config_path"]
        wrapper_config = load_yaml(wrapper_config_path, normalize=False)
        return wrapper_config
