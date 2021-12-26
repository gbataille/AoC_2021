from pathlib import Path
from typing import List, Optional

from utils import aoc_input, geo
from utils.out import debug

TEST_DATA = """6,10
0,14
9,10
0,3
10,4
4,11
6,0
6,12
4,1
0,13
10,12
3,4
3,0
8,4
1,10
2,14
8,10
9,0

fold along y=7
fold along x=5"""


def main_part_1(input_file: Optional[Path]) -> None:
    input_data = TEST_DATA
    if input_file is not None:
        input_data = input_file.read_text()

    folds: List[str] = []
    points: List[geo.Point2D] = []
    max_x: int = 0
    max_y: int = 0
    for line in input_data.strip().split('\n'):
        if not line:
            continue
        elif line.startswith('fold'):
            folds.append(line[11:])
        else:
            x_str, y_str = line.strip().split(',')
            x = int(x_str)
            y = int(y_str)
            if x > max_x:
                max_x = x
            if y > max_y:
                max_y = y
            points.append(geo.Point2D(x, y))

    sheet: geo.Array2D[bool] = geo.Array2D.empty(max_x + 1, max_y + 1, False)
    for point in points:
        sheet.set_value_at_point(point, True)

    debug(sheet.to_string(lambda x: "#" if x else '.'))
    debug(folds)

    for fold in folds:
        direction, location = fold.split('=')
        location = int(location)
        if direction == 'y':
            new_sheet = geo.Array2D.empty(sheet.width, location, False)
        else:
            new_sheet = geo.Array2D.empty(location, sheet.height, False)

        for cell in new_sheet.step_through():
            mirror_x: int = 0
            mirror_y: int = 0
            if direction == 'y':
                mirror_x = cell.coordinates.x
                mirror_y = location + (location - cell.coordinates.y)
            else:
                mirror_x = location + (location - cell.coordinates.x)
                mirror_y = cell.coordinates.y

            mirror_cell: geo.Cell[geo.Point2D, bool]
            if mirror_x >= sheet.width or mirror_y >= sheet.height:
                mirror_cell = geo.Cell(geo.Point2D(-1, -1), False)
            else:
                mirror_cell = sheet.get_cell_at(mirror_x, mirror_y)

            cell.value = sheet.get_cell_at(cell.coordinates.x, cell.coordinates.y).value or mirror_cell.value

        debug('')
        debug(new_sheet.to_string(lambda x: "#" if x else '.'))

        sheet = new_sheet

    print(new_sheet.to_string(lambda x: "#" if x else '.'))


def main_part_2(input_file: Optional[Path] = None) -> None:
    input_data = TEST_DATA
    if input_file:
        input_data = input_file.read_text()


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
