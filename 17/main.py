from pathlib import Path

from utils import aoc_input


def main_part_1() -> None:
    input_data = input_file.read_text()


def main_part_2() -> None:
    input_data = input_file.read_text()


def main(day_num: int, part_num: int) -> None:
    if part_num == 1:
        aoc_input.get_input(day_num, part_num)
        main_part_1()
    elif part_num == 2:
        aoc_input.get_input(day_num, part_num)
        main_part_2()
    else:
        raise ValueError(f"Invalid part number {part_num}")