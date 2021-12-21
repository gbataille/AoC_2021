from copy import deepcopy
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional

from utils import aoc_input

TEST_DATA = """0,9 -> 5,9
8,0 -> 0,8
9,4 -> 3,4
2,2 -> 2,1
7,0 -> 7,4
6,4 -> 2,0
0,9 -> 2,9
3,4 -> 1,4
0,0 -> 8,8
5,5 -> 8,2"""


@dataclass
class Point:
    x: int
    y: int

    @staticmethod
    def from_str(string: str) -> 'Point':
        x_str, y_str = string.strip().split(',')
        return Point(int(x_str), int(y_str))


@dataclass
class Line:
    start: Point
    end: Point

    def is_horizontal(self) -> bool:
        return self.start.y == self.end.y

    def is_vertical(self) -> bool:
        return self.start.x == self.end.x

    @staticmethod
    def from_str(string: str) -> 'Line':
        start_str, _, end_str = string.strip().split(' ')
        return Line(Point.from_str(start_str), Point.from_str(end_str))


@dataclass
class MapLine:
    cells: List[List[int]]

    @staticmethod
    def with_size(size_x: int, size_y: int) -> 'MapLine':
        line = [0] * (size_x + 1)
        cells = [deepcopy(line) for _ in range(size_y + 1)]
        return MapLine(cells)

    def mark_line(self, line: Line) -> 'MapLine':
        if line.is_vertical():
            if line.start.y < line.end.y:
                start = line.start.y
                end = line.end.y
            else:
                start = line.end.y
                end = line.start.y
            for y in range(start, end + 1):
                self.cells[y][line.start.x] = self.cells[y][line.start.x] + 1
        elif line.is_horizontal():
            if line.start.x < line.end.x:
                start = line.start.x
                end = line.end.x
            else:
                start = line.end.x
                end = line.start.x
            for x in range(start, end + 1):
                self.cells[line.start.y][x] = self.cells[line.start.y][x] + 1
        else:
            len_line = abs(line.end.x - line.start.x) + 1
            step_x = 1 if line.end.x > line.start.x else -1
            step_y = 1 if line.end.y > line.start.y else -1
            for i in range(len_line):
                self.cells[line.start.y + i * step_y][line.start.x + i * step_x] += 1

        return self

    def to_str(self) -> 'str':
        out = ''
        for line in self.cells:
            out = out + ' '.join(map(str, line)) + '\n'

        out.replace('0', '.')
        return out


def main_part_1(input_file: Optional[Path]) -> None:
    input_data = TEST_DATA
    if input_file is not None:
        input_data = input_file.read_text()

    lines = []
    for line_str in input_data.strip().split('\n'):
        lines.append(Line.from_str(line_str))

    max_x = 0
    for line in lines:
        if line.end.x > max_x:
            max_x = line.end.x
        if line.start.x > max_x:
            max_x = line.start.x

    max_y = 0
    for line in lines:
        if line.end.y > max_y:
            max_y = line.end.y
        if line.start.y > max_y:
            max_y = line.start.y

    map_line = MapLine.with_size(max_x, max_y)
    for line in lines:
        map_line.mark_line(line)

    cnt = 0
    for line in map_line.cells:
        for cell in line:
            if cell >= 2:
                cnt += 1

    print(cnt)


def main_part_2(input_file: Optional[Path] = None) -> None:
    main_part_1(input_file)


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
