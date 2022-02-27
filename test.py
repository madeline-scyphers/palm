import sys
sys.path.append("canopy_generator")

import numpy as np

from canopy_generator.generate_canopy import generate_canopy
from canopy_generator.plotting import plot_generated_canopy


domain = np.array([
    [np.NAN, 1, 1, 1, np.NAN],
    [np.NAN, np.NAN, np.NAN, 1, 1],
    [np.NAN, np.NAN, np.NAN, 1, 1],
    [np.NAN, 1, 1, 1, 1],
    [np.NAN, np.NAN, np.NAN, 1, 1],
    [1, 1, 1, 1, 1],
    ])



plot_generated_canopy(domain)