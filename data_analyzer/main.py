from domain import Domain, House, Cell
from load_config import config, consts
# from houses import House, Cell
from utils import factors, get_factors_rev

house_fraction_denomanator = consts["house"]["fraction_denomanator"]

factors = get_factors_rev(house_fraction_denomanator)
x = next(factors)
y = next(factors)

plot_size = config["plot_size"]

house = House(plot_size["x"] / x, plot_size["y"] / y, consts["house"]["height"])

cell = Cell(house, **plot_size)

domain = Domain.from_domain_config(house, config, consts)

with open("input", "w") as f:
    f.write(str(domain))
