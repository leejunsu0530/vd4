from datetime import datetime


def _try_and_return(func):
    """성공하면 수정해서, 실패하면 그대로"""

    def wrapper(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            return result
        except (TypeError, ValueError):
            return args

    return wrapper


def format_filename(input_string: str) -> str:
    invalid_to_fullwidth: dict[str, str] = {
        '<': '＜',  # U+FF1C
        '>': '＞',  # U+FF1E
        ':': '：',  # U+FF1A
        '"': '＂',  # U+FF02
        '/': '／',  # U+FF0F
        '\\': '＼',  # U+FF3C
        '|': '｜',  # U+FF5C
        '?': '？',  # U+FF1F
        '*': '＊',  # U+FF0A
    }

    # Replace each invalid character with its fullwidth equivalent
    for char, fullwidth_char in invalid_to_fullwidth.items():
        input_string = input_string.replace(char, fullwidth_char)

    return input_string


@_try_and_return
def format_number(num: int | str) -> str:
    num = int(num)
    """4자리마다 ,로 끊음"""
    num_str = str(num)[::-1]  # Reverse the string
    grouped = ",".join(num_str[i:i + 4] for i in range(0, len(num_str), 4))
    return grouped[::-1]  # Reverse it back


@_try_and_return
def format_date(date: int | str, type_: str = "%y.%m.%d") -> str | None:
    """yyyymmdd("%Y%m%d") -> yy.mm.dd("%y.%m.%d")"""
    date_obj = datetime.strptime(str(date), "%Y%m%d")
    return date_obj.strftime(type_)


@_try_and_return
def format_time(seconds: float | int | str, return_int: bool = True) -> str:
    seconds = float(seconds)
    minutes, sec = divmod(seconds, 60)  # 초를 분과 초로 변환
    hours, minutes = divmod(minutes, 60)  # 분을 시와 분으로 변환
    if return_int:
        sec = round(sec)
        if hours >= 1:
            return f"{int(hours):02}:{int(minutes):02}:{sec:02}"  # hh:mm:ss.SS
        else:
            return f"{int(minutes):02}:{sec:02}"  # mm:ss.SS
    else:
        if hours >= 1:
            return f"{int(hours):02}:{int(minutes):02}:{sec:05.2f}"  # hh:mm:ss.SS
        else:
            return f"{int(minutes):02}:{sec:05.2f}"  # mm:ss.SS


def _format_byte(byte: int | str, round_: int = 4) -> tuple[float, float, float]:
    """mb, gb 튜플 반환"""
    byte = int(byte)
    kb = round(byte / 1024, round_)
    mb = round(byte / (1024 ** 2), round_)
    gb = round(byte / (1024 ** 3), round_)
    return kb, mb, gb


@_try_and_return
def format_byte_str(byte: int | str, round_: int = 2) -> str:
    kb, mb, gb = _format_byte(byte, round_)
    if gb >= 1:
        return f"{gb} GiB"
    elif mb >= 1:
        return f"{mb} MiB"
    else:
        return f"{kb} KiB"


if __name__ == '__main__':
    print(format_byte_str(10000000))
    # print(format_number("10000000000a"))
