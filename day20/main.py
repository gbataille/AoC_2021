from pathlib import Path
from typing import Optional

from utils import aoc_input, geo
from utils.out import debug

TEST_DATA = """..#.#..#####.#.#.#.###.##.....###.##.#..###.####..#####..#....#..#..##..###..######.###...####..#..#####..##..#.#####...##.#.#..#.##..#.#......#.###.######.###.####...#.##.##..#..#..#####.....#.#....###..#.##......#.....#..#..#..##..#...##.######.####.####.#.#...#.......#..#.#.#...####.##.#......#..#...##.#.##..#...##.#.##..###.#......#.#.......#.#.#.####.###.##...#.....####.#..#..#.##.#....##..#.####....##...##..#...#......#.#.......#.......##..####..#...#.#.#...##..#.#..###..#####........#..####......#..#

#..#.
#....
##..#
..#..
..###"""


def main_part_1(input_file: Optional[Path]) -> None:
    input_data = TEST_DATA
    if input_file is not None:
        input_data = input_file.read_text()

    lines = input_data.strip().split('\n')
    algo = lines[0]

    image = geo.Array2D[str].from_string('\n'.join(lines[2:]), lambda x: x)
    nb_run = 2

    while nb_run > 0:
        new_image = geo.Array2D[str].empty(image.width + 2, image.height + 2, '.')
        for node in new_image.step_through():
            bin_str = ''
            for y in range(node.coordinates.y - 1, node.coordinates.y + 2):
                for x in range(node.coordinates.x - 1, node.coordinates.x + 2):
                    x_image = x - 1
                    y_image = y - 1
                    if x_image < 0 or y_image < 0 or x_image >= image.width or y_image >= image.height:
                        if algo[0] == '.':
                            bin_str += '.'
                        else:
                            if nb_run % 2 == 0:
                                bin_str += '.'
                            else:
                                bin_str += '#'
                    else:
                        bin_str += image.get_value_at(x_image, y_image)
            bin_str = bin_str.replace('.', '0')
            bin_str = bin_str.replace('#', '1')
            index = int(bin_str, 2)
            node.value = algo[index]
            # print(node.coordinates, bin_str, node.value)
            # input('\n')

        print(new_image.to_string(str))

        nb_run -= 1
        image = new_image

    nb_pixels = 0
    for node in image.step_through():
        if node.value == '#':
            nb_pixels += 1

    print('less than 5278')
    print(nb_pixels)


def main_part_2(input_file: Optional[Path] = None) -> None:
    input_data = TEST_DATA
    if input_file:
        input_data = input_file.read_text()

    lines = input_data.strip().split('\n')
    algo = lines[0]

    image = geo.Array2D[str].from_string('\n'.join(lines[2:]), lambda x: x)
    nb_run = 50

    while nb_run > 0:
        new_image = geo.Array2D[str].empty(image.width + 2, image.height + 2, '.')
        for node in new_image.step_through():
            bin_str = ''
            for y in range(node.coordinates.y - 1, node.coordinates.y + 2):
                for x in range(node.coordinates.x - 1, node.coordinates.x + 2):
                    x_image = x - 1
                    y_image = y - 1
                    if x_image < 0 or y_image < 0 or x_image >= image.width or y_image >= image.height:
                        if algo[0] == '.':
                            bin_str += '.'
                        else:
                            if nb_run % 2 == 0:
                                bin_str += '.'
                            else:
                                bin_str += '#'
                    else:
                        bin_str += image.get_value_at(x_image, y_image)
            bin_str = bin_str.replace('.', '0')
            bin_str = bin_str.replace('#', '1')
            index = int(bin_str, 2)
            node.value = algo[index]
            # print(node.coordinates, bin_str, node.value)
            # input('\n')

        nb_run -= 1
        image = new_image

    nb_pixels = 0
    for node in image.step_through():
        if node.value == '#':
            nb_pixels += 1

    print(nb_pixels)


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
