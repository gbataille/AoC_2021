from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional, Set

from utils import aoc_input, geo, strings
from utils.out import debug

TEST_DATA = """1163751742
1381373672
2136511328
3694931569
7463417111
1319128137
1359912421
3125421639
1293138521
2311944581"""


@dataclass
class SubmarinePath:
    head: geo.Cell[geo.Point2D, int]
    weight: int = 0


@dataclass
class Solver:
    chitons: geo.Array2D[int]
    min_map: geo.Array2D[int]
    paths: List[SubmarinePath]
    best: int = -1

    def move1(self) -> 'Solver':
        new_paths: List['SubmarinePath'] = []
        last_cell = self.min_map.get_cell_at(self.min_map.width - 1, self.min_map.height - 1)
        for path in self.paths:
            for cell in self.chitons.neighbours(path.head.coordinates.x, path.head.coordinates.y):
                new_weight = path.weight + cell.value
                min_for_cell = self.min_map.get_cell_at(cell.coordinates.x, cell.coordinates.y)

                if ((min_for_cell.value == -1 or min_for_cell.value > new_weight)
                        and (last_cell.value == -1 or new_weight < last_cell.value)):
                    min_for_cell.value = new_weight
                    new_paths.append(SubmarinePath(head=cell, weight=new_weight))

        self.paths = new_paths

        return self

    def solve(self):
        self.extend(self.chitons.get_cell_at(0, 0))

    def extend(self, cell: geo.Cell[geo.Point2D, int]):
        min_map_cell = self.min_map.get_cell_at(cell.coordinates.x, cell.coordinates.y)
        current_weight = min_map_cell.value
        for neighbour in self.chitons.neighbours(cell.coordinates.x, cell.coordinates.y):
            min_map_neighbour = self.chitons.get_cell_at(neighbour.coordinates.x, neighbour.coordinates.y)
            neighbour_weight = min_map_neighbour.value

            if neighbour_weight == -1 or neighbour_weight > current_weight + cell.value:
                min_map_neighbour.value = current_weight + cell.value
                if not (neighbour.coordinates.x == self.chitons.width - 1
                        and neighbour.coordinates.y == self.chitons.height - 1):
                    self.extend(neighbour)


def main_part_1(input_file: Optional[Path]) -> None:
    input_data = TEST_DATA
    if input_file is not None:
        input_data = input_file.read_text()

    chitons: geo.Array2D[int] = geo.Array2D.from_string(input_data, int)
    min_map: geo.Array2D[int] = geo.Array2D.empty(chitons.width, chitons.height, -1)
    start = chitons.get_cell_at(0, 0)
    paths: List[SubmarinePath] = [SubmarinePath(head=start)]

    solver = Solver(chitons, min_map, paths)
    while solver.paths:
        solver.move1()
        print(
            solver.min_map.to_string(
                lambda x: '  .' if x == -1 else str(x).zfill(3).replace('0', ' '),
                elem_separator=' ',
            ))
        input("press enter")
        print('')

    print(solver.min_map.get_cell_at(solver.min_map.width - 1, solver.min_map.height - 1))


def main_part_2(input_file: Optional[Path] = None) -> None:
    input_data = TEST_DATA
    if input_file:
        input_data = input_file.read_text()

    tile: geo.Array2D[int] = geo.Array2D.from_string(input_data, int)
    chitons: geo.Array2D[int] = geo.Array2D.empty(tile.width * 5, tile.height * 5, -1)
    for chiton_cell in chitons.step_through():
        tile_num_x = int(chiton_cell.coordinates.x / tile.width)
        projected_tile_x = chiton_cell.coordinates.x % tile.width
        tile_num_y = int(chiton_cell.coordinates.y / tile.height)
        projected_tile_y = chiton_cell.coordinates.y % tile.height
        chiton_value = tile.get_cell_at(projected_tile_x, projected_tile_y).value + tile_num_x + tile_num_y
        if chiton_value > 9:
            chiton_value -= 9
        chiton_cell.value = chiton_value

    min_map: geo.Array2D[int] = geo.Array2D.empty(chitons.width, chitons.height, -1)
    min_map.set_value_at(0, 0, 0)
    start = chitons.get_cell_at(0, 0)
    # paths: List[SubmarinePath] = [SubmarinePath(head=start)]
    heads: List[geo.Cell[geo.Point2D, int]] = [start]

    print('algo')
    while heads:
        head = heads.pop()
        for neighbour in chitons.neighbours(head.coordinates.x, head.coordinates.y):
            neighbour_weight = min_map.get_value_at(head.coordinates.x, head.coordinates.y) + neighbour.value
            neighbour_cur_value = min_map.get_value_at(neighbour.coordinates.x, neighbour.coordinates.y)
            if neighbour_cur_value == -1 or neighbour_weight < neighbour_cur_value:
                min_map.set_value_at(neighbour.coordinates.x, neighbour.coordinates.y, neighbour_weight)
                heads.append(neighbour)

        # print(
        #     min_map.to_string(
        #         lambda x: '  .' if x == -1 else strings.replace_leading_x('0', ' ',
        #                                                                   str(x).zfill(3)),
        #         elem_separator=' ',
        #     ))
        # input("press enter")
        # print('')

    print(min_map.get_cell_at(min_map.width - 1, min_map.height - 1))

    # ATTEMPT 1
    # solver = Solver(chitons, min_map, paths)
    # while solver.paths:
    #     solver.move1()
    #
    # print(solver.min_map.get_cell_at(solver.min_map.width - 1, solver.min_map.height - 1))

    # ATTEMPT 2
    # solver2 = Solver(chitons, min_map, paths)
    # solver2.extend(solver2.chitons.get_cell_at(0, 0))
    #
    # print(solver2.min_map.get_cell_at(solver2.min_map.width - 1, solver2.min_map.height - 1))


def main(day_num: int, part_num: int, with_test_data=True) -> None:
    input_file = None
    if not with_test_data:
        input_file = aoc_input.get_input(day_num)

    if part_num == 1:
        main_part_1(input_file)
    elif part_num == 2:
        main_part_2(input_file)
    else:
        raise ValueError(f"Invalid part number 0part_num0")
