"""
Lacks optimizations (repeated sub path for example)
"""
from copy import deepcopy
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional, Set

from utils import aoc_input
from utils.out import debug

TEST_DATA = """start-A
start-b
A-c
A-b
b-d
A-end
b-end"""

TEST_DATA = """dc-end
HN-start
start-kj
dc-start
dc-HN
LN-dc
HN-end
kj-sa
kj-HN
kj-dc"""

TEST_DATA = """fs-end
he-DX
fs-he
start-DX
pj-DX
end-zg
zg-sl
zg-pj
pj-he
RW-he
fs-DX
pj-RW
zg-RW
start-pj
he-WI
zg-he
pj-fs
start-RW"""


@dataclass
class Cave:
    name: str

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Cave):
            return False
        return self.name == other.name

    def __hash__(self):
        return hash(self.name)

    def is_small(self) -> bool:
        return ord('a') <= ord(self.name[0]) <= ord('z')

    def is_start_end(self) -> bool:
        return self.name in ['start', 'end']


@dataclass
class CavePath:
    caves: List[Cave]
    small_caves_seen: Set[Cave] = field(default_factory=set)
    has_gone_twice_to_small: bool = False

    def move1(self, connections: Dict[str, str]) -> List[Path]:
        available_connections = connections.get(self.caves[-1])

        new_pathes = []
        for connected_cave in available_connections:
            new_path_has_gone_twice_to_small = self.has_gone_twice_to_small
            new_small_caves_seen = set(self.small_caves_seen)

            if connected_cave.is_small():
                if connected_cave in self.small_caves_seen:
                    if connected_cave.is_start_end():
                        continue
                    if self.has_gone_twice_to_small:
                        continue
                    else:
                        new_path_has_gone_twice_to_small = True
                else:
                    new_small_caves_seen.add(connected_cave)

            new_path = CavePath(
                caves=self.caves + [connected_cave],
                small_caves_seen=new_small_caves_seen,
                has_gone_twice_to_small=new_path_has_gone_twice_to_small,
            )
            new_pathes.append(new_path)

        return new_pathes

    def is_done(self) -> bool:
        return self.caves[-1] == Cave('end')


def main_part_1(input_file: Optional[Path]) -> None:
    input_data = TEST_DATA
    if input_file is not None:
        input_data = input_file.read_text()

    connections: Dict[Cave, List[Cave]] = {}
    explored_paths: List[CavePath] = [CavePath([Cave('start')], small_caves_seen=set([Cave('start')]))]
    final_paths: List[CavePath] = []

    for line in input_data.strip().split('\n'):
        from_cave, to_cave = line.strip().split('-')
        from_cave = Cave(from_cave)
        to_cave = Cave(to_cave)
        if connections.get(from_cave) is None:
            connections[from_cave] = []
        if connections.get(to_cave) is None:
            connections[to_cave] = []
        connections[from_cave].append(to_cave)
        connections[to_cave].append(from_cave)

    while explored_paths:
        new_explored_paths = []

        for path in explored_paths:
            new_pathes = path.move1(connections)
            while new_pathes:
                path = new_pathes.pop()
                if path.is_done():
                    final_paths.append(path)
                else:
                    new_explored_paths.append(path)

        explored_paths = new_explored_paths

    print(len(final_paths))


def main_part_2(input_file: Optional[Path] = None) -> None:
    input_data = TEST_DATA
    if input_file:
        input_data = input_file.read_text()


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
