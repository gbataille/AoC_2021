from pathlib import Path

from utils import aoc_input


def main_part_1(input_file: Path) -> None:
    input_data = input_file.read_text()


def main_part_2(input_file: Path) -> None:
    input_data = input_file.read_text()

    cnt = 0
    lines = list(map(int, input_data.strip().split('\n')))
    for idx in range(len(lines) - 3):
        after = lines[idx + 3]
        before = lines[idx]
        if after > before:
            cnt += 1

    print(cnt)


def main(day_num: int, part_num: int) -> None:
    if part_num == 1:
        input_file = aoc_input.get_input(day_num, part_num)
        main_part_1(input_file)
    elif part_num == 2:
        input_file = aoc_input.get_input(day_num, part_num)
        main_part_2(input_file)
    else:
        raise ValueError(f"Invalid part number {part_num}")
