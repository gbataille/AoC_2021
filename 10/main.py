from pathlib import Path
from typing import List, Optional

from utils import aoc_input
from utils.out import debug

TEST_DATA = """[({(<(())[]>[[{[]{<()<>>
[(()[<>])]({[<{<<[]>>(
{([(<{}[<>[]}>{[]{[(<()>
(((({<>}<{<{<>}{[]{[]{}
[[<[([]))<([[{}[[()]]]
[{[{({}]{}}([{[{{{}}([]
{<[[]]>}<{[{[{[]{()[[[]
[<(<(<(<{}))><([]([]()
<{([([[(<>()){}]>(<<{{
<{([{{}}[<[[[<>{}]]]>[]]"""

POINTS = {
    ')': 3,
    ']': 57,
    '}': 1197,
    '>': 25137,
}

AUTOCOMPLETE = {
    '(': 1,
    '[': 2,
    '{': 3,
    '<': 4,
}


def main_part_1(input_file: Optional[Path]) -> None:
    input_data = TEST_DATA
    if input_file is not None:
        input_data = input_file.read_text()

    score = 0
    for line in input_data.strip().split('\n'):
        stack = []
        for char in line:
            if char in ['(', '<', '{', '[']:
                stack.append(char)
            else:
                if (char == ')' and stack[-1] == '(' or char == '}' and stack[-1] == '{'
                        or char == '>' and stack[-1] == '<' or char == ']' and stack[-1] == '['):
                    stack.pop()
                else:
                    score += POINTS[char]
                    break

    print(score)


def main_part_2(input_file: Optional[Path] = None) -> None:
    input_data = TEST_DATA
    if input_file:
        input_data = input_file.read_text()

    ok_lines: List[List[str]] = []
    for line in input_data.strip().split('\n'):
        stack = []
        corrupt = False
        for char in line:
            if char in ['(', '<', '{', '[']:
                stack.append(char)
            else:
                if (char == ')' and stack[-1] == '(' or char == '}' and stack[-1] == '{'
                        or char == '>' and stack[-1] == '<' or char == ']' and stack[-1] == '['):
                    stack.pop()
                else:
                    corrupt = True
                    break

        if not corrupt:
            ok_lines.append(stack)

    scores = []
    for line in ok_lines:
        score = 0
        for idx in range(len(line) - 1, -1, -1):
            char = line[idx]
            score = score * 5 + AUTOCOMPLETE[char]

        scores.append(score)

    print(scores)
    scores.sort()
    print(scores)
    print(len(scores))
    print(int(len(scores) / 2))
    print(scores[int(len(scores) / 2)])


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
