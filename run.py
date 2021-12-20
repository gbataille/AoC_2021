import importlib
import sys


def run():
    if len(sys.argv) != 2:
        print(
            "The script needs to be launched with the day number as a parameter"
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

    try:
        day_module = importlib.import_module(str(day_num))
        day_module.main()
    except (ImportError, KeyError):
        print(f"Could not import the main program for day {day_num}")
        sys.exit(103)


if __name__ == "__main__":
    run()
