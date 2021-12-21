from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional

from utils import aoc_input

TEST_DATA = """7,4,9,5,11,17,23,2,0,14,21,24,10,16,13,6,15,25,12,22,18,20,8,19,3,26,1

22 13 17 11  0
 8  2 23  4 24
21  9 14 16  7
 6 10  3 18  5
 1 12 20 15 19

 3 15  0  2 22
 9 18 13 17  5
19  8  7 25 23
20 11 10 24  4
14 21 16 12  6

14 21 17 24  4
10 16 15  9 19
18  8 23 26 20
22 11 13  6  5
 2  0 12  3  7"""


@dataclass
class Cell:
    num: int
    marked: bool = False


@dataclass
class Board:
    board: List[List[Cell]] = field(default_factory=list)

    def add_line(self, line: str) -> 'Board':
        nums = list(filter(lambda x: bool(x), line.split(' ')))
        self.board.append(list(map(lambda x: Cell(int(x)), nums)))
        return self

    def mark_num(self, num: int) -> 'Board':
        for line in self.board:
            for cell in line:
                if cell.num == num:
                    cell.marked = True
        return self

    def is_winner(self) -> bool:
        for line in self.board:
            if all(map(lambda x: x.marked, line)):
                return True

        for idx in range(5):
            if all(map(lambda x: x.marked, map(lambda x: x[idx], self.board))):
                return True

        return False

    def score(self, last_drawn_num: int) -> int:
        score = 0
        for line in self.board:
            for cell in line:
                if not cell.marked:
                    score += cell.num

        print(score)
        print(last_drawn_num)
        return score * last_drawn_num


def main_part_1(input_file: Optional[Path]) -> None:
    input_data = TEST_DATA
    if input_file is not None:
        input_data = input_file.read_text()

    boards: List[Board] = []
    draw: List[int] = []

    lines = input_data.strip().split('\n')
    draw = list(map(int, lines[0].split(',')))
    print(draw)

    board: Board = None
    for line in lines[1:]:
        if not line:
            if board is not None:
                boards.append(board)
            board = Board()
        else:
            board.add_line(line)

    boards.append(board)

    winner: Board = None
    draw_idx = 0
    while winner is None:
        drawn_num = draw[draw_idx]
        for board in boards:
            board.mark_num(drawn_num)
            if board.is_winner():
                winner = board
                break
        draw_idx += 1

    print(winner.score(draw[draw_idx - 1]))


def main_part_2(input_file: Optional[Path] = None) -> None:
    input_data = TEST_DATA
    if input_file:
        input_data = input_file.read_text()

    boards: List[Board] = []
    draw: List[int] = []

    lines = input_data.strip().split('\n')
    draw = list(map(int, lines[0].split(',')))

    board: Board = None
    for line in lines[1:]:
        if not line:
            if board is not None:
                boards.append(board)
            board = Board()
        else:
            board.add_line(line)

    boards.append(board)

    done: bool = False
    last_winner: List[Board] = []
    draw_idx = 0
    while not done:
        last_winner = []
        drawn_num = draw[draw_idx]
        for board in boards:
            board.mark_num(drawn_num)
            if board.is_winner():
                last_winner.append(board)
        draw_idx += 1

        for w in last_winner:
            boards.remove(w)
        print(f'Remains {len(boards)} boards')
        done = boards == []

    print(last_winner)
    print(last_winner[0].score(draw[draw_idx - 1]))


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
