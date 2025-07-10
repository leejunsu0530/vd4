import os
from copy import deepcopy
from rich.style import Style
from rich.traceback import install
from rich.progress import Progress
from rich.console import Console
from rich.live import Live
from rich.text import Text
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Callable, Literal, Any

from ..filemanage.filesave import write_dict_to_json, read_dict_from_json, date_for_log, write_str_to_file
from ..ydl.ydl_tools import bring_playlist_info, bring_video_info, change_video_dict_list, download_music, \
    download_video
from ..ydl.youtube_url_tools import find_id
from ..ydl.extcolors_from_thumbnail import thumbnail_selector, download_thumbnail, bring_major_colors
from ..newtypes.format_str_tools import format_byte_str

from .rich_VD4 import (my_console,
                       LoggerForRich,
                       progress_video_info,
                       default_keys_to_show,
                       make_info_table,
                       group_text_and_progress)
from .videos import Videos, MAJOR_KEYS, InfoDict

install(show_locals=True)


class VideosManager:
    def __init__(self, *playlist_videos_init: Videos | str,
                 parent_videos_dir: str = f"{os.getcwd()}\\downloads",
                 parent_file_dir: str = "",
                 additional_videos_dict_keys: dict[str, Callable[[InfoDict], Any]] = None,
                 video_force_update: bool | Literal["just_bring"] = False,
                 default_styles: list[str | Style] = None):
        """

        Args:
            playlist_videos_init: Videos로 각각의 링크 설정. 링크만 넣어도 됨
            parent_videos_dir: 비디오의 채널명 폴더가 위치할 위치
            parent_file_dir: 정보,에러,다운메니져 폴더가 위치할 위치. 기본은 비디오 채널명 폴더와 같은 위치
            additional_videos_dict_keys: 비디오스의 비디오 정보 딕셔너리에 추가할 키 값의 이름과 함수
            video_force_update: datas에 기록된 정보의 업데이트 여부. just_bring이면 정보를 기록하지 않음. true면 강제 업데이트, false면 최초 1회만 업데이트
            default_styles: 표들의 스타일이 지정되지 않았을 경우 이 스타일로 일괄 지정
            playlist_videos_init_kwargs: 리스트 말고 키(비디오 딕셔너리):벨류 형태로도 지정 가능
        """
        if not parent_file_dir:
            parent_file_dir = parent_videos_dir
        self.data_path = f"{parent_file_dir}\\Data"  # 이건 그대로
        self._thumbnail_path = f"{parent_file_dir}\\Thumbnails"
        self._video_path = f"{parent_videos_dir}\\Videos"
        self.error_path = f"{parent_file_dir}\\Errors"
        self._down_archive_path = f"{parent_file_dir}\\Download_archives"
        self.temp_path = f"{parent_videos_dir}\\Temp"

        self.videos_list: list[Videos] = []
        self.videos_to_download_list: list[Videos] = []

        self._channel_thumbnail_path = f"{self._thumbnail_path}\\Channel_thumbnails"
        self.channel_style_dict_path = self.data_path
        self.channel_style_dict_name = "channel_style.json"

        self.channel_style_dict: dict[str, list[str]] = read_dict_from_json(self.channel_style_dict_path,
                                                                            self.channel_style_dict_name)  # 없으면 빈 딕셔너리

        for videos in playlist_videos_init:
            if isinstance(videos, str):
                videos = Videos(playlist_url=videos)
            # 채널 정보 가져와서 영상 목록 뽑아내기
            playlist_url = videos.playlist_url
            playlist_info_dict = self.__bring_playlist_json(playlist_url, videos.update_playlist_data)
            channel_name = playlist_info_dict.get('channel')  # 채널로 할지 업로더로 할지?

            if not videos.list_all_videos:  # 기존 비디오스를 재사용하는 게 아니면
                entries = change_video_dict_list(playlist_info_dict)
                cannot_download: list[dict] = []
                # "private", "premium_only", "subscriber_only", "needs_auth", "unlisted" or "public"
                entries = [entry for entry in entries if videos.video_bring_restrict(entry)] # 조건에 맞지 않으면 리스트에서 제거
                cannot_download = [entry for entry in entries if entry.get("availability") in ("premium_only", "subscriber_only", "needs_auth", "unlisted")] # 이 중 하나면 cannot d에 넣기
                entries = [entry for entry in entries if not entry.get("availability") in ("premium_only", "subscriber_only", "needs_auth", "unlisted", "private") or "[Private video]" not in entry.get('title')] # 이 조건이 아니면 처리


                # 구체화 정보 가져와서 비디오스로 넣기
                videos.list_all_videos = self.__bring_detailed_info_list(playlist_url, playlist_info_dict.get('title'),
                                                                         channel_name,
                                                                         entries,
                                                                         video_force_update) + cannot_download
            else:
                my_console.print(f"{videos.pl_folder_name} Videos 가져옴")

            if not videos.pl_folder_name:  # 플리 이름 설정 따로 한게 아니면. 이건 일단 남겨놈
                videos.pl_folder_name = playlist_info_dict.get('title')
                videos.down_archive_name = f"{videos.pl_folder_name}.archive"

            # 경로설정
            videos.channel_name = channel_name
            if not videos.artist:
                videos.artist = channel_name
            if not videos.album:
                videos.album = videos.pl_folder_name
            videos.video_path = f"{self._video_path}\\{videos.pl_folder_name} ({channel_name})"
            videos.temp_path = f"{self.temp_path}\\{videos.pl_folder_name} ({channel_name})"
            videos.error_path = f"{self.error_path}\\{videos.pl_folder_name} ({channel_name})"
            videos.thumbnail_path = f"{self._thumbnail_path}\\videos\\{videos.pl_folder_name} ({channel_name})"
            # 채널이 아니라 영상 썸내일 경로임
            videos.down_archive_path = f"{self._down_archive_path}\\{channel_name}"  # da이름은 비디오스에서 지정
            videos.custom_da_path = f"{self._down_archive_path}\\Custom_down_archives"

            if not videos.styles:  # 비디오스에 유저가 정한 스타일이 없다면
                if default_styles:  # 유저가 지정한 게 최우선
                    videos.styles = default_styles  # 일괄 스타일임
                elif channel_name in self.channel_style_dict:  # 이미 이 채널의 스타일을 지정한 적이 있으면
                    videos.styles = self.channel_style_dict[channel_name]
                else:  # 처음 지정하는 채널이면
                    channel_url = playlist_info_dict.get('uploader_url') # 채널이면 업로더 url에 id 있음.
                    if channel_url is None:
                        channel_url = playlist_info_dict.get('channel_url') # 플리면 업로더 url이 없음. 이걸로

                    self.channel_style_dict[channel_name] = self.__get_thumbnail_colors(
                        channel_url,
                        self._channel_thumbnail_path, my_console)  # 색 반환
                    videos.styles = self.channel_style_dict[channel_name]

            if additional_videos_dict_keys:
                for key, value in additional_videos_dict_keys.items():
                    videos.additional_keys[key] = value

            videos.update()

            self.videos_list.append(deepcopy(videos))

        self.videos_to_download_list = self.videos_list  # 기본값으로는 바로 다운로드
        write_dict_to_json(self.channel_style_dict_name, self.channel_style_dict, self.channel_style_dict_path)

    def __bring_playlist_json(self, url: str, update_data: bool = True) -> dict:
        """갱신은 지속적으로 업로드되는 채널에서 가져오는 것이 아니면 필요 없음
        채널은 id찾아보고 없으면 가져오기
        """
        id_: str | None = find_id(url)

        playlist_data_path = f"{self.data_path}\\playlist_data"
        os.makedirs(playlist_data_path, exist_ok=True)  # 경로 없으면 오류남

        for pl_name in os.listdir(playlist_data_path):
            if id_ and id_ in pl_name:
                info_dict = read_dict_from_json(playlist_data_path, pl_name)
                if not update_data: # 업데이트 할거면(true면) break 안하고
                    break  # 파일 찾았고 갱신x면 이거 리턴. break되면 else 안됨

        else:  # for문에서 못찾으면 -> 파일에 없으면/업데이트 하는거면
            info_dict: dict = bring_playlist_info(url, LoggerForRich())

            playlist_data_name = f"{info_dict.get('title')} ({info_dict.get('uploader')}) [{info_dict.get('id')}]"
            # 업로더가 여럿일 때 어떻게 되는지 확인, 플리에서 업로더 확인
            write_dict_to_json(playlist_data_name, info_dict, playlist_data_path)

        return info_dict

    def __get_thumbnail_colors(self, channel_url: str, thumbnail_folder_path: str, console: Console) -> list[str]:
        """경로는 채널의 썸내일 폴더/플리 썸내일즈에 적음"""
        channel_info_dict = self.__bring_playlist_json(channel_url, False)
        channel_name = channel_info_dict.get('uploader')
        profile, channel_art = thumbnail_selector(channel_info_dict)
        colors = ["bright_white", "dim white"]
        if profile:  # 프로필 있으면
            error_code, message, saved_path = download_thumbnail(profile, f"{channel_name} (profile)",
                                                                 thumbnail_folder_path)
            console.print(message, highlight=True)
            if error_code == 0:  # 다운 성공이면
                colors = bring_major_colors(saved_path)

        if channel_art:  # 채널아트
            error_code, message, saved_path = download_thumbnail(channel_art, f"{channel_name} (channel_art)",
                                                                 thumbnail_folder_path)
            console.print(message, highlight=True)
            if error_code == 0 and not colors:  # 앞에서 못찾으면. 여기서도 못찾으면 기본으로 들어감
                colors = bring_major_colors(saved_path)

        return colors

    @staticmethod
    def __bring_detailed_info(entry: dict, video_data_path: str, error_path: str, playlist_title: str,
                              force_update: bool | str, console: Console = None) -> dict:
        title = entry.get('title')  # 포메팅 된 파일명
        info_dict: dict = read_dict_from_json(video_data_path, title)

        if not info_dict or force_update:  # force_update가 true거나 문자열이거나 infod가 없으면
            info_dict, dl_traceback = bring_video_info(entry.get('url'), playlist_title, LoggerForRich(console=console))
            if not dl_traceback and force_update != "just_bring":  # 정상이면(justbring면 위에서 가져온거 반환만 하고 저장x)
                write_dict_to_json(title, info_dict, video_data_path)
            else:  # dl에러가 있으면 정보는 entry에서 가져오기. 출력은 로거 포 리치에서
                info_dict = entry  # 불완전한 정보라도 들어는 감. 저장은 하지 않음
                error_message: dict = {
                    "title": f"{title}",
                    "availabitlty": f"{entry.get('availability')}",
                    "live_status": f"{entry.get('live_status')}",
                    "entry": entry,
                    "error": f"{dl_traceback}"
                }
                write_dict_to_json(f"[{date_for_log()}] {title}", error_message, parent_path=error_path)
        return info_dict

    def __bring_detailed_info_list(self, playlist_url: str, playlist_title: str, channel_name: str, entries: list[dict],
                                   force_update: bool | str = False) -> list[dict]:
        """업로더 이름에는 플리/채널명이 정보폴더 이름으로 들어감.
        개별 비디오는 채널명 폴더에 저장
        force_update가 just_bring면 파일로 저장x
        비디오가 최초공개일 때, 비공개일 때, 맨겐일 때 어떻게 되는지 확인하기"""
        video_data_path = f"{self.data_path}\\video_data\\{channel_name}"
        error_path = f"{self.error_path}\\data\\video_data\\{channel_name}"
        info_dict_list: list[dict | None] = []

        with ThreadPoolExecutor() as excutor, progress_video_info() as progress:
            progress.print(f"{playlist_url} 정보 가져오는 중...")  # 이건 프로그래스 도중이 아니라 잘 적용됨
            task_id = progress.add_task("비디오 정보 다운로드: ", total=len(entries),
                                        channel_name=channel_name,
                                        playlist_title=playlist_title,
                                        video_title="Unknown")
            future_to_entry = {
                excutor.submit(self.__bring_detailed_info, entry, video_data_path, error_path, playlist_title,
                               force_update, progress.console): entry
                for entry in entries
            }

            for future in as_completed(future_to_entry):
                entry = future_to_entry[future]
                try:
                    info_dict: dict = future.result()
                    if info_dict:
                        info_dict_list.append(info_dict)
                except Exception as e:
                    progress.log(f"[Error] while processing entry {entry.get('title')}: {e}")
                progress.update(task_id, advance=1, video_title=entry.get('title', 'Unknown'))

        return info_dict_list

    def set_to_download_list(self, *videos: Videos):
        self.videos_to_download_list = list(videos)

    def show_total_table(self, keys_to_show: list[MAJOR_KEYS | tuple[MAJOR_KEYS, Callable[[Any], str]]] = None,
                         show_lines: bool = False, show_edges: bool = True,
                         restrict: Callable[[InfoDict], bool] = None):
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
        다운아카 여부는 'is_downloaded'로 접근 가능"""
        if not keys_to_show:
            keys_to_show = ['playlist'] + default_keys_to_show
        videos_to_show = []
        caption_to_show = ""
        row_style = []
        sum_candl = 0
        sum_cantdl = 0
        sum_filesize = 0
        for videos in self.videos_to_download_list:
            # 비디오스에 있는 함수 참조, 맨 아래 캡션에 정보 모두 적기,row스타일 정하기
            videos.update()
            videos_to_show += videos.list_all_videos
            can_dl_len, cannot_dl_len, can_dl_filesize_sum = videos.calculate_table_info()
            sum_candl += can_dl_len
            sum_cantdl += cannot_dl_len
            sum_filesize += can_dl_filesize_sum
            caption_to_show += (f"[{videos.style}]다운로드 가능 영상 수: {can_dl_len}, "
                                f"다운로드 불가능 영상 수: {cannot_dl_len}, 총 용량: {format_byte_str(can_dl_filesize_sum)}[/]\n")
            row_style += (videos.styles[:3] * ((can_dl_len // 3) + 1))[:can_dl_len]

        caption_to_show += (f"전체 다운로드 가능 영상 수: {sum_candl}, 다운로드 불가능 영상 수: {sum_cantdl}, "
                            f"총 용량: {format_byte_str(sum_filesize)}")

        table = make_info_table(video_list=videos_to_show,
                                keys_to_show=keys_to_show,
                                title="Total Table",
                                caption=caption_to_show,
                                style='none',
                                row_style=row_style,
                                print_=False,
                                print_title_and_caption=True,
                                show_lines=show_lines,
                                show_edges=show_edges,
                                restrict=restrict,
                                sort_by=None)

        my_console.print(table)

    def show_total_info(self):
        for videos in self.videos_to_download_list:
            videos.info()

    def show_total_head(self, len_: int = 5):
        for videos in self.videos_to_download_list:
            videos.head(len_)

    class DLLogger(LoggerForRich):
        def __init__(self, live: Live, progress: Progress, videos: Videos):
            super().__init__(True, my_console)  # print_info는 상관x임. 밑에서 재정의해서
            self.live = live
            self.progress = progress
            self.videos = videos

        def info(self, msg: str):
            msg = msg.replace("\n", "")
            msg_text = self.highlight_text(msg)
            self.live.update(group_text_and_progress(msg_text, self.videos.style, self.progress))

        def error(self, msg):
            write_str_to_file(f"[{date_for_log()}] {self.videos.pl_folder_name}", msg, 
                              f"{self.videos.error_path}\\videos\\{self.videos.channel_name}")
            msg = Text.from_ansi(msg)
            self.console.print(msg, style="bright_red")

    def __download(self, type_: Literal["video", "music"],
                   concurrent_fragments: int,
                   embed_info_json: bool,
                   restrict_format: Literal["[height<=1080]", "[height<=720]", ""] = "",
                   ext: Literal["mkv", "mp4"] | str = "mkv") -> list[int]:
        total_videos: dict[str, str] = {}
        downloaded_videos: set[str] = set()
        for videos in self.videos_to_download_list:
            videos.update()
            [downloaded_videos.add(da) for da in videos.bring_da_list()]  # 이미 다운된 갯수 초기화
            total_videos.update({id_: title for id_, title in
                                 zip(videos.bring_list_from_key('id'), videos.bring_list_from_key('title'))})

        total_progress = progress_video_info()
        total_task = total_progress.add_task(
            description="영상 다운로드: " if type_ == "video" else "음악 다운로드: ",
            channel_name="Unknown",
            playlist_title="Unknown",
            video_title="Unknown",
            total=len(total_videos)
        )

        with Live(group_text_and_progress(progress=total_progress), console=my_console) as live:
            for videos in self.videos_to_download_list:
                os.makedirs(videos.down_archive_path, exist_ok=True)
                total_progress.update(total_task,
                                      channel_name=f"[{videos.style}]{videos.channel_name}[/]",
                                      playlist_title=videos.pl_folder_name)

                def my_hook(d: dict):
                    info_dict: dict = d["info_dict"] if "info_dict" in d else {}
                    if d['status'] == 'downloading':  # 다운중 상태 시 id로 이름 표시
                        # video_title = total_dict.get(info_dict.get('id', ''), "Unknown")
                        video_title = info_dict.get("title", "Unknown")
                        total_progress.update(total_task, video_title=video_title)
                    elif d['status'] == 'finished':
                        id_ = info_dict.get('id')
                        if id_:
                            downloaded_videos.add(id_)  # 다운 진도는 영상과 소리를 따로 세는 것을 막기 위해 id 수로 업데이트
                        total_progress.update(total_task, completed=len(downloaded_videos))

                url_list = videos.bring_list_from_key('webpage_url')
                skip_list: list[list[str] | None] = [
                    ['dash'] if 'm3u8' in protocol else ['m3u8'] if 'dash' in protocol else ['dash', 'm3u8'] for
                    protocol in videos.bring_list_from_key('protocol')]
                chapters_list: list[list[dict]] = videos.bring_list_from_key('chapters')

                if type_ == "video":
                    error_codes = [download_video(video_path=videos.video_path,
                                                  urls=url,
                                                  inner_folder=videos.inner_split_by,
                                                  thumbnail_path=videos.thumbnail_path,
                                                  download_archive_path=videos.down_archive_path,
                                                  download_archive_name=videos.down_archive_name,
                                                  temp_path=videos.temp_path,
                                                  split_chapters=videos.split_chapter,
                                                  restrict_format=restrict_format,
                                                  ext=ext,
                                                  progress_hook=my_hook,
                                                  concurrent_fragments=concurrent_fragments,
                                                  embed_info_json=embed_info_json,
                                                  skip_hls_or_dash=skip,
                                                  ignore_errors='only_download',
                                                  logger=self.DLLogger(live, total_progress, videos),
                                                  chapter=chapters)
                                   for url, skip, chapters in zip(url_list, skip_list, chapters_list)]

                elif type_ == "music":
                    error_codes = [download_music(music_path=videos.video_path,
                                                  urls=url,
                                                  inner_folder=videos.inner_split_by,
                                                  thumbnail_path=videos.thumbnail_path,
                                                  download_archive_path=videos.down_archive_path,
                                                  download_archive_name=videos.down_archive_name,
                                                  temp_path=videos.temp_path,
                                                  split_chapters=videos.split_chapter if chapters else False,
                                                  album=videos.album,
                                                  artist=videos.artist,
                                                  progress_hook=my_hook,
                                                  concurrent_fragments=concurrent_fragments,
                                                  embed_info_json=embed_info_json,
                                                  skip_hls_or_dash=skip,
                                                  ignore_errors='only_download',
                                                  logger=self.DLLogger(live, total_progress, videos),
                                                  chapter=chapters)
                                   for url, skip, chapters in zip(url_list, skip_list, chapters_list)]
        
        for temp_folder in os.listdir(self.temp_path):
            dir_path = f"{self.temp_path}\\{temp_folder}"
            if os.path.isdir(dir_path) and not os.listdir(dir_path):
                os.rmdir(dir_path)
        
        return error_codes

    def download_as_video(self, restrict_format: Literal["[height<=1080]", "[height<=720]", ""] = "[height<=1080]",
                          concurrent_fragments: int = min(32, (os.cpu_count() or 1) + 4),
                          embed_info_json: bool = False, ext: Literal["mkv", "mp4"] | str = 'mkv') -> list[int]:
        error_codes = self.__download("video", concurrent_fragments, embed_info_json, restrict_format, ext)
        return error_codes

    def download_as_music(self, concurrent_fragments: int = min(32, (os.cpu_count() or 1) + 4),
                          embed_info_json: bool = False):
        error_codes = self.__download("music", concurrent_fragments, embed_info_json)
        return error_codes
