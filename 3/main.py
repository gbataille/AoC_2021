from pathlib import Path
from typing import List, Optional

from utils import aoc_input

TEST_DATA = """00100
11110
10110
10111
10101
01111
00111
11100
10000
11001
00010
01010"""


def main_part_1(input_file: Optional[Path]) -> None:
    input_data = TEST_DATA
    if input_file is not None:
        input_data = input_file.read_text()

    gamma_rate = ''
    epsilon_rate = ''
    lines = input_data.strip().split('\n')
    one_frequency = [0] * len(lines[0])
    cnt = 0
    for line in lines:
        for idx, char in enumerate(line):
            if char == '1':
                one_frequency[idx] = one_frequency[idx] + 1

        cnt += 1

    for nb in one_frequency:
        if nb > cnt / 2:
            gamma_rate = gamma_rate + '1'
            epsilon_rate = epsilon_rate + '0'
        else:
            gamma_rate = gamma_rate + '0'
            epsilon_rate = epsilon_rate + '1'

    print(gamma_rate)
    print(epsilon_rate)
    print(int(gamma_rate, 2) * int(epsilon_rate, 2))


def freq(string_list: List[str]) -> List[int]:
    one_frequency = [0] * len(string_list[0])
    for line in string_list:
        for idx, char in enumerate(line):
            if char == '1':
                one_frequency[idx] = one_frequency[idx] + 1

    return one_frequency


def main_part_2(input_file: Optional[Path] = None) -> None:
    input_data = TEST_DATA
    if input_file:
        input_data = input_file.read_text()

    oxygen_rating = None
    co2_rating = None

    lines = input_data.strip().split('\n')

    candidates = lines
    bit = 0
    while oxygen_rating is None:
        one_frequency = freq(candidates)
        bit_criteria = 0
        if one_frequency[bit] >= len(candidates) / 2:
            bit_criteria = 1
        remaining = []
        for candidate in candidates:
            if candidate[bit] == str(bit_criteria):
                remaining.append(candidate)

        candidates = remaining
        bit += 1
        if len(candidates) == 1:
            oxygen_rating = candidates[0]
        if len(candidates) == 0:
            raise ValueError("no more candidates")

        print(candidates)
        print('')

    candidates = lines
    bit = 0
    while co2_rating is None:
        one_frequency = freq(candidates)
        bit_criteria = 1
        if one_frequency[bit] >= len(candidates) / 2:
            bit_criteria = 0
        remaining = []
        for candidate in candidates:
            if candidate[bit] == str(bit_criteria):
                remaining.append(candidate)

        candidates = remaining
        bit += 1
        if len(candidates) == 1:
            co2_rating = candidates[0]
        if len(candidates) == 0:
            raise ValueError("no more candidates")

    print(oxygen_rating, int(oxygen_rating, 2))
    print(co2_rating, int(co2_rating, 2))
    print(int(oxygen_rating, 2) * int(co2_rating, 2))


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
