from pathlib import Path
from typing import Dict, Optional

from utils import aoc_input
from utils.out import debug

TEST_DATA = "3,4,3,1,2"

REPRODUCTION_RATE = 7
NEW_PENALTY = 2


def main_part_1(input_file: Optional[Path]) -> None:
    input_data = TEST_DATA
    if input_file is not None:
        input_data = input_file.read_text()

    fishes = list(map(int, input_data.strip().split(',')))
    for day in range(256):
        new_fishes = 0
        for fish_idx in range(len(fishes)):
            age = fishes[fish_idx]
            if age == 0:
                new_fishes += 1
                age = 6
            else:
                age -= 1
            fishes[fish_idx] = age
        fishes = fishes + [8] * new_fishes

    print(len(fishes))


def main_part_2(input_file: Optional[Path] = None) -> None:
    input_data = TEST_DATA
    if input_file is not None:
        input_data = input_file.read_text()

    fishes = list(map(int, input_data.strip().split(',')))

    generations: Dict[int, int] = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0}
    for fish in fishes:
        generations[fish] = generations[fish] + 1

    for day in range(256):
        for gen in range(9):
            generations[gen - 1] = generations[gen]
        generations[8] = generations[-1]
        generations[6] = generations[6] + generations[-1]
        del generations[-1]

    population = 0
    for val in generations.values():
        population += val

    print(population)


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
