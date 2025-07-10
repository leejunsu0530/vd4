from typing import Callable
from ..newtypes.format_str_tools import format_number, format_date, format_byte_str, format_time

from rich.console import Console, Group
from rich.table import Table, Column
import rich.box as box
from rich.style import Style
from rich.text import Text
from rich.panel import Panel
from rich.progress import (
    Progress,
    BarColumn,
    TextColumn,
    TimeElapsedColumn,
    TimeRemainingColumn,
    MofNCompleteColumn,
    SpinnerColumn)

# 여기서만 만들어짐
my_console = Console()


def progress_video_info(console: Console = None) -> Progress:
    return Progress(
        TextColumn(
            "[bright_cyan]{task.description}[/] "
            "[bold bright_magenta]{task.fields[channel_name]}[/] "
            "[bold #ff5c00]{task.fields[playlist_title]}[/] "
            "[bold #ffc100]{task.fields[video_title]}",
            justify="left"),
        # 현재 비디오 제목 표시
        BarColumn(
            style="dim cyan",  # 진행되지 않은(배경) 부분: 어두운 자홍
            complete_style="bright_cyan",  # 진행된(채워진) 부분: 시안
            finished_style="bold #03ff00",  # 작업 완료 시 전체 진행바: 밝은 연두색
            pulse_style="dim white"  # 펄스 애니메이션 시: 어두운 하얀색
        ),
        TextColumn("{task.percentage:>3.1f}%"),
        MofNCompleteColumn(),
        TimeElapsedColumn(),
        TimeRemainingColumn(),
        SpinnerColumn(),
        console=console)


def group_text_and_progress(text: Text = Text('Unknown'), border_style: str | Style = 'none',
                            progress: Progress = None) -> Group:
    panel = Panel(text, border_style=border_style)
    return Group(panel, progress)


def highlight_normal_text(msg: str):
    msg_text = Text.from_ansi(msg)

    # 1. 대괄호 안의 내용을 (대괄호 포함) magenta 색으로 강조
    msg_text.highlight_regex(r'\[[^\]]*\]', style="magenta")
    # 2. 숫자를 cyan 색으로 강조
    msg_text.highlight_regex(r'\d+', style="cyan")
    # 3. 작은따옴표로 둘러싸인 문자열을 lime 색으로 강조
    msg_text.highlight_regex(r"'[^']*'", style="#8aff67")
    # 4. 파일명 또는 파일 경로 형태의 문자를 orange 색으로 강조.
    # 이 정규식은 드라이브 문자, 콜론, 백슬래시로 시작하여,
    # 하나 이상의 디렉터리 이름이 백슬래시로 구분되고, 확장자를 포함한 파일 이름을 매칭합니다.
    msg_text.highlight_regex(
        r'[A-Za-z]:\\(?:[^\\\/:*?"<>|\r\n]+\\)*[^\\\/:*?"<>|\r\n]+\.[^\\\/:*?"<>|\r\n]+',
        style="orange1"
    )

    return msg_text


def hightlight_download_text(msg: str):
    msg_text = Text.from_ansi(msg)
    msg_text.highlight_regex(r'\[[^\]]*\]', style="magenta")  # []내부 처리

    # 1. 퍼센트 (예: "4.9%") → 시안색
    msg_text.highlight_regex(r'\b\d+(?:\.\d+)?%', style="cyan")

    # 2. 총 파일 용량 (예: "13.66MiB") → 초록색
    # "of ~" 부분까지 굳이 매칭할 필요가 없다면, 단순히 파일 크기 형태만 찾으면 됩니다.
    msg_text.highlight_regex(r'\b\d+(?:\.\d+)?[KMGTP]?i?B', style="green")

    # 3. 다운로드 속도 (예: "202.01KiB/s") → 노란색
    # 단순히 "KiB/s"까지 포함해서 하이라이트하고 싶다면 아래와 같이 쓰고,
    # '/s'는 제외하고 "202.01KiB"만 강조하고 싶다면 `(?=/s)` 형태의 룩어헤드를 사용하세요.
    msg_text.highlight_regex(r'\b\d+(?:\.\d+)?[KMGTP]?i?B/s', style="orange1")

    # 4. ETA (예: "ETA 00:44") → 빨강
    msg_text.highlight_regex(r'ETA\s+(?:\d{1,2}:\d{2}|Unknown)', style="red")

    # 5. 조각 정보 (예: "(frag 1/44)") → 주황색
    msg_text.highlight_regex(r'\(frag\s+\d+/\d+\)', style="yellow")

    return msg_text


class LoggerForRich:
    def __init__(self, print_info: bool | str = False, console=my_console):
        """print_info: 'only_download', false, true. 특정 시간보다 클때 출력 여부는 외부에서 결정"""
        self.print_info = print_info
        self.console = console

    def debug(self, msg):
        # For compatibility with youtube-dl, both debug and info are passed into debug
        # You can distinguish them by the prefix '[debug] '
        if msg.startswith('[debug] '):
            pass
        else:
            self.info(msg)

    @staticmethod
    def highlight_text(msg: str):
        if msg.startswith('[download]'):  # dl은 기본 색 그대로
            msg_text = hightlight_download_text(msg)
        else:  # 다운이 아니면
            msg_text = highlight_normal_text(msg)

        return msg_text

    def info(self, msg):
        if self.print_info is False:
            return None
        elif self.print_info == "only_download" and not msg.startswith("[download]"):
            return None

        msg_text = self.highlight_text(msg)
        self.console.print(msg_text)

    def warning(self, msg):
        msg = Text.from_ansi(msg)
        self.console.print(msg, style="bright_yellow")

    def error(self, msg):
        msg = Text.from_ansi(msg)
        self.console.print(msg, style="bright_red")


default_keys_to_show = [
    'title',
    ('upload_date', format_date),
    ('view_count', format_number),
    ('like_count', format_number),
    ('duration', format_time),
    ('filesize_approx', format_byte_str)]


def make_info_table(*, video_list: list[dict],
                    keys_to_show: list[str | tuple[str, Callable[[str | int | float], str]]] = None,
                    title: str | None = None, caption: str | None = None,
                    style: str | Style = "none", row_style: list[str | Style] = None,
                    print_: bool = True,
                    print_title_and_caption: bool = True,
                    show_lines: bool = True,
                    show_edges: bool = True,
                    restrict: Callable[[dict], bool] = None,
                    sort_by: tuple[str, bool] = None) -> Table:
    if not keys_to_show:
        keys_to_show = default_keys_to_show

    keys_to_show: list[tuple[str, Callable]] = [(key, lambda x: x) if isinstance(key, str)
                                                else key for key in keys_to_show]

    if sort_by:
        key_names: list[str] = [key if not key == sort_by[0] else f"[bold bright_magenta]{key}▲[/]" if not sort_by[
            1] else f"[bold bright_magenta]{key}▼[/]" for key, func in keys_to_show]
    else:
        key_names = [key for key, fuck in keys_to_show]
    headers = [Column(header="index", min_width=4)] + [Column(header=key, min_width=11) for key in key_names]
    table = Table(
        *headers,
        title=title if print_title_and_caption else None,
        caption=caption if print_title_and_caption else None,
        box=box.HORIZONTALS,
        show_lines=show_lines,
        show_edge=show_edges,
        style=style,
        title_style=style,
        caption_style=style
    )

    if not restrict:
        def restrict(dict_): return bool(dict_)
    if not row_style:
        row_style = ['none', 'dim']

    for idx, video in enumerate(video_list):
        lst = [idx + 1] + [func(video.get(key, "N/A")) for key, func in keys_to_show if restrict(video)]
        lst = map(str, lst)

        each_row_style = row_style[idx % len(row_style)]
        # 다운된거면 초록으로. 맴버십 전용일 때도 처리해야 함
        if video.get("availability") != "public":
            each_row_style += Style(bgcolor="red", strike=True)
        elif video.get('repeated'):
            each_row_style += Style(bgcolor="yellow")
        elif video.get('is_downloaded'):  # 퍼블릭이고 다운됐으면
            each_row_style += Style(bgcolor="green")

        table.add_row(*lst, style=each_row_style)  # 언페킹해서 *args에 리스트의 요소를 전달
    if print_:
        my_console.print(table)
    return table


if __name__ == '__main__':
    t = "[download]   4.9% of ~  13.66MiB at  202.01KiB/s ETA 00:44 (frag 1/44)"
    my_console.print(hightlight_download_text(t))
