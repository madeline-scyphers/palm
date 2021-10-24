from abc import ABC, abstractmethod
from typing import Optional

import numpy as np


class BaseDomainArea(ABC):
    subplot: Optional["BaseDomainArea"]
    x: int
    y: int
    y: Optional[int]
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


class House(BaseDomainArea):
    def __init__(self, x: int, y: int, z: int) -> None:
        self.x = round(x)
        self.y = round(y)
        self.z = z
        self.matrix = self.get_matrix()

    def get_matrix(self) -> np.ndarray:
        house = self.z * np.full((self.y, self.x), self.z)
        return house


class Cell(BaseDomainArea):
    def __init__(self, subplot: House, x: int, y: int) -> None:
        self.subplot = subplot
        self.x = x
        self.y = y
        self._validate_matrix_size(subplot=self.subplot)
        self.matrix = self.get_matrix()

    def get_matrix(self) -> np.ndarray:
        left = (self.x - self.subplot.x) // 2
        top = (self.y - self.subplot.y) // 2
        plot =  np.zeros((self.y, self.x))
        plot[top:top + self.subplot.y, left:left + self.subplot.x] = self.subplot.matrix
        
        return plot

class Domain(BaseDomainArea):
    def __init__(self, subplot: Cell, x: int, y: int) -> None:
        self.subplot = subplot
        self.x = x
        self.y = y
        self._validate_matrix_size(subplot=self.subplot)
        self.matrix = self.get_matrix()

    def get_matrix(self) -> np.ndarray:
        domain = np.tile(self.subplot.matrix, (self.y // self.subplot.matrix.shape[0], self.x // self.subplot.matrix.shape[1]))
        return domain

    @classmethod
    def from_domain_config(cls, house, config, consts):
        cell = Cell(house, **config["plot_size"])
        x = consts["domain"]["x"]
        y = consts["domain"]["y"]
        return cls(subplot=cell, x=x, y=y)
