from abc import ABC, abstractmethod

import numpy as np


class BaseDomainArea(ABC):
    matrix: np.ndarray

    def __str__(self) -> str:
        string = ""
        for row in self.matrix:
            string += f'{" ".join(str(int(pixel)) for pixel in row)}\n'
        return string

    @abstractmethod
    def get_matrix(self) -> np.ndarray:
        """Get the numpy matrix representation of the domain area"""


class House(BaseDomainArea):
    def __init__(self, x: int, y: int, z: int) -> None:
        self.x = round(x)
        self.y = round(y)
        self.z = z
        self.matrix = self.get_matrix()

    def get_matrix(self) -> np.ndarray:
        house = self.z * np.ones((self.y, self.x))
        return house


class Cell(BaseDomainArea):
    def __init__(self, house: House, x: int, y: int) -> None:
        self.house = house
        self._validate_matrix_size(x, "x")
        self._validate_matrix_size(y, "y")
        self.x = x
        self.y = y
        self.matrix = self.get_matrix()

    def get_matrix(self) -> np.ndarray:
        left = (self.x - self.house.x) // 2
        top = (self.y - self.house.y) // 2
        plot =  np.zeros((self.y, self.x))
        plot[top:top + self.house.y, left:left + self.house.x] = self.house.matrix
        
        return plot

    def _validate_matrix_size(self, value: int, house_edge_attr: str):
        if value < getattr(self.house, house_edge_attr):
            raise ValueError(f"The {house_edge_attr} value of HousePlot must be larger than the house going on it!")


class Domain(BaseDomainArea):
    def __init__(self, cell: Cell, x: int, y: int) -> None:
        self.cell = cell
        self.x = x
        self.y = y
        self.matrix = self.get_matrix()

    def get_matrix(self) -> np.ndarray:
        domain = np.tile(self.cell.matrix, (self.y // self.cell.matrix.shape[0], self.x // self.cell.matrix.shape[1]))
        return domain

    @classmethod
    def from_domain_config(cls, house, config, consts):
        cell = Cell(house, **config["plot_size"])
        x = consts["domain"]["x"]
        y = consts["domain"]["y"]
        return cls(cell=cell, x=x, y=y)
