from dataclasses import dataclass
from typing import Generic, List, TypeVar


@dataclass
class Point2D:
    x: int
    y: int


@dataclass
class Point3D:
    x: int
    y: int
    z: int


T = TypeVar('T')


@dataclass
class Array2D(Generic[T]):
    cells: List[List[T]]

    def get_at(self, x: int, y: int) -> T:
        return self.cells[y][x]

    def insert_at(self, x: int, y: int, value: T) -> 'Array2D':
        self.cells[y][x] = value
        return self
