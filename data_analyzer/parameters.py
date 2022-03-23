from pathlib import Path

import numpy as np

BASE_DIR = Path(__file__).parent.parent.resolve()

raw_data_path = (Path.cwd().parent / "Hom" / "LAI3" / "PALM Files" / "20211201T2039_3d.001.nc").resolve()
raw_data_path2 = (Path.cwd().parent / "Hom" / "LAI3" / "PALM Files" / "new_job_3d.003.nc").resolve()
raw_data_path3 = (Path.cwd().parent / "Hom" / "LAI3" / "PALM Files" / "20211202T181145_3d.nc").resolve()
s0_path = (Path.cwd().parent / "Processed_s0" / "DS0__LAI3.mat").resolve()
baled_output_path = (Path.cwd().parent / "Hom/LAI3/BaledOutput/").resolve()

JOB = "20211203T133212"

JOB = "20211205T141223"

BASE_DIR = Path(__file__).parent.parent.resolve()

BASE_JOBS_DIR = BASE_DIR / "current_version" / "JOBS"
JOB_PATH = BASE_JOBS_DIR / JOB
DATA_PATH_3D = JOB_PATH / f"OUTPUT/{JOB}_3d.nc"
DATA_PATH_TS = JOB_PATH / f"OUTPUT/{JOB}_3d.nc"
DATA_PATH_XY = JOB_PATH / f"OUTPUT/{JOB}_xy.nc"
DATA_LAD = JOB_PATH / f"INPUT/{JOB}_static"
CONFIG_PATH = JOB_PATH / "wrapper_config"
CANOPY_CSV = CONFIG_PATH / "canopy.csv"
CELL_CSV = CONFIG_PATH / "cell.csv"
HOUSE_CSV = CONFIG_PATH / "house.csv"
TOPO_CSV = CONFIG_PATH / "topo.csv"
CONFIG = CONFIG_PATH / "wrapper_config.json"


def job_path(job):
    return BASE_JOBS_DIR / job


def data_path(job_path, job):
    return job_path / f"OUTPUT/{job}_3d.nc"


def lad_path(job_path, job):
    return job_path / f"INPUT/{job}_static"


def config_path(job_path):
    return job_path / "wrapper_config/wrapper_config.json"


def canopy_path(job_path):
    return job_path / "wrapper_config/canopy.csv"


z_delta_s0_values = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

time_slice = 0
z_slice = 1
y_slice = 2
x_slice = 3

DW = 12
dZ = 5
CANOPY_HEIGHT_UNITS = 9
