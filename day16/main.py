from dataclasses import dataclass, field
from functools import reduce
from pathlib import Path
from typing import List, Optional, Tuple

from utils import aoc_input
from utils.out import debug

TEST_DATA = "CE00C43D881120"

HEX_TO_BIN = {
    '0': '0000',
    '1': '0001',
    '2': '0010',
    '3': '0011',
    '4': '0100',
    '5': '0101',
    '6': '0110',
    '7': '0111',
    '8': '1000',
    '9': '1001',
    'A': '1010',
    'B': '1011',
    'C': '1100',
    'D': '1101',
    'E': '1110',
    'F': '1111',
}


@dataclass
class Packet:
    version: int
    type_id: int
    literal_value: Optional[int] = None
    children: List['Packet'] = field(default_factory=list)

    @property
    def value(self) -> int:
        if self.type_id == 0:
            return reduce(lambda x, y: x + y, map(lambda x: x.value, self.children))
        elif self.type_id == 1:
            return reduce(lambda x, y: x * y, map(lambda x: x.value, self.children))
        elif self.type_id == 2:
            return reduce(min, map(lambda x: x.value, self.children))
        elif self.type_id == 3:
            return reduce(max, map(lambda x: x.value, self.children))
        elif self.type_id == 4:
            return self.literal_value or 0
        elif self.type_id == 5:
            return 1 if self.children[0].value > self.children[1].value else 0
        elif self.type_id == 6:
            return 1 if self.children[0].value < self.children[1].value else 0
        elif self.type_id == 7:
            return 1 if self.children[0].value == self.children[1].value else 0
        else:
            raise ValueError(f'Unknown type {self.type_id}')


def parse_literal(input_string: str) -> Tuple[int, int]:
    cursor = 0
    done = False
    binary_str = ''
    while not done:
        done = not bool(int(input_string[cursor]))
        binary_str += input_string[cursor + 1:cursor + 5]
        cursor += 5

    return (int(binary_str, 2), cursor)


def parse_sub_packets(input_string: str, max_packets: int = 0) -> Tuple[List[Packet], int]:
    cursor = 0
    packets: List[Packet] = []
    try:
        while max_packets == 0 or len(packets) < max_packets:
            if all(map(lambda x: x == '0', input_string[cursor:])):
                print('clean exit')
                break

            version = int(input_string[cursor:cursor + 3], 2)
            type_id = int(input_string[cursor + 3:cursor + 6], 2)

            if type_id == 4:
                value, next_idx = parse_literal(input_string[cursor + 6:])
                packets.append(Packet(version, type_id, literal_value=value))
                cursor += 6 + next_idx

            else:
                length_type_id = int(input_string[cursor + 6])
                if length_type_id == 0:
                    length = int(input_string[cursor + 7:cursor + 22], 2)
                    sub_packets_str = input_string[cursor + 22:cursor + 22 + length]
                    sub_packets, _ = parse_sub_packets(sub_packets_str)
                    packets.append(Packet(version, type_id, children=sub_packets))
                    cursor = cursor + 22 + length
                else:
                    nb_packets = int(input_string[cursor + 7:cursor + 18], 2)
                    sub_packets, next_idx = parse_sub_packets(input_string[cursor + 18:], max_packets=nb_packets)
                    packets.append(Packet(version, type_id, children=sub_packets))
                    cursor += 18 + next_idx

    except (IndexError, ValueError):
        print('ugly exit')

    return packets, cursor


def total_version(packets: List[Packet]) -> int:
    total = 0
    for packet in packets:
        total += total_version(packet.children)
        total += packet.version

    return total


def main_part_1(input_file: Optional[Path]) -> None:
    input_data = TEST_DATA
    if input_file is not None:
        input_data = input_file.read_text()

    bits = ''
    for hex_char in input_data.strip():
        bits += HEX_TO_BIN[hex_char]

    packets, _ = parse_sub_packets(bits)

    print(total_version(packets))


def main_part_2(input_file: Optional[Path] = None) -> None:
    input_data = TEST_DATA
    if input_file:
        input_data = input_file.read_text()

    bits = ''
    for hex_char in input_data.strip():
        bits += HEX_TO_BIN[hex_char]

    packets, _ = parse_sub_packets(bits)

    print(packets[0].value)


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
