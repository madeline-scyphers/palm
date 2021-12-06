from abc import ABC, abstractmethod
from typing import Optional
from math import floor, remainder

from utils import get_factors_rev

import numpy as np


class BaseDomainArea(ABC):
    subplot: Optional["BaseDomainArea"]
    x: int
    y: int
    z: Optional[int]
    matrix: np.ndarray

    def __str__(self) -> str:
        string = ""
        for row in self.matrix:
            string += f'{" ".join(str(int(pixel)) for pixel in row)}\n'
        return string

    @abstractmethod
    def get_matrix(self) -> np.ndarray:
        """Get the numpy matrix representation of the domain area"""

    def _validate_matrix_size(self, subplot):
        for value in ["x", "y"]:
            cell_val = getattr(self, value)
            subplot_val = getattr(subplot, value)
            if subplot_val and cell_val < subplot_val:
                raise ValueError(f"The {value} ({cell_val}) value of {self.__class__.__name__}"
                                 f" must be larger than the house ({subplot_val}) going on it!")
                
    def save_matrix(self, filename: str, matrix_name: str = None) -> None:
        matrix = self.matrix if matrix_name is None else getattr(self, matrix_name)
        np.savetxt(filename, matrix, delimiter=",")

class House(BaseDomainArea):
    def __init__(self, x: int, y: int, z: int) -> None:
        self.x = round(x)
        self.y = round(y)
        self.z = z
        self.matrix = self.get_matrix()

    def get_matrix(self) -> np.ndarray:
        house = np.full((self.y, self.x), self.z)
        return house


class Cell(BaseDomainArea):
    def __init__(self, subplot: House, x: int, y: int, tree_domain_fraction: int) -> None:
        self.subplot = subplot
        self.x = x
        self.y = y
        self.tree_domain_fraction = tree_domain_fraction
        self._validate_matrix_size(subplot=self.subplot)
        self.matrix = self.get_matrix()
        self.trees = self.get_trees()
        
        if np.max(self.matrix + self.trees) > np.max(self.matrix):
            raise TypeError("Invalid Configuration, Only valid configuration found when trees overlap with house matrix")

    def get_matrix(self) -> np.ndarray:
        left = (self.x - self.subplot.x) // 2
        top = (self.y - self.subplot.y) // 2
        plot =  np.zeros((self.y, self.x), dtype=int)
        plot[top:top + self.subplot.y, left:left + self.subplot.x] = self.subplot.matrix
        
        return plot
    
    def calc_perimeter(self, x: int, y: int):
        # offset = 4
        # inset_min, inset_max = x, self.matrix.shape[0] - x
        return 2 * x + 2 * y - 4

    def get_trees(self):
        no_of_trees = self.matrix.size // self.tree_domain_fraction if self.tree_domain_fraction is not None else 0
        perimeter = self.calc_perimeter(self.x, self.y)

        trees_fence = self.set_fence(no_of_trees)
        return trees_fence

    def set_fence(self, no_of_trees):
        a = np.zeros((self.y, self.x), dtype=int)
        
        for step in range(1, min(a.shape) // 2):
            a = self._set_fence(np.zeros((self.y, self.x), dtype=int), step)
            if a.sum() >= no_of_trees:
                break
        else:
            raise TypeError("Invalid number of trees")
        
        perimeter = a.sum()
        
        perim_locations = np.linspace(0, perimeter, num=no_of_trees, endpoint=False, dtype=int)
        perim_inds = np.where(a[a == 1])[0]
        a[a == 1] = np.where(np.isin(perim_inds, perim_locations), 1, 0)
        return a

    @staticmethod
    def _set_fence(a, step=0):
        a[((np.arange(0,step), np.arange(-step,0))),] = 1
        a[:,((np.arange(0,step), np.arange(-step,0)))] = 1
        return a

class Domain(BaseDomainArea):
    def __init__(self, subplot: Cell, x: int, y: int) -> None:
        self.subplot = subplot
        self.x = x
        self.y = y
        self._validate_matrix_size(subplot=self.subplot)
        self.matrix, self.trees_matrix = self.get_matrix()
    
    def print_tree_matrix(self) -> str:
        string = ""
        for row in self.trees_matrix: 
            string += f'{" ".join(str(int(pixel)) for pixel in row)}\n'
        return string

    def get_matrix(self) -> np.ndarray:
        domain = np.tile(self.subplot.matrix, 
                         (self.y // self.subplot.matrix.shape[0], self.x // self.subplot.matrix.shape[1]))
        domain_trees = np.tile(self.subplot.trees, 
                               (self.y // self.subplot.matrix.shape[0], self.x // self.subplot.matrix.shape[1]))
        
        return domain, domain_trees

    @classmethod
    def from_domain_config(cls, house, config):
        cell = Cell(house, tree_domain_fraction=config["trees"]["domain_fraction"], **config["plot_size"])
        x = config["domain"]["x"]
        y = config["domain"]["y"]
        return cls(subplot=cell, x=x, y=y)
    
def setup_domain(cfg):
    house_fraction_denominator = cfg["house"]["domain_fraction"]

    factors = get_factors_rev(house_fraction_denominator)
    x_factor = next(factors)
    y_factor = next(factors)

    plot_size = cfg["plot_size"]

    house = House(plot_size["x"] / x_factor, plot_size["y"] / y_factor, cfg["house"]["height"])

    return Domain.from_domain_config(house, cfg)


if __name__ == "__main__":
    from load_run_config import default_config
    config = default_config(
        house_domain_fraction=4,
        plot_size_x=96,
        plot_size_y=72,
        tree_domain_fraction=4
    )
    domain = setup_domain(config)
    print(domain.subplot.trees)