import math
import re
from pathlib import Path
from typing import Optional

from utils import aoc_input
from utils.out import debug

TEST_DATA = """target area: x=20..30, y=-10..-5"""


def main_part_1(input_file: Optional[Path]) -> None:
    input_data = TEST_DATA
    if input_file is not None:
        input_data = input_file.read_text()

    regex = r'target area: x=(\d+)\.\.(\d+), y=(-?\d+)\.\.(-?\d+)'
    matches = re.match(regex, input_data.strip())
    min_x, max_x, min_y, max_y = map(int, matches.groups())
    if min_y > max_y:
        temp = min_y
        min_y = max_y
        max_y = temp
    print(min_x, max_x, min_y, max_y)

    min_vx = math.ceil(math.sqrt(2 * min_x - 0.25) - 0.5)
    max_vx = math.floor(math.sqrt(2 * max_x - 0.25) - 0.5)
    print(min_vx, max_vx)

    max_vy = max(map(abs, [min_y, max_y])) - 1
    print(max_vy)

    height = (max_vy + 1) * max_vy / 2
    print(height)


def main_part_2(input_file: Optional[Path] = None) -> None:
    input_data = TEST_DATA
    if input_file:
        input_data = input_file.read_text()

    regex = r'target area: x=(\d+)\.\.(\d+), y=(-?\d+)\.\.(-?\d+)'
    matches = re.match(regex, input_data.strip())
    min_x, max_x, min_y, max_y = map(int, matches.groups())
    if min_y > max_y:
        temp = min_y
        min_y = max_y
        max_y = temp

    sum_int_till = {}
    for i in range(1, max_x + 1):
        sum_int_till[i] = int(i * (i + 1) / 2)

    min_vx = math.ceil(math.sqrt(2 * min_x - 0.25) - 0.5)
    max_vx = max_x

    min_vy = min_y
    max_vy = max(map(abs, [min_y, max_y])) - 1

    iter_to_vx = {}
    for vx in range(min_vx, max_vx + 1):
        try:
            min_iter = math.ceil(((2 * vx + 1) / 2) - math.sqrt(((2 * vx + 1) / 2)**2 - 2 * min_x))
        except ValueError:
            continue

        try:
            max_iter = math.floor(((2 * vx + 1) / 2) - math.sqrt(((2 * vx + 1) / 2)**2 - 2 * max_x))
        except ValueError:
            max_iter = 300

        for iter_nb in range(min_iter, max_iter + 1):
            if iter_to_vx.get(iter_nb) is None:
                iter_to_vx[iter_nb] = []
            iter_to_vx[iter_nb].append(vx)

    print(iter_to_vx)

    iter_to_vy = {}
    for vy in range(min_vy, max_vy + 1):
        if vy > 0:
            try:
                min_iter = ((2 * vy + 1) / 2) + math.sqrt(((2 * vy + 1) / 2)**2 + 2 * abs(min_y))
            except ValueError:
                continue

            try:
                max_iter = ((2 * vy + 1) / 2) + math.sqrt(((2 * vy + 1) / 2)**2 + 2 * abs(max_y))
            except ValueError:
                continue
        else:
            try:
                min_iter = ((-2 * abs(vy) + 1) / 2) + math.sqrt(((2 * abs(vy) - 1) / 2)**2 + 2 * abs(min_y))
            except ValueError:
                continue

            try:
                max_iter = ((-2 * abs(vy) + 1) / 2) + math.sqrt(((2 * abs(vy) - 1) / 2)**2 + 2 * abs(max_y))
            except ValueError:
                continue

        if min_iter > max_iter:
            temp = min_iter
            min_iter = max_iter
            max_iter = temp

        min_iter = math.ceil(min_iter)
        max_iter = math.floor(max_iter)

        for iter_nb in range(min_iter, max_iter + 1):
            if iter_nb <= 0:
                continue
            if iter_to_vy.get(iter_nb) is None:
                iter_to_vy[iter_nb] = []
            iter_to_vy[iter_nb].append(vy)

    print(iter_to_vy)

    pairs = set([])
    for key, x_sol in iter_to_vx.items():
        if key in iter_to_vy.keys():
            for x in x_sol:
                for y in iter_to_vy[key]:
                    pairs.add((x, y))

    debug(pairs)
    print("must be less than 5746, more than 4606")
    print(len(pairs))


def main(day_num: int, part_num: int, with_test_data=True) -> None:
    input_file = None
    if not with_test_data:
        input_file = aoc_input.get_input(day_num)

    if part_num == 1:
        main_part_1(input_file)
    elif part_num == 2:
        main_part_2(input_file)
    else:
        raise ValueError(f"Invalid part number {part_num}")
