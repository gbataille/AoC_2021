from pathlib import Path


def main():
    root_path = Path(__file__).parent.parent
    for day in range(1, 26):
        day_path = root_path.joinpath(str(day))
        if not day_path.exists():
            day_path.mkdir()
            day_path.joinpath("__init__.py").write_text("from .main import *")
            day_path.joinpath("main.py").write_text("""
def main():
    pass
                """)


if __name__ == "__main__":
    main()
