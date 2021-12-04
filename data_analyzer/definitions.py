import numpy as np
from pathlib import Path

raw_data_path = (Path.cwd().parent / "Hom" / "LAI3" / "PALM Files" / "20211201T2039_3d.001.nc").resolve()
raw_data_path2 = (Path.cwd().parent / "Hom" / "LAI3" / "PALM Files" / "new_job_3d.003.nc").resolve()
raw_data_path3 = (Path.cwd().parent / "Hom" / "LAI3" / "PALM Files" / "20211202T181145_3d.nc").resolve()
s0_path = (Path.cwd().parent / "Processed_s0" / "DS0__LAI3.mat").resolve()
baled_output_path = (Path.cwd().parent / 'Hom/LAI3/BaledOutput/').resolve()

JOB = "20211203T133212"

BASE_DATA_PATH = (Path.cwd().parent / "Hom/LAI3/PALM Files").resolve()
JOB_PATH = BASE_DATA_PATH / JOB
DATA_PATH = JOB_PATH / f"OUTPUT/{JOB}_3d.nc"
CONFIG_PATH = JOB_PATH / "wrapper_config"
CANOPY_CSV = CONFIG_PATH / "canopy.csv"
CELL_CSV = CONFIG_PATH / "cell.csv"
HOUSE_CSV = CONFIG_PATH / "house.csv"
TOPO_CSV = CONFIG_PATH / "topo.csv"
CONFIG = CONFIG_PATH / "wrapper_config.json"

z_delta_s0_values = np.array([0, 1, 2, 3, 4, 5])

time_slice = 0
z_slice = 1
y_slice = 2
x_slice = 3