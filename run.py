import importlib
import sys


def run():
    if len(sys.argv) != 3:
        print(
            "The script needs to be launched with the day number as a parameter and the part # (1 or 2)"
        )
        sys.exit(100)

    day_num = 0
    try:
        day_num = int(sys.argv[1])
    except ValueError:
        print(
            "The script needs to be launched with the day number as an int parameter"
        )
        sys.exit(101)

    if day_num > 25 or day_num < 1:
        print(
            "The script needs to be launched with the day number between 1 and 25"
        )
        sys.exit(102)

    part_num = 0
    try:
        part_num = int(sys.argv[2])
    except ValueError:
        print(
            "The script needs to be launched with the part number as an int parameter"
        )
        sys.exit(104)

    if part_num > 2 or part_num < 1:
        print(
            "The script needs to be launched with the part number between 1 and 2"
        )
        sys.exit(105)

    day_module = importlib.import_module(str(day_num))
    day_module.main(day_num, part_num)
    # try:
    #     day_module = importlib.import_module(str(day_num))
    #     day_module.main(day_num, part_num)
    # except (ImportError, KeyError):
    #     print(
    #         f"Could not import the main program for day {day_num} and part {part_num}"
    #     )
    #     sys.exit(103)


if __name__ == "__main__":
    run()