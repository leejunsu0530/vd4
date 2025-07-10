import sys
from typing import Any

from rich.prompt import Prompt
from rich.style import Style


def ask_continue(msg: str) -> None:
    if Prompt.ask(msg, choices=["y", "n"], default="n") == "n":
        sys.exit()


def ask_y_or_n(msg: str, default: str = "n") -> bool:
    if ask_choice(msg, ["y", "n"], default) == "y":
        return True
    else:
        return False


def ask_choice(msg: str, choice: list[Any] = None, default: str = "") -> Any:
    choice: list[str] = [str(c) for c in choice] if choice else None
    if not default:
        return Prompt.ask(msg, choices=choice)
    else:
        return Prompt.ask(msg, choices=choice, default=default)


def ask_choice_num(
    msg: str,
    choice: list[Any] = None,
    default: int = None,
    styles: list[str | Style] = None,
) -> int:
    """문자열 리스트로 제공하면 번호 매겨서 선택지 제공
    기본 styles = ["red", "blue", "green", "yellow", "magenta", "cyan", "bright_magenta", "bright_cyan"]
    """
    if not styles:
        styles = [
            "red",
            "blue",
            "green",
            "yellow",
            "magenta",
            "cyan",
            "bright_magenta",
            "bright_cyan",
        ]
    choice: list[str] = [str(c) for c in choice] if choice else None
    choice_str = "/".join(
        [f"[{styles[idx % len(styles)]}]{idx}:{c}[/]" for idx, c in enumerate(choice)]
    )
    if not default:
        return int(
            Prompt.ask(
                f"{msg} [{choice_str}]", choices=[f"{i}" for i in range(len(choice))]
            )
        )
    else:
        return int(
            Prompt.ask(
                f"{msg} [{choice_str}]",
                choices=[f"{i}" for i in range(len(choice))],
                default=default,
            )
        )


if __name__ == "__main__":
    print(ask_choice_num("안녕하세요", ["a", "b", "c"]))
