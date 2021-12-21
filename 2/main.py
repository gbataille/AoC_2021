from pathlib import Path
from typing import Optional

from utils import aoc_input

TEST_DATA = """forward 5
down 5
forward 8
up 3
down 8
forward 2"""


def main_part_1(input_file: Optional[Path]) -> None:
    input_data = TEST_DATA
    if input_file is not None:
        input_data = input_file.read_text()

    position = 0
    depth = 0
    for line in input_data.strip().split('\n'):
        direction, amount = line.split(' ')
        if direction == 'forward':
            position += int(amount)
        elif direction == 'up':
            depth -= int(amount)
        elif direction == 'down':
            depth += int(amount)
        else:
            raise ValueError('bad parse')

    print(depth, position)
    print(depth * position)


def main_part_2(input_file: Optional[Path] = None) -> None:
    input_data = TEST_DATA
    if input_file:
        input_data = input_file.read_text()

    aim = 0
    position = 0
    depth = 0
    for line in input_data.strip().split('\n'):
        direction, amount = line.split(' ')
        if direction == 'forward':
            position += int(amount)
            depth += aim * int(amount)
        elif direction == 'up':
            aim -= int(amount)
        elif direction == 'down':
            aim += int(amount)
        else:
            raise ValueError('bad parse')

    print(depth, position)
    print(depth * position)


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
