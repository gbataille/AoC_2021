from pathlib import Path
from typing import Optional

from utils import aoc_input
from utils.out import debug

TEST_DATA = """NNCB

CH -> B
HH -> N
CB -> H
NH -> C
HB -> C
HC -> B
HN -> C
NN -> C
BH -> H
NC -> B
NB -> B
BN -> B
BB -> N
BC -> B
CC -> N
CN -> C"""


def main_part_1(input_file: Optional[Path]) -> None:
    input_data = TEST_DATA
    if input_file is not None:
        input_data = input_file.read_text()

    lines = input_data.strip().split('\n')
    template_str = lines[0]
    pair_insertions = lines[2:]
    rules = {}
    for pair_insertion in pair_insertions:
        from_pair, added_base = pair_insertion.split(' -> ')
        rules[from_pair] = added_base

    for _ in range(10):
        new_template = template_str[0]
        for idx in range(len(template_str) - 1):
            pair = template_str[idx:idx + 2]
            base = rules[pair]
            new_template = new_template + f'{base}{pair[1]}'

        template_str = new_template

    count = {}
    for char in template_str:
        if char not in count.keys():
            count[char] = 0
        count[char] += 1

    max_char = (0, 'A')
    min_char = (99999999999999999999, 'A')

    for char, nb in count.items():
        if nb > max_char[0]:
            max_char = (nb, char)
        elif nb < min_char[0]:
            min_char = (nb, char)

    print(max_char[0] - min_char[0])


def main_part_2(input_file: Optional[Path] = None) -> None:
    input_data = TEST_DATA
    if input_file:
        input_data = input_file.read_text()

    lines = input_data.strip().split('\n')
    template_str = lines[0]
    pair_insertions = lines[2:]
    rules = {}
    for pair_insertion in pair_insertions:
        from_pair, added_base = pair_insertion.split(' -> ')
        rules[from_pair] = added_base

    pairs = {}
    for idx in range(len(template_str) - 1):
        pair = template_str[idx:idx + 2]
        if pair not in pairs.keys():
            pairs[pair] = 0
        pairs[pair] += 1

    for iteration in range(40):
        # debug(f'###### {iteration} #######')
        # debug(pairs)
        new_pairs = {}
        for pair, cnt in list(pairs.items()):
            base = rules[pair]
            key1 = f'{pair[0]}{base}'
            key2 = f'{base}{pair[1]}'
            # debug(f'{key1} - {key2}')
            if key1 not in new_pairs.keys():
                new_pairs[key1] = 0
            if key2 not in new_pairs.keys():
                new_pairs[key2] = 0
            new_pairs[key1] += cnt
            new_pairs[key2] += cnt
            # debug(new_pairs)
            # debug('')

        pairs = new_pairs

    start_count = {}
    end_count = {}
    for pair, cnt in pairs.items():
        if pair[0] not in start_count.keys():
            start_count[pair[0]] = 0
        if pair[1] not in end_count.keys():
            end_count[pair[1]] = 0
        start_count[pair[0]] += cnt
        end_count[pair[1]] += cnt

    count = {}
    for char, cnt in end_count.items():
        count[char] = max(cnt, start_count[char])

    max_char = (-1, '')
    min_char = (-1, '')

    for char, nb in count.items():
        if nb > max_char[0]:
            max_char = (nb, char)
        elif min_char[0] == -1 or nb < min_char[0]:
            min_char = (nb, char)

    print(max_char[0] - min_char[0])


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
