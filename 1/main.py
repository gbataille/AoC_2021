from pathlib import Path
from typing import Optional

from utils import aoc_input

TEST_DATA = ""


def main_part_1(input_file: Optional[Path] = None) -> None:
    input_data = TEST_DATA
    if input_file:
        input_data = input_file.read_text()


def main_part_2(input_file: Optional[Path] = None) -> None:
    input_data = TEST_DATA
    if input_file:
        input_data = input_file.read_text()

    cnt = 0
    lines = list(map(int, input_data.strip().split('\n')))
    for idx in range(len(lines) - 3):
        after = lines[idx + 3]
        before = lines[idx]
        if after > before:
            cnt += 1

    print(cnt)


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
