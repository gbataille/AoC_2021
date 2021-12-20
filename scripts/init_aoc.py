from pathlib import Path

day_file = """from pathlib import Path

from utils import aoc_input


def main_part_1() -> None:
    input_data = input_file.read_text()


def main_part_2() -> None:
    input_data = input_file.read_text()


def main(day_num: int, part_num: int) -> None:
    if part_num == 1:
        aoc_input.get_input(day_num, part_num)
        main_part_1()
    elif part_num == 2:
        aoc_input.get_input(day_num, part_num)
        main_part_2()
    else:
        raise ValueError(f"Invalid part number {part_num}")"""


def main():
    root_path = Path(__file__).parent.parent
    for day in range(1, 26):
        day_path = root_path.joinpath(str(day))
        if not day_path.exists():
            day_path.mkdir()
        day_path.joinpath("__init__.py").write_text("from .main import *")
        day_path.joinpath("main.py").write_text(day_file)


if __name__ == "__main__":
    main()
