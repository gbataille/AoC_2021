from pathlib import Path
from typing import Optional

from utils import aoc_input, geo
from utils.out import debug

TEST_DATA = """5483143223
2745854711
5264556173
6141336146
6357385478
4167524645
2176841721
6882881134
4846848554
5283751526"""

ITERATIONS = 100


def main_part_1(input_file: Optional[Path]) -> None:
    input_data = TEST_DATA
    if input_file is not None:
        input_data = input_file.read_text()

    flashes = 0
    octos = geo.Array2D.from_string(input_data, int)
    for _ in range(ITERATIONS):
        for octo_cell in octos:
            octo_cell.value += 1
            octos.set_cell(octo_cell)

        flashing = True
        while flashing:
            flashing = False
            for octo_cell in octos:
                if octo_cell.value > 9:
                    flashing = True
                    for neighbour in octos.neighbours(octo_cell.coordinates.x,
                                                      octo_cell.coordinates.y,
                                                      include_diags=True):
                        if neighbour.value != -1:
                            neighbour.value += 1
                            octos.set_cell(neighbour)

                    flashes += 1
                    octo_cell.value = -1
                    octos.set_cell(octo_cell)

        for octo_cell in octos:
            if octo_cell.value == -1:
                octo_cell.value = 0
                octos.set_cell(octo_cell)

    print(octos.to_string())
    print(flashes)


def main_part_2(input_file: Optional[Path] = None) -> None:
    input_data = TEST_DATA
    if input_file:
        input_data = input_file.read_text()

    octos = geo.Array2D.from_string(input_data, int)
    step = 1
    while True:
        for octo_cell in octos:
            octo_cell.value += 1
            octos.set_cell(octo_cell)

        flashing = True
        nb_flash = 0
        while flashing:
            flashing = False
            for octo_cell in octos:
                if octo_cell.value > 9:
                    flashing = True
                    for neighbour in octos.neighbours(octo_cell.coordinates.x,
                                                      octo_cell.coordinates.y,
                                                      include_diags=True):
                        if neighbour.value != -1:
                            neighbour.value += 1
                            octos.set_cell(neighbour)

                    nb_flash += 1
                    octo_cell.value = -1
                    octos.set_cell(octo_cell)

        if nb_flash == 100:
            break

        for octo_cell in octos:
            if octo_cell.value == -1:
                octo_cell.value = 0
                octos.set_cell(octo_cell)

        step += 1

    print(step)


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
