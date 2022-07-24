import copy
import datetime as dt
import logging
import os
import subprocess
import json
from pathlib import Path
import traceback
from string import Template

import jinja2
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
    def __init__(self):
        self.config = None
        self.model_settings = None
        self.ex_settings = None
        self.experiment_dir = None

    def load_config(self, config_file: os.PathLike):
        """
        Load config file and return a dictionary # TODO finish this

        Parameters
        ----------
        config_file : os.PathLike
            File path for the experiment configuration file

        Returns
        -------
        loaded_config: dict
        """
        config = load_yaml(config_file)
        experiment_name = get_dt_now_as_str()
        config["optimization_options"]["experiment"]["name"] = experiment_name

        self.config = config
        self.model_settings = self.config["model_options"]
        self.ex_settings = self.config["optimization_options"]
        self.experiment_dir = Path(self.model_settings["optimization_output_dir"]).expanduser() / experiment_name
        self.experiment_dir.mkdir()
        return self.config

    def write_configs(self, trial: Trial) -> None:
        """
        This function is usually used to write out the configurations files used
        in an individual optimization trial run, or to dynamically write a run
        script to start an optimization trial run.

        Parameters
        ----------
        trial : BaseTrial
        """
        try:
            trial_config = copy.deepcopy(self.config)
            job_name = zfilled_trial_index(trial.index)
            job_output_dir = self.experiment_dir / job_name
            job_output_dir.mkdir(parents=True)

            run_time = trial_config["model_options"]["output_end_time"] * trial_config["model_options"][
                "palmrun_walltime_scalar"]
            data_analyses_time = (
                    (trial_config["model_options"]["output_end_time"] - trial_config["model_options"][
                        "output_start_time"])
                    * trial_config["model_options"]["data_analyse_walltime_scalar"])
            trial_config_path = job_output_dir / "trial_config.yaml"
            job_script_path = (job_output_dir / "slurm_job.sh").resolve()

            trial_config["parameters"] = trial.arm.parameters
            trial_config["model_options"]["config_path"] = str(trial_config_path)
            trial_config["model_options"]["job_script_path"] = str(job_script_path)
            trial_config["model_options"]["job_name"] = job_name
            trial_config["model_options"]["log_file"] = str(job_output_dir / f"{job_name}_%j.log")
            trial_config["model_options"]["job_output_dir"] = str(job_output_dir)
            trial_config["model_options"]["run_time"] = int(run_time)
            trial_config["model_options"]["data_analyses_time"] = data_analyses_time
            trial_config["model_options"]["batch_time"] = int(run_time + data_analyses_time)

            trial.update_run_metadata(
                dict(trial_config_path=trial_config_path,
                    job_script_path=job_script_path))

            with open(JOB_SCRIPT_PATH) as template:
                job_script = template.read()
            jinja_env = jinja2.Environment(
                loader=jinja2.BaseLoader(),
            )
            template = jinja_env.from_string(job_script)
            job_script = template.render(**trial_config["model_options"])
            # job_script = job_script.format(**trial_config["model_options"])

            with open(job_script_path, "w") as f:
                f.write(job_script)

            with open(trial_config_path, 'w') as f:
                yaml.dump(trial_config, f)
        except Exception as e:
            from pprint import pprint
            pprint(trial_config["model_options"])
            logging.exception(e)
            logging.exception(traceback.format_exc())
            print()
            print()
            print()
            raise

    def run_model(self, trial: Trial):
        """
        Runs a model by deploying a given trial.

        Parameters
        ----------
        trial : BaseTrial
        """
        try:
            trial_config = self._load_trial_config(trial)

            job_script_path = trial_config["model_options"]["job_script_path"]
            cmd = f"sbatch {job_script_path}"

            args = cmd.split()
            subprocess.Popen(
                args, stdout=subprocess.PIPE, universal_newlines=True
            )
        except Exception as e:
            logging.exception(e)
            logging.exception(traceback.format_exc())
            print()
            print()
            print()

    def set_trial_status(self, trial: Trial) -> None:
        """
        The trial gets polled from time to time to see if it is completed, failed, still running,
        etc. This marks the trial as one of those options based on some criteria of the model.
        If the model is still running, don't do anything with the trial.

        Parameters
        ----------
        trial : BaseTrial

        Examples
        --------
        trial.mark_completed()
        trial.mark_failed()
        trial.mark_abandoned()
        trial.mark_early_stopped()

        See Also
        --------
        # TODO add sphinx link to ax trial status

        """
        trial_config = self._load_trial_config(trial)

        log_file = Path(trial_config["model_options"]["log_file"])

        if log_file.exists():
            with open(log_file, "r") as f:
                contents = f.read()
            if "palmrun crashed" in contents:
                trial.mark_abandoned()
            elif "error:" in contents:
                trial.mark_failed()
            if "all OUTPUT-files saved" in contents:
                trial.mark_completed()

    def fetch_trial_data(self, trial: Trial, metric_properties: dict, metric_name: str,  *args, **kwargs):
        """
        Retrieves the trial data and prepares it for the metric(s) used in the objective
        function.

        For example, for a case where you are minimizing the error between a model and observations, using RMSE as a
        metric, this function would load the model output and the corresponding observation data that will be passed to
        the RMSE metric.

        The return value of this function is a dictionary, with keys that match the keys
        of the metric used in the objective function.
        # TODO work on this description

        Parameters
        ----------
        trial : Trial
        metric_properties: dict
        metric_name: str

        Returns
        -------
        dict
            A dictionary with the keys matching the keys of the metric function
                used in the objective
        """
        trial_config = trial.run_metadata["trial_config_path"]
        job_output_dir = trial_config["model_options"]["job_output_dir"]
        data_filepath = job_output_dir / "r_ca.json"

        with open(data_filepath, 'r') as f:
            data = json.load(f)
        r_ca = np.array(data["r_ca"])
        return dict(a=r_ca)

    @staticmethod
    def _load_trial_config(trial: Trial):
        trial_config_path = trial.run_metadata["trial_config_path"]
        trial_config = load_yaml(trial_config_path, normalize=False)
        return trial_config
