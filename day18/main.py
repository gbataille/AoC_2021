import math
from dataclasses import dataclass
from itertools import permutations
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union, cast

from utils import aoc_input
from utils.out import debug


@dataclass
class SnailNum:
    left: Union[int, 'SnailNum']
    right: Union[int, 'SnailNum']
    depth: int = 0
    max_children_depth: int = 0
    is_full_left: bool = False
    is_full_right: bool = False

    def __post_init__(self):
        self._set_depth(depth=0)

    def _set_depth(
        self,
        depth: int = 0,
    ) -> Tuple[int, int, bool, bool]:
        left_max_depth = 0
        right_max_depth = 0
        left_full_left = True
        right_full_right = True

        if isinstance(self.left, SnailNum):
            _, left_max_depth, left_full_left, _ = self.left._set_depth(depth=depth + 1)
        if isinstance(self.right, SnailNum):
            _, right_max_depth, _, rigth_full_right = self.right._set_depth(depth=depth + 1)

        self.depth = depth
        self.max_children_depth = max([left_max_depth, right_max_depth, depth])

        if self.max_children_depth == left_max_depth:
            is_full_right = False
            is_full_left = left_full_left
        elif self.max_children_depth == right_max_depth:
            is_full_left = False
            is_full_right = right_full_right
        else:
            is_full_right = True
            is_full_left = True

        self.is_full_left = is_full_left
        self.is_full_right = is_full_right

        return self.depth, self.max_children_depth, self.is_full_left, self.is_full_right

    def leftmost(self) -> int:
        if isinstance(self.left, int):
            return self.left
        else:
            return self.left.leftmost()

    def rightmost(self) -> int:
        if isinstance(self.right, int):
            return self.right
        else:
            return self.right.rightmost()

    @staticmethod
    def add(a: 'SnailNum', b: 'SnailNum') -> 'SnailNum':
        sn = SnailNum(left=a, right=b)
        sn.reduce()
        return sn

    @staticmethod
    def add_num(a: 'SnailNum', b: int, side: str) -> None:
        if side == 'left':
            if isinstance(a.left, SnailNum):
                SnailNum.add_num(a.left, b, side)
            else:
                a.left += b
        if side == 'right':
            if isinstance(a.right, SnailNum):
                SnailNum.add_num(a.right, b, side)
            else:
                a.right += b

    @staticmethod
    def from_list(snail_list: List[Any]) -> 'SnailNum':
        if len(snail_list) != 2:
            raise ValueError("Not a pair")

        left = snail_list[0]
        if isinstance(snail_list[0], list):
            left = SnailNum.from_list(snail_list[0])
        right = snail_list[1]
        if isinstance(snail_list[1], list):
            right = SnailNum.from_list(snail_list[1])

        return SnailNum(left, right)

    def to_string(self):
        left: str
        right: str
        if isinstance(self.left, SnailNum):
            left = self.left.to_string()
        else:
            left = str(self.left)
        if isinstance(self.right, SnailNum):
            right = self.right.to_string()
        else:
            right = str(self.right)

        return f'[{left},{right}]'

    def reduce(self) -> 'SnailNum':
        _, exploded, _, _ = self.explode()
        if exploded:
            self._set_depth()
            return self.reduce()

        _, splitted = self.split()
        if splitted:
            self._set_depth()
            return self.reduce()

        return self

    def explode(self) -> Tuple['SnailNum', bool, int, int]:
        if self.max_children_depth < 4:
            return self, False, 0, 0

        if self.depth == 3:
            left: int
            right: int
            if isinstance(self.left, SnailNum):
                left = self.left.left  # type:ignore
                right = self.left.right  # type:ignore
                self.left = 0

                if isinstance(self.right, SnailNum):
                    SnailNum.add_num(self.right, right, 'left')
                else:
                    self.right += right
                right = 0

            else:
                left = self.right.left  # type:ignore
                right = self.right.right  # type:ignore
                self.right = 0

                if isinstance(self.left, SnailNum):
                    SnailNum.add_num(self.left, left, 'right')
                else:
                    self.left += left
                left = 0

            return self, True, left, right

        if isinstance(self.left, SnailNum) and self.left.max_children_depth >= 4:
            _, _, left_add, right_add = self.left.explode()
            if isinstance(self.right, SnailNum):
                SnailNum.add_num(self.right, right_add, 'left')
            else:
                self.right += right_add
            right_add = 0
            return self, True, left_add, right_add

        if isinstance(self.right, SnailNum) and self.right.max_children_depth >= 4:
            _, _, left_add, right_add = self.right.explode()
            if isinstance(self.left, SnailNum):
                SnailNum.add_num(self.left, left_add, 'right')
            else:
                self.left += left_add
            left_add = 0
            return self, True, left_add, right_add

        raise ValueError("We should not be there")

    def split(self) -> Tuple['SnailNum', bool]:
        if isinstance(self.left, SnailNum):
            _, splitted = self.left.split()
            if splitted:
                return self, True
        else:
            if self.left > 9:
                self.left = SnailNum(left=math.floor(self.left / 2), right=math.ceil(self.left / 2))
                return self, True

        if isinstance(self.right, SnailNum):
            _, splitted = self.right.split()
            if splitted:
                return self, True
        else:
            if self.right > 9:
                self.right = SnailNum(left=math.floor(self.right / 2), right=math.ceil(self.right / 2))
                return self, True

        return self, False

    def magnitude(self) -> int:
        left_magnitude: int
        right_magnitude: int
        if isinstance(self.left, SnailNum):
            left = self.left.magnitude()
        else:
            left = self.left
        if isinstance(self.right, SnailNum):
            right = self.right.magnitude()
        else:
            right = self.right

        return 3 * left + 2 * right


TEST_DATA = """[[[0,[5,8]],[[1,7],[9,6]]],[[4,[1,2]],[[1,4],2]]]
[[[5,[2,8]],4],[5,[[9,9],0]]]
[6,[[[6,2],[5,6]],[[7,6],[4,7]]]]
[[[6,[0,7]],[0,9]],[4,[9,[9,0]]]]
[[[7,[6,4]],[3,[1,3]]],[[[5,5],1],9]]
[[6,[[7,3],[3,2]]],[[[3,8],[5,7]],4]]
[[[[5,4],[7,7]],8],[[8,3],8]]
[[9,3],[[9,9],[6,[4,9]]]]
[[2,[[7,7],7]],[[5,8],[[9,3],[0,2]]]]
[[[[5,2],5],[8,[3,7]]],[[5,[7,5]],[4,4]]]"""


def main_part_1(input_file: Optional[Path]) -> None:
    input_data = TEST_DATA
    if input_file is not None:
        input_data = input_file.read_text()

    tot = None
    for line in input_data.strip().split('\n'):
        snail_num = SnailNum.from_list(eval(line))
        if tot is None:
            tot = snail_num
        else:
            tot = SnailNum.add(tot, snail_num)

    print(tot.to_string())
    print(tot.magnitude())


def main_part_2(input_file: Optional[Path] = None) -> None:
    input_data = TEST_DATA
    if input_file:
        input_data = input_file.read_text()

    nums: List[SnailNum] = []
    for line in input_data.strip().split('\n'):
        sn = SnailNum.from_list(eval(line))
        nums.append(sn)

    max_magnitude = 0
    i = 0
    for pair in permutations(nums, 2):
        sum_num = SnailNum.add(
            SnailNum.from_list(eval(pair[0].to_string())),
            SnailNum.from_list(eval(pair[1].to_string())),
        )
        magnitude = sum_num.magnitude()
        print(i)
        print(pair[0].to_string())
        print(pair[1].to_string())
        print(sum_num.to_string())
        print(magnitude)
        print('')
        if magnitude > max_magnitude:
            max_magnitude = magnitude
        i += 1

    print(max_magnitude)


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
