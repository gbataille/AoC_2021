from pathlib import Path
from typing import Dict, List, Optional, Tuple

import numpy as np

from utils import aoc_input
from utils.out import debug

TEST_DATA = "16,1,2,0,4,2,7,1,2,14"


def main_part_1(input_file: Optional[Path]) -> None:
    input_data = TEST_DATA
    if input_file is not None:
        input_data = input_file.read_text()

    crabs = list(map(int, input_data.strip().split(',')))
    horizontal_target = int(np.median(crabs))
    fuel = 0
    for crab in crabs:
        fuel += abs(crab - horizontal_target)

    print(fuel)


def main_part_2(input_file: Optional[Path] = None) -> None:
    input_data = TEST_DATA
    if input_file:
        input_data = input_file.read_text()

    crabs = list(map(int, input_data.strip().split(',')))

    def cost(crabs: List[int], target: int) -> int:
        cost = 0
        for crab in crabs:
            distance = abs(crab - target)
            cost += distance * (distance + 1) / 2

        return cost

    middle = int((max(crabs) - min(crabs)) / 2)
    cost_middle = cost(crabs, middle)
    cost_left = cost(crabs, min(crabs))
    cost_right = cost(crabs, max(crabs))
    start_state = {'left': (min(crabs), cost_left), 'middle': (middle, cost_middle), 'right': (max(crabs), cost_right)}

    def iterate(state: Dict[int, Tuple[int, int]]) -> Dict[int, int]:
        print(state)
        if state['left'] == state['middle'] or state['right'] == state['middle']:
            return state

        if state['left'][1] < state['right'][1]:
            middle_loc = abs(int((state['left'][0] + state['middle'][0]) / 2))
            middle_cost = cost(crabs, middle_loc)
            middle = (middle_loc, middle_cost)
            iterate({'left': state['left'], 'middle': middle, 'right': state['middle']})
        else:
            middle_loc = abs(int((state['right'][0] + state['middle'][0]) / 2))
            middle_cost = cost(crabs, middle_loc)
            middle = (middle_loc, middle_cost)
            iterate({'left': state['middle'], 'middle': middle, 'right': state['right']})

    print(iterate(start_state))

    # horizontal_target = round(np.average(crabs))
    # fuel = 0
    # for crab in crabs:
    #     distance = abs(crab - horizontal_target)
    #     fuel += distance * (distance + 1) / 2
    #
    # print(fuel)


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
