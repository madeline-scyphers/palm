from domain import Domain, House, Cell
from load_config import config
from generate_canopy import copy_netcdf
from utils import factors, get_factors_rev

house_fraction_denominator = config["house"]["domain_fraction"]

factors = get_factors_rev(house_fraction_denominator)
x_factor = next(factors)
y_factor = next(factors)

plot_size = config["plot_size"]

house = House(plot_size["x"] / x_factor, plot_size["y"] / y_factor, config["house"]["height"])

# cell = Cell(house, **plot_size)

domain = Domain.from_domain_config(house, config)

# print(domain.print_tree_matrix())

with open("input", "w") as f:
    f.write(str(domain))
    
with open("tree.txt", "w") as f:
    f.write(domain.print_tree_matrix())

copy_netcdf(job_name=config["job_name"], tree_matrix=domain.trees_matrix)

# with open("tree_matrix.txt", "w") as f:
    # f.write(domain.print_tree_matrix())

