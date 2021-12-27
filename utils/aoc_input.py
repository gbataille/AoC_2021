from pathlib import Path

import requests


def get_input(day_num: int) -> Path:
    INPUT_URL = f'https://adventofcode.com/2021/day/{day_num}/input'
    SESSION = '53616c7465645f5f5387d599bad2dff087267620b3a35300383c6d799c1ceb0b362634d72dc03490164c83ac70ecbbce'
    input_file_path = Path(__file__).parent.parent.joinpath(str(day_num), 'input.txt')
    if not input_file_path.exists():
        input_data = requests.get(INPUT_URL, cookies={'session': SESSION}).text
        input_file_path.write_text(input_data)
    return input_file_path
