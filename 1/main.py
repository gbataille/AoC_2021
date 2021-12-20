from pathlib import Path


def main():
    input_path = Path(__file__).parent.joinpath('input1.txt')
    input_data = input_path.read_text()

    cnt = 0
    lines = list(map(int, input_data.strip().split('\n')))
    for idx in range(len(lines) - 3):
        after = lines[idx + 1] + lines[idx + 2] + lines[idx + 3]
        before = lines[idx] + lines[idx + 1] + lines[idx + 2]
        if after > before:
            cnt += 1

    print(cnt)
