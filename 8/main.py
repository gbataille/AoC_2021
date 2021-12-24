from pathlib import Path
from typing import Optional

from utils import aoc_input
from utils.out import debug

TEST_DATA = """be cfbegad cbdgef fgaecd cgeb fdcge agebfd fecdb fabcd edb | fdgacbe cefdb cefbgd gcbe
edbfga begcd cbg gc gcadebf fbgde acbgfd abcde gfcbed gfec | fcgedb cgb dgebacf gc
fgaebd cg bdaec gdafb agbcfd gdcbef bgcad gfac gcb cdgabef | cg cg fdcagb cbg
fbegcd cbd adcefb dageb afcb bc aefdc ecdab fgdeca fcdbega | efabcd cedba gadfec cb
aecbfdg fbg gf bafeg dbefa fcge gcbea fcaegb dgceab fcbdga | gecf egdcabf bgf bfgea
fgeab ca afcebg bdacfeg cfaedg gcfdb baec bfadeg bafgc acf | gebdcfa ecba ca fadegcb
dbcfg fgd bdegcaf fgec aegbdf ecdfab fbedc dacgb gdcebf gf | cefg dcbef fcge gbcadfe
bdfegc cbegaf gecbf dfcage bdacg ed bedf ced adcbefg gebcd | ed bcgafe cdgba cbgef
egadfb cdbfeg cegd fecab cgb gbdefca cg fgcdab egfdb bfceg | gbdfcae bgc cg cgb
gcafb gcf dcaebfg ecagb gf abcdeg gaef cafbge fdbac fegbdc | fgae cfgab fg bagce"""

# TEST_DATA = """acedgfb cdfbe gcdfa fbcad dab cefabd cdfgeb eafb cagedb ab | cdfeb fcadb cdfeb cdbaf"""

SEVEN_SEGMENT_NUM = {
    1: 2,
    2: 5,
    3: 5,
    4: 4,
    6: 6,
    7: 3,
    8: 7,
    9: 6,
    0: 6,
}
UNIQUE_REPR = {1: 2, 4: 4, 7: 3, 8: 7}


def main_part_1(input_file: Optional[Path]) -> None:
    input_data = TEST_DATA
    if input_file is not None:
        input_data = input_file.read_text()

    lines = input_data.strip().split('\n')
    cnt = 0
    for line in lines:
        ten_digits_list, output_list = line.strip().split('|')
        ten_digits = ten_digits_list.strip().split(' ')
        outputs = output_list.strip().split(' ')

        for output in outputs:
            if len(output) in UNIQUE_REPR.values():
                cnt += 1

    print(cnt)


def main_part_2(input_file: Optional[Path] = None) -> None:
    input_data = TEST_DATA
    if input_file:
        input_data = input_file.read_text()

    tot = 0
    lines = input_data.strip().split('\n')
    for line in lines:
        ten_digits_list, output_list = line.strip().split('|')
        ten_digits = ten_digits_list.strip().split(' ')
        outputs = output_list.strip().split(' ')

        ten_digits_per_length = {}
        for digit in ten_digits:
            l = len(digit)
            if l not in ten_digits_per_length.keys():
                ten_digits_per_length[l] = []

            ten_digits_per_length[l].append(digit)

        one = list(filter(lambda x: len(x) == 2, ten_digits))[0]
        four = list(filter(lambda x: len(x) == 4, ten_digits))[0]
        seven = list(filter(lambda x: len(x) == 3, ten_digits))[0]
        eight = list(filter(lambda x: len(x) == 7, ten_digits))[0]
        three = list(filter(lambda x: len(set(x) - set(one)) == 3, ten_digits_per_length[5]))[0]
        ten_digits_per_length[5].remove(three)
        nine = list(filter(lambda x: len(set(x) - set(three)) == 1, ten_digits_per_length[6]))[0]
        ten_digits_per_length[6].remove(nine)
        five = list(filter(lambda x: len(set(nine) - set(x)) == 1, ten_digits_per_length[5]))[0]
        ten_digits_per_length[5].remove(five)
        two = ten_digits_per_length[5][0]
        ten_digits_per_length[5].remove(two)
        six = list(filter(lambda x: len(set(x) - set(five)) == 1, ten_digits_per_length[6]))[0]
        ten_digits_per_length[6].remove(six)
        zero = ten_digits_per_length[6][0]
        ten_digits_per_length[6].remove(zero)

        decoder = {
            one: '1',
            two: '2',
            three: '3',
            four: '4',
            five: '5',
            six: '6',
            seven: '7',
            eight: '8',
            nine: '9',
            zero: '0'
        }

        num = ''
        for output in outputs:
            for k, v in decoder.items():
                if set(k) == set(output):
                    num = f'{num}{str(v)}'
                    break

        tot += int(num)
    print(tot)


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
