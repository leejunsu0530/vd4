from ..newtypes import format_str_tools


def filename(input_string: str) -> str:
    return format_str_tools.format_filename(input_string)


def number(num: int | str) -> str:
    return format_str_tools.format_number(num)


def date(date_: int | str, type_: str = "%y.%m.%d") -> str | None:
    return format_str_tools.format_date(date_, type_)


def time(seconds: float | int | str, return_int: bool = True) -> str:
    return format_str_tools.format_time(seconds, return_int)


def byte(byte_: int | str, round_: int = 2) -> str:
    return format_str_tools.format_byte_str(byte_, round_)
