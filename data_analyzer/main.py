from domain import Domain, House, Cell
from load_config import config, consts
# from houses import House, Cell
from utils import factors

house_fraction_denomanator = consts["house"]["fraction_denomanator"]

primes_ls = factors(house_fraction_denomanator)

plot_size = config["plot_size"]

house = House(plot_size["x"] / primes_ls[0], plot_size["y"] / primes_ls[1], consts["house"]["height"])

cell = Cell(house, **plot_size)

domain = Domain.from_domain_config(house, config, consts)

with open("input", "w") as f:
    f.write(str(domain))
