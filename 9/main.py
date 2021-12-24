from pathlib import Path
from typing import List, Optional, Set, Tuple

from utils import aoc_input, geo
from utils.out import debug

TEST_DATA = """2199943210
3987894921
9856789892
8767896789
9899965678"""


def main_part_1(input_file: Optional[Path]) -> None:
    input_data = TEST_DATA
    if input_file is not None:
        input_data = input_file.read_text()

    heightmap = geo.Array2D[int].from_string(input_data, int)
    low_points: List[geo.Point2D] = []

    out = 0

    for cell in heightmap.step_through():
        neighbours = list(map(lambda j: j.value, heightmap.neighbours(cell.coordinates.x, cell.coordinates.y)))
        if cell.value < min(neighbours):
            low_points.append(cell.coordinates)
            out += 1 + cell.value

    print(out)


def main_part_2(input_file: Optional[Path] = None) -> None:
    input_data = TEST_DATA
    if input_file:
        input_data = input_file.read_text()

    heightmap = geo.Array2D[int].from_string(input_data, int)
    low_points: List[geo.Point2D] = []

    for cell in heightmap.step_through():
        neighbours = list(map(lambda j: j.value, heightmap.neighbours(cell.coordinates.x, cell.coordinates.y)))
        if cell.value < min(neighbours):
            low_points.append(cell.coordinates)

    def extend_basin(basin: Set[geo.Point2D]):
        len_in = len(basin)
        addtl_points: List[Tuple[int, int, int]] = []
        for point in basin:
            addtl_points += list(heightmap.neighbours(point.x, point.y))
        basin = basin | set(map(lambda j: j.coordinates, filter(lambda i: i.value != 9, addtl_points)))
        len_out = len(basin)
        if len_in == len_out:
            return basin

        return extend_basin(basin)

    basins: List[Set[int]] = []
    basins_sizes = []
    for point in low_points:
        basin = [point]
        basin = extend_basin(set(basin))
        basins.append(basin)
        basins_sizes.append(len(basin))

    basins_sizes.sort()
    print(basins_sizes[-1] * basins_sizes[-2] * basins_sizes[-3])


def main(day_num: int, part_num: int, with_test_data=True) -> None:
    input_file = None
    if not with_test_data:
        input_file = aoc_input.get_input(day_num, part_num)

    if part_num == 1:
        main_part_1(input_file)
    elif part_num == 2:
        main_part_2(input_file)
    else:
        raise ValueError(f"Invalid part number {part_num}")
