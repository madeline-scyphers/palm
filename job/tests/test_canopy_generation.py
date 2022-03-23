import numpy as np
from hypothesis import HealthCheck, assume, given, settings
from hypothesis import strategies as st

from job.run import setup_domain
from job.utils import get_factors_rev

DOMAIN_X = 96
DOMAIN_Y = 216


def get_config(domain_fraction, plot_size_x, plot_size_y):
    config = {
        "domain": {"x": DOMAIN_X, "y": DOMAIN_Y, "z": 5},
        "house": {"domain_fraction": domain_fraction, "height": 4},
        "plot_size": {"x": plot_size_x, "y": plot_size_y},
        "trees": {"domain_fraction": 8},
    }
    return config


@given(
    domain_fraction_pt1=st.integers().filter(lambda x: x % 2 == 0 and x % 3 != 0 and 2 <= x <= DOMAIN_X),
    domain_fraction_pt2=st.integers().filter(lambda y: y % 2 == 0 and y % 3 != 0 and 2 <= y <= DOMAIN_Y),
    plot_size_x=st.integers().filter(lambda x: DOMAIN_X % x == 0 and x % 2 == 0 and x % 3 != 0 and 4 <= x <= DOMAIN_X),
    plot_size_y=st.integers().filter(lambda y: DOMAIN_Y % y == 0 and y % 2 == 0 and y % 3 != 0 and 4 <= y <= DOMAIN_Y),
)
@settings(max_examples=1000, suppress_health_check=[HealthCheck.filter_too_much])
def test(domain_fraction_pt1, domain_fraction_pt2, plot_size_x, plot_size_y):
    domain_fraction = domain_fraction_pt1 * domain_fraction_pt2
    config = get_config(domain_fraction=domain_fraction, plot_size_x=plot_size_x, plot_size_y=plot_size_y)

    domain = setup_domain(config)

    assert domain.matrix.shape == (DOMAIN_Y, DOMAIN_X)
    assert np.count_nonzero(domain.matrix) == (DOMAIN_Y * DOMAIN_X) / domain_fraction
