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


T = TypeVar('T')


@dataclass
class Array2D(Generic[T]):
    cells: List[List[T]]
    height: int
    width: int

    def __init__(
        self,
        cells: List[List[T]],
    ):
        self.cells = cells
        self.width = len(cells[0])
        self.height = len(cells)

    def get_at(self, x: int, y: int) -> T:
        return self.cells[y][x]

    def insert_at(self, x: int, y: int, value: T) -> 'Array2D':
        if x > self.width or x < 0:
            raise IndexError(f'x {x} is outside the array boundaries')
        if y > self.height or y < 0:
            raise IndexError(f'y {y} is outside the array boundaries')

        self.cells[y][x] = value
        return self

    def insert_at_point(self, p: Point2D, value: T) -> 'Array2D':
        return self.insert_at(p.x, p.y, value)

    def step_through(self, horizontally: bool = True) -> Generator[Tuple[int, int, T], None, None]:
        if horizontally:
            for y in range(self.height):
                for x in range(self.width):
                    yield (x, y, self.cells[y][x])
        else:
            for x in range(self.width):
                for y in range(self.height):
                    yield (x, y, self.get_at(x, y))

    def neighbours(self, x: int, y: int, include_diags: bool = False) -> Generator[Tuple[int, int, T], None, None]:
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

                yield (x + dx, y + dy, self.get_at(x + dx, y + dy))

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
                line_str += elem_separator + elem_to_str(elem)

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
