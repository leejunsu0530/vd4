from typing import Callable, Literal, TypedDict, Any
from copy import deepcopy
from rich.style import Style
from rich.panel import Panel

from ..filemanage.filesave import read_str_from_file
from ..filemanage.bring_path import bring_file_name_no_ext
from ..newtypes.format_str_tools import format_byte_str, format_date
from ..newtypes.new_sum import new_sum
from ..newtypes.dict_list import bring_key_list, dict_set_inter, dict_set_diff, dict_set_union

from .rich_VD4 import make_info_table, Table, my_console

CODE_FILE_PATH = bring_file_name_no_ext()

MAJOR_KEYS = Literal[
                 "id", "title", "uploader", "channel", "playlist", "upload_date", "duration", "view_count",
                 "like_count", "live_status", "availability", "filesize_approx"] | str


class InfoDict(TypedDict, total=False):
    id: str
    title: str
    webpage_url: str
    url: str
    description: str
    uploader: str
    channel: str
    channel_id: str
    playlist: str
    upload_date: str
    duration: int | float
    duration_string: str
    view_count: int
    like_count: int
    live_status: Literal["not_live", "is_live", "is_upcoming", "was_live", "post_live"]
    availability: Literal["private", "premium_only", "subscriber_only", "needs_auth", "unlisted", "public"]
    filesize_approx: int | float
    filesize: int | float
    chapters: list[dict[str, int]]
    comments: list[dict]
    album: str
    artist: str


def sum_videos(*videos: "Videos", pl_folder_name: str = "", artist_name: str = "", album_title: str = "",
               style: Style | str = None) -> "Videos":
    """커스텀 경로의 비디오스 객체를 반환"""
    new_videos: Videos = new_sum(*videos)
    if pl_folder_name:
        new_videos.pl_folder_name = pl_folder_name
    if artist_name:
        new_videos.artist = artist_name
    if album_title:
        new_videos.album = album_title
    if style:
        new_videos.style = style
    new_videos.down_archive_name = None
    new_videos.update()

    return new_videos


def path_styler(path: str):
    return path.replace('\\', '/').replace('/', '[bold #ff5c00]/[/]')


class Videos:
    def __init__(self, playlist_url: str,
                 video_bring_restrict: Callable[[InfoDict], bool] = None,
                 playlist_title: str = "",
                 inner_folder_split: Literal["%(upload_date>%Y.%m)s", "%(uploader)s", "%(playlist)s"] | str = "",
                 styles: list[Style | str] | Style | str = None,
                 split_chapter: bool = False,
                 update_playlist_data: bool = True, custom_da: bool = False,
                 artist_name: str = "", album_title: str = ""):

        """
        비디오스 객체의 da_name이 'custom'이거나 none이면 커스텀 경로로 지정됨
        Args:
            playlist_url: 메니져에서 읽어오고 구체화 시에 사용됨
            video_bring_restrict: 가져올 개별 영상 목록을 지정하는 함수. 기본적으로는 전부 가져옴.
            playlist_title: 하나의 플레이리스트를 저장할 폴더명. 플레이리스트명으로 자동지정됨.
            inner_folder_split: 내부에 폴더로 나눔. '%(upload_date>%Y.%m)s' (날짜 월별로 묶기), '%(uploader)s' (업로더 채널명으로 묶기), '%(playlist)s' (플레이리스트 이름으로 묶기). 자세한 건 https://github.com/yt-dlp/yt-dlp?tab=readme-ov-file#output-template 의 출력 탬플릿 참조.
            styles: 첫번째 스타일은 표나 정보 등에 사용됨. 스타일 리스트나 스타일, 문자열로 지정가능. 기본적으로는 채널 썸내일에서 주요 색 가져옴. 자세한 건 https://rich.readthedocs.io/en/stable/style.html 참조
            split_chapter: 챕터별로 영상을 분리할지 여부.
            update_playlist_data: 플리 정보 새로 가져올지 파일에서 읽을지 여부. 지속적인 업로드시 변경해야 갱신됨
            custom_da: 다운로드 아카이브를 커스텀 경로에 저장할지 여부
            artist_name: 작곡가로 들어갈 이름. 기본적으로 채널명으로 자동지정됨.
            album_title: 엘범 제목. 기본적으로 플리명으로 자동지정됨.

        """
        # 메니져가 정의해주는 변수
        self.down_archive_path = ""
        self.channel_name = ""
        self.video_path = ""
        self.thumbnail_path = ""
        self.error_path = ""
        self.temp_path = ""
        self.custom_da_path = ""

        def check_is_repeated(video_dict: dict) -> bool:
            # 기존은 list_not_repeated 정의하고 for문 돌면서 넣은 뒤 이 리스트에 있으면 중복에 넣고 이 리스트로 다운 가능/불가능 정했었음.
            if video_dict.get('id') in bring_key_list(self.list_repeated, 'id'):  # 중복이면
                return True
            else:  # 중복 아니면
                return False

        self.additional_keys: dict[str, Callable[[dict], Any]] = {
            'repeated': check_is_repeated,  # 중복 분류는 구현이 어려움. 중복 확인만 하기
            'is_downloaded': lambda video_dict: True if video_dict.get("id") in self.bring_da_list() else False,
        }

        self.pl_folder_name = playlist_title
        self.playlist_url = playlist_url
        self.video_bring_restrict = video_bring_restrict if video_bring_restrict else lambda dict_: True
        self.update_playlist_data = update_playlist_data
        self.inner_split_by = inner_folder_split
        self.split_chapter = split_chapter
        self.custom_da = custom_da
        self.artist = artist_name
        self.album = album_title

        self.list_all_videos: list[dict] = []
        self.list_can_download: list[dict] = []
        self.list_cannot_download: list[dict] = []  # 비공개, 맴버십 온리, 최초공개 등.
        self.list_repeated: list[dict] = []  # 중복 id

        self.sort_by: tuple[str, bool] = ("upload_date", False)  # 기본으로 업로드 날짜, 내림차순 정렬
        if isinstance(styles, list) or styles is None:
            self.styles:list[str | Style] | None = styles  # none이나 리스트면 그대로
        else:  # 아니면 리스트로 바꿈
            if isinstance(styles, Style):
                self.styles = [styles, Style(dim=True) + styles]
            else:  # 문자열이면
                self.styles = [styles, Style(dim=True) + Style.parse(styles)]

        self.style: Style | str = self.styles[0] if self.styles else 'none'

        self.down_archive_name = f"{self.pl_folder_name}.archive"  # 아카이브 경로/채널명/플리명.archive

    def override_list(self, videos: "Videos") -> "Videos":
        """다른 속성은 유지하고 리스트만 덮어씌움"""
        self.list_all_videos = videos.list_all_videos
        return self

    def change_value(self,
                 playlist_title: str = "",
                 inner_folder_split: Literal["%(upload_date>%Y.%m)s", "%(uploader)s", "%(playlist)s"] | str = "",
                 styles: list[Style | str] | Style | str = None,
                 split_chapter: bool = False,
                 custom_da: bool = False,
                 artist_name: str = "", album_title: str = "") -> "Videos":
        if playlist_title:
            self.pl_folder_name = playlist_title
        if inner_folder_split:
            self.inner_split_by = inner_folder_split
        if styles:
            self.styles = styles
        if split_chapter:
            self.split_chapter = split_chapter
        if custom_da:
            self.custom_da = custom_da
        if artist_name:
            self.artist = artist_name
        if album_title:
            self.album = album_title
        return self

    def update(self) -> "Videos":
        """영상 순서 정렬, 스타일 객체 일괄화, 다운로드 리스트 키를 딕셔너리에 추가, 다운로드 경로가 커스텀이면 커스텀 경로로 수정, 중복시 중복 리스트로 이동, 다운로드 가능/불가능 구별
        availability에는 "private", "premium_only", "subscriber_only", "needs_auth", "unlisted" or "public" 존재 가능.
        이 중 다운로드 가능은 public뿐
        """
        # da 커스텀 체크는 da가져오기에서 처리
        # 스타일이 문자열이면 스타일 객체로
        self.styles = [Style.parse(style) if isinstance(style, str) else style for style in self.styles]
        if len(self.styles) == 1:
            self.styles = [self.styles[0], self.styles[0] + Style(dim=True)]
        self.style = self.styles[0]

        self.sort(self.sort_by[0], self.sort_by[1])  # 이건 전체만 sort하면 됨

        list_not_repeated = []
        for video in self.list_all_videos:
            if video.get('id') not in list_not_repeated:  # 이 키가 처음이면
                list_not_repeated.append(video)
            else:  # 이 키가 중복이면
                self.list_repeated.append(video)

            for key, func in self.additional_keys.items():
                video[key] = func(video)  # 기본적으로 중복 여부 체크와 다운여부 체크를 함. 여기서 중복일 시 repeated를 true로 설정

        self.list_can_download = [video for video in self.list_all_videos if
                                  video.get("availability") == "public" and not video.get('repeated')]
        self.list_cannot_download = [video for video in self.list_all_videos if
                                     video.get("availability") != "public" and not video.get('repeated')]
        # self.list_repeated = [video for video in self.list_all_videos if video.get('repeated')]  # 위에서 넣음
        return self

    def info(self, print_: bool = True) -> Panel:
        self.update()
        styles_str = ""
        for idx, style in enumerate(self.styles):
            styles_str += f"[{style}]{style}[/]"
            if idx != len(self.styles) - 1:
                styles_str += ", "

        path_info = self.video_path + ("" if not self.inner_split_by else f"/{self.inner_split_by}\n")
        can_dl_len, cannot_dl_len, can_dl_filesize_sum = self.calculate_table_info()

        info: Panel = Panel(f"[{self.style}]채널명[/]: {self.channel_name}\n"
                            f"[{self.style}]폴더명(플리명)[/]: {self.pl_folder_name}\n"
                            # f"[{self.style}]url[/]: {self.playlist_url}\n"
                            f"[{self.style}]영상 저장 경로[/]: {path_styler(path_info)}\n"
                            # f"[{self.style}]임시 저장 경로[/]: {path_styler(self.temp_path)}\n"
                            # f"[{self.style}]썸내일 저장 경로[/]: {path_styler(self.thumbnail_path)}\n"
                            # f"[{self.style}]오류 경로[/]: {path_styler(self.error_path)}\n"
                            f"[{self.style}]다운아카이브 경로[/]: {path_styler(self.down_archive_path)}\n"
                            f"[{self.style}]다운아카이브 이름[/]: {self.down_archive_name}\n"
                            f"[{self.style}]스타일[/]: {styles_str}\n"
                            f"[{self.style}]다운로드 가능 영상 수[/]: {can_dl_len}, "
                            f"[{self.style}]다운로드 불가능 영상 수[/]: {cannot_dl_len}, "
                            f"[{self.style}]총 용량[/]: {format_byte_str(can_dl_filesize_sum)}\n"
                            f"[{self.style}]아티스트명[/]: {self.artist} / [{self.style}]엘범명[/]: {self.album}",
                            border_style=self.style)
        if print_:
            my_console.print(info, highlight=False)
        return info

    def head(self, len_: int = 5, print_: bool = True) -> Table:
        self.update()
        table = make_info_table(video_list=self.list_all_videos[:len_],
                                keys_to_show=['title', ('upload_date', format_date), 'duration_string'],
                                title=self.pl_folder_name,
                                caption=None,
                                style=self.style,
                                row_style=self.styles[:3],
                                print_=print_,
                                print_title_and_caption=True,
                                show_lines=False,
                                show_edges=False,
                                restrict=None,
                                sort_by=self.sort_by)
        return table

    def bring_list_from_key(self, key: MAJOR_KEYS) -> list[int | str | float | list | dict]:
        """해당하는 키값의 리스트 반환"""
        return bring_key_list(self.list_can_download, key)

    def sort(self, order: MAJOR_KEYS, reverse: bool = False) -> "Videos":
        """
        키값으로 정렬
        Args:
            order: 정렬할 기준 키값(upload_date, filesize_approx...),
            reverse: 오름차순 여부
        """
        self.sort_by = order, reverse
        list_cannot_sort = [video for video in self.list_all_videos if video.get(order) is None]  # none이면 빠지겠지
        list_can_sort = [video for video in self.list_all_videos if video.get(order) is not None]
        # 정렬할 키값이 없는거는 다른 리스트에 빼놓고 분류 후 합친다
        list_can_sort.sort(key=lambda dict_: dict_.get(order), reverse=reverse)  # 분류 불가만 했으므로 기본값 필요 x
        self.list_all_videos = list_can_sort + list_cannot_sort
        # self.update()  # 이건 아마 다른 함수에서 쓸때 처리해서 상관 없을 듯

    def cut(self, start: int = None, end: int = None, 
            pop_from_original: bool = True) -> "Videos":
        """
        파이썬의 슬라이싱과 같은 구조
        Args:
            start: 시작 위치
            end: 끝 위치
            percent: 전체에 대한 퍼센트로 따질지 여부. 기본이라면 갯수로 따짐
            pop_from_original: true면 원본을 필터링함, false면 필터링한 걸 반환
            new_pl_folder_name: 폴더명을 바꿀거면 설정

        """
        new_videos: Videos = deepcopy(self)

        new_videos.list_all_videos = new_videos.list_all_videos[start:end]
        if pop_from_original:
            self.override_list(self - new_videos)  # 원본에서 뺌. 이게 false면 원본은 그대로임

        new_videos.update()

        return new_videos

    def filtering(self, opt: Callable[[InfoDict], bool], pop_from_original: bool = True) -> "Videos":
        """
        조건에 맞는 것만 남겨서 반환하거나 원본을 변경
        Args:
            opt: lambda info_dict: '엘든링' in info_dict['name'] or '엘든 링' in info_dict['name']
            pop_from_original: true면 원본을 변경, false면 변경 안함. 둘 다 수정된거 반환함.
            new_pl_folder_name: 하위 폴더 이름 지정
        """
        new_videos: Videos = deepcopy(self)

        new_videos.list_all_videos = [new_videos.list_all_videos[idx] for idx, video_dict in
                                      enumerate(new_videos.list_all_videos) if opt(video_dict)]
        if pop_from_original:
            self.override_list(self - new_videos)  # 원본에서 뺌. 이게 false면 원본은 그대로임

        new_videos.update()

        return new_videos

    def filtering_keyward(self, *keywards: str, find_in_descriptions: bool = False,
                          find_in_comments: bool = False,
                          pop_from_original: bool = True) -> "Videos":
        """제목, 설명, (댓글)에서 찾기"""
        new_videos_to_filter: Videos = deepcopy(self)
        new_videos_to_return: Videos = deepcopy(self)
        new_videos_to_return.list_all_videos = []

        for keyward in keywards:
            new_videos_to_return.list_all_videos += new_videos_to_filter.filtering(
                lambda dict_,keyward=keyward: keyward in dict_["title"]).list_all_videos
            new_videos_to_return.list_all_videos += new_videos_to_filter.filtering(
                lambda dict_,keyward=keyward: keyward in dict_["description"] and find_in_descriptions).list_all_videos

            def find_in_c(info_dict: dict, keyward=keyward) -> bool:
                if not find_in_comments or not info_dict.get('comments'):
                    return False
                else:
                    comment_text = "".join([(c.get('text')) for c in info_dict.get('comments')])
                    return keyward in comment_text

            new_videos_to_return.list_all_videos += new_videos_to_filter.filtering(find_in_c).list_all_videos

        if pop_from_original:
            self.override_list(self - new_videos_to_return)
            # 원본에서 뺌. 이게 false면 원본은 그대로임

        return new_videos_to_return

    def bring_da_list(self) -> list[str]:
        """파일 읽어오기,, 딕셔너리에 is_da넣기,
        비디오스의 da 이름이 custom이면 경로를 커스텀 경로로, 이름을 업로더_파일명.archive로"""
        if self.down_archive_name == 'custom' or self.down_archive_name is None or self.custom_da:
            self.down_archive_path = self.custom_da_path
            self.down_archive_name = f"{self.channel_name}_{CODE_FILE_PATH}.archive"

        down_archive = read_str_from_file(f"{self.down_archive_path}\\{self.down_archive_name}")
        dl_id_list = [line.split()[1] for line in down_archive.split("\n") if line] if down_archive else []
        # if 안붙이면 마지막줄에 공백에서 오류

        return dl_id_list

    def show_table(self, keys_to_show: list[MAJOR_KEYS | tuple[MAJOR_KEYS, Callable[[str | int | float | Any], str]]] = None,
                   show_lines: bool = False,
                   show_edges: bool = True,
                   print_: bool = True, restrict: Callable[[InfoDict], bool] = None) -> Table:
        """
        keys_to_show는 키 이름 또는 (키 이름,값에 적용할 함수명) 리스트임. 키가 없을 경우 Unknown반환.
        기본 keys_to_show:
        keys_to_show = [
            'title',
            ('upload_date', format_date),
            ('view_count', format_number),
            ('like_count', format_number),
            ('duration', format_time),
            ('filesize_approx', format_byte_str)]
        restrict: 예를 들어 lambda dict_: dict.get('availability') == 'public'
        다운아카 여부는 'is_downloaded'로 접근 가능
        Return:
            table
            """
        self.update()
        title = self.pl_folder_name
        can_dl_len, cannot_dl_len, can_dl_filesize_sum = self.calculate_table_info()
        caption = (f"[{self.style}]다운로드 가능 영상 수[/]: {can_dl_len}, "
                   f"[{self.style}]다운로드 불가능 영상 수[/]: {cannot_dl_len}, "
                   f"[{self.style}]총 용량[/]: {format_byte_str(can_dl_filesize_sum)}")

        table = make_info_table(video_list=self.list_all_videos,
                                keys_to_show=keys_to_show,
                                title=title if print_ else None,
                                caption=caption if print_ else None,
                                style=self.style,
                                row_style=self.styles[:3],
                                print_=print_,
                                print_title_and_caption=True,
                                show_lines=show_lines,
                                show_edges=show_edges,
                                restrict=restrict,
                                sort_by=self.sort_by)
        # print_ 안하면 제목도 안나옴
        return table

    def calculate_table_info(self) -> tuple[int, int, int]:
        """
        Return:
            can_dl_len, cannot_dl_len, can_dl_filesize_sum(not formated)
            """
        can_dl_len = len(self.list_can_download)
        cannot_dl_len = len(self.list_cannot_download)
        can_dl_filesize_sum = sum([video_dict.get("filesize_approx", 0) for video_dict in self.list_can_download if
                                   isinstance(video_dict.get("filesize_approx", 0), int)])

        return can_dl_len, cannot_dl_len, can_dl_filesize_sum

    # 연산(합,차,교집합)함수: 집합으로 연산한 후 순서 재정렬해야 함. 필터가 클래스를 반환하는지 리스트를 반환하는지에 따라 이거에 클래스를 넣을지 리스트를 넣을지 달라짐.
    def __add__(self, other: "Videos") -> "Videos":
        # 이건 따로 역방향 연산을 정의하지 않으면 a+b는 a에서, b+a는 b에서 처리됨
        # __iadd__는 +=연산으로, 이거 하면 새 객체 반환임.
        new_videos = deepcopy(self)
        new_videos.list_all_videos = dict_set_union(new_videos.list_all_videos, other.list_all_videos)
        new_videos.update()
        return new_videos

    def __sub__(self, other: "Videos") -> "Videos":
        new_videos = deepcopy(self)
        new_videos.list_all_videos = dict_set_diff(new_videos.list_all_videos, other.list_all_videos)
        new_videos.update()
        return new_videos

    def __and__(self, other: "Videos") -> "Videos":
        """교집합: &메소드 사용"""
        new_videos = deepcopy(self)
        new_videos.list_all_videos = dict_set_inter(new_videos.list_all_videos, other.list_all_videos)
        new_videos.update()
        return new_videos

    def __str__(self) -> Panel:
        return self.info(False)

    def __repr__(self) -> Panel:
        return self.info(False)
