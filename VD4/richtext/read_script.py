from rich.syntax import Syntax
from rich.console import Console
import sys
import os


def print_code(console: Console = None, line_range: tuple[int, int] = None, line_numbers: bool = True):
    path = os.path.abspath(sys.argv[0])

    syntax = Syntax.from_path(path, line_numbers=line_numbers, encoding='utf-8', line_range=line_range)
    if not console:
        console = Console()
    console.print(syntax)


if __name__ == '__main__':
    print_code()
    print("진행됨")
