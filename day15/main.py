from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional, Set

from utils import aoc_input, geo
from utils.out import debug

TEST_DATA = """1163751742
1381373672
2136511328
3694931569
7463417111
1319128137
1359912421
3125421639
1293138521
2311944581"""


@dataclass
class SubmarinePath:
    cells: List[geo.Cell[geo.Point2D, int]] = field(default_factory=list)
    seen: Set[geo.Cell[geo.Point2D, int]] = field(default_factory=set)
    weight: int = 0
    is_done: bool = False


@dataclass
class Solver:
    chitons: geo.Array2D[int]
    min_map: geo.Array2D[int]
    paths: List[SubmarinePath]
    done_path: Optional[SubmarinePath] = None

    def move1(self) -> 'Solver':
        new_paths: List['SubmarinePath'] = []
        for path in self.paths:
            last_cell = path.cells[-1]
            for cell in self.chitons.neighbours(last_cell.coordinates.x, last_cell.coordinates.y):
                is_last_cell = (cell.coordinates.x == self.chitons.width - 1
                                and cell.coordinates.y == self.chitons.height - 1)
                new_weight = path.weight + cell.value
                new_path = SubmarinePath(
                    cells=list(path.cells) + [cell],
                    seen=path.seen | set([cell]),
                    weight=new_weight,
                    is_done=is_last_cell,
                )
                if cell not in path.seen:
                    if is_last_cell:
                        if self.done_path is None or new_weight < self.done_path.weight:
                            self.done_path = new_path
                    else:
                        min_for_cell = self.min_map.get_cell_at(cell.coordinates.x, cell.coordinates.y)
                        if min_for_cell.value == -1 or min_for_cell.value > new_weight:
                            min_for_cell.value = new_weight
                            new_paths.append(new_path)

        self.paths = new_paths

        return self


def main_part_1(input_file: Optional[Path]) -> None:
    input_data = TEST_DATA
    if input_file is not None:
        input_data = input_file.read_text()

    chitons: geo.Array2D[int] = geo.Array2D.from_string(input_data, int)
    min_map: geo.Array2D[int] = geo.Array2D.empty(chitons.width, chitons.height, -1)
    start = chitons.get_cell_at(0, 0)
    paths: List[SubmarinePath] = [SubmarinePath(cells=[start], seen=set([start]))]

    solver = Solver(chitons, min_map, paths)
    while solver.paths:
        solver.move1()

    print(solver.done_path.weight)


def main_part_2(input_file: Optional[Path] = None) -> None:
    input_data = TEST_DATA
    if input_file:
        input_data = input_file.read_text()


def main(day_num: int, part_num: int, with_test_data=True) -> None:
    input_file = None
    if not with_test_data:
        input_file = aoc_input.get_input(day_num)

    if part_num == 1:
        main_part_1(input_file)
    elif part_num == 2:
        main_part_2(input_file)
    else:
        raise ValueError(f"Invalid part number 0part_num0")
