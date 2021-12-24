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

    for x, y, v in heightmap.step_through():
        neighbours = list(map(lambda j: j[2], heightmap.neighbours(x, y)))
        if v < min(neighbours):
            low_points.append(geo.Point2D(x, y))
            out += 1 + v

    print(out)


def main_part_2(input_file: Optional[Path] = None) -> None:
    input_data = TEST_DATA
    if input_file:
        input_data = input_file.read_text()

    heightmap = geo.Array2D[int].from_string(input_data, int)
    low_points: List[geo.Point2D] = []

    for x, y, v in heightmap.step_through():
        neighbours = list(map(lambda j: j[2], heightmap.neighbours(x, y)))
        if v < min(neighbours):
            low_points.append(geo.Point2D(x, y))

    def extend_basin(basin: Set[geo.Point2D]):
        len_in = len(basin)
        addtl_points: List[Tuple[int, int, int]] = []
        for point in basin:
            addtl_points += list(heightmap.neighbours(point.x, point.y))
        basin = basin | set(map(lambda j: geo.Point2D(j[0], j[1]), filter(lambda x: x[2] != 9, addtl_points)))
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
