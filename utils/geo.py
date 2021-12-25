from copy import deepcopy
from dataclasses import dataclass
from typing import Callable, Generator, Generic, List, Optional, Tuple, TypeVar


@dataclass
class Point2D:
    x: int
    y: int

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Point2D):
            return False
        return self.x == other.x and self.y == other.y

    def __hash__(self) -> int:
        return hash((self.x, self.y))


C = TypeVar('C')
T = TypeVar('T')


@dataclass
class Cell(Generic[C, T]):
    coordinates: C
    value: T


@dataclass
class Array2D(Generic[T]):
    cells: List[List[Cell[Point2D, T]]]
    height: int
    width: int

    def __init__(
        self,
        cells: List[List[T]],
    ):
        self.cells = [[Cell(Point2D(cell_idx, line_idx), cell_value) for cell_idx, cell_value in enumerate(line)]
                      for line_idx, line in enumerate(cells)]
        self.width = len(cells[0])
        self.height = len(cells)

    def __iter__(self) -> Generator[Cell[Point2D, T], None, None]:
        return self.step_through()

    def get_value_at(self, x: int, y: int) -> T:
        return self.get_cell_at(x, y).value

    def get_cell_at(self, x: int, y: int) -> Cell[Point2D, T]:
        return self.cells[y][x]

    def set_value_at(self, x: int, y: int, value: T) -> 'Array2D':
        if x > self.width or x < 0:
            raise IndexError(f'x {x} is outside the array boundaries')
        if y > self.height or y < 0:
            raise IndexError(f'y {y} is outside the array boundaries')

        return self.set_cell(Cell(Point2D(x, y), value))

    def set_value_at_point(self, p: Point2D, value: T) -> 'Array2D':
        return self.set_cell(Cell(p, value))

    def set_cell(self, cell: Cell[Point2D, T]) -> 'Array2D':
        self.cells[cell.coordinates.y][cell.coordinates.x] = cell
        return self

    def step_through(self, horizontally: bool = True) -> Generator[Cell[Point2D, T], None, None]:
        if horizontally:
            for y in range(self.height):
                for x in range(self.width):
                    yield self.get_cell_at(x, y)
        else:
            for x in range(self.width):
                for y in range(self.height):
                    yield self.get_cell_at(x, y)

    def neighbours(self, x: int, y: int, include_diags: bool = False) -> Generator[Cell[Point2D, T], None, None]:
        for dx in range(-1, 2):
            for dy in range(-1, 2):
                # skip diag
                if not include_diags and dx != 0 and dy != 0:
                    continue

                # skip self
                if dx == 0 and dy == 0:
                    continue

                # Handle borders
                if not 0 <= x + dx < self.width:
                    continue
                if not 0 <= y + dy < self.height:
                    continue

                yield self.get_cell_at(x + dx, y + dy)

    @staticmethod
    def from_string(
        input_str: str,
        str_elem_to_T_elem: Callable[[str], T],
        line_separator: str = '\n',
        elem_separator: Optional[str] = None,
    ) -> 'Array2D[T]':
        cells: List[List[T]] = []
        for line_str in input_str.strip().split(line_separator):
            line = []

            line_list = []
            if elem_separator:
                line_list = line_str.strip().split(elem_separator)
            else:
                line_list = list(line_str.strip())

            for elem in line_list:
                line.append(str_elem_to_T_elem(elem))

            cells.append(line)

        return Array2D(cells)

    def to_string(
        self,
        elem_to_str: Callable[[T], str] = str,
        line_separator: str = '\n',
        elem_separator: str = '',
    ):
        out = ''
        for line in self.cells:
            line_str = ''
            for elem in line:
                line_str += elem_separator + elem_to_str(elem.value)

            if elem_separator != '':
                line_str = line_str[1:]

            out += line_str + line_separator

        return out

    @staticmethod
    def empty(width: int, height: int, elem: T) -> 'Array2D':
        cells = []

        line = []
        for _ in range(width):
            line.append(elem)

        for _ in range(height):
            cells.append(deepcopy(line))

        return Array2D(cells)
