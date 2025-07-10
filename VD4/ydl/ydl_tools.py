import os
import traceback
import yt_dlp
from typing import Callable
from ..newtypes.format_str_tools import format_filename
from .timestamp_parser import parse_chapters


class ExtractChapter(yt_dlp.postprocessor.PostProcessor):
    """
        "pre_process" (after video extraction)
        "after_filter" (after video passes filter)
        "video" (after --format; before --print/--output)
        "before_dl" (before each video download)
        "post_process" (after each video download; default)
        "after_move" (after moving the video file to its final location)
        "after_video" (after downloading and processing all formats of a video)
        "playlist" (at end of playlist)
        """

    # ℹ️ See help(yt_dlp.postprocessor.PostProcessor)
    def run(self, info: dict):
        if info.get("chapters"):
            self.to_screen(f"Already have chapters:{[chapter.get('title') for chapter in info.get('chapters')]}")
            return [], info

        video_duration = info.get('duration', None)

        # 설명란에서 추가
        description: str = info.get('description')
        chapters = parse_chapters(description, video_duration)
        info['meta_comment'] = description  # 원본을 코멘트에 추가. 밑에 챕터 나오면 그걸로 덮어씌워짐
        if chapters and len(chapters) >= 3:  # 설명란에 챕터가 있다면 그건 진짜 챕터니까 갯수 확인 필요 없음
            info['chapters'] = chapters
            self.to_screen(f"Embedded chapters from description:{[chapter.get('title') for chapter in chapters]}")
            return [], info

        # 댓글에서 추가
        comments: list[dict] = info.get('comments')
        if not comments:
            self.to_screen("Comment doesn't exists")
            return [], info

        for comment in comments:
            chapters = parse_chapters(comment.get("text", ""), video_duration)
            if chapters and len(chapters) >= 5:  # 길이 제한은 이거 기준으로 노래를 나눌거기 때문에
                info['chapters'] = chapters
                info['meta_comment'] = comment.get("text", "")  # 원본을 코멘트에 추가
                self.to_screen(f"Embedded chapters from comment:{[chapter.get('title') for chapter in chapters]}")
                return [], info

        self.to_screen(f"No chapters to embed found!")
        return [], info


class EmbedChapter(yt_dlp.postprocessor.PostProcessor):
    def __init__(self, downloader=None, chapter: list[dict[str, str | int]] = None):
        super().__init__(downloader=downloader)
        self.chapter = chapter

    def run(self, information):
        if self.chapter:
            information['chapters'] = self.chapter
        return [], information


def download_video(*, video_path: str,
                   urls: list[str] | str,
                   inner_folder: str = "",
                   thumbnail_path: str = "",
                   download_archive_path: str = os.getcwd(),
                   download_archive_name: str = '',
                   temp_path: str = '',
                   split_chapters: bool = False,
                   embed_info_json: bool = False,
                   restrict_format: str = "[height<=1080]",
                   ext: str = "mkv",
                   progress_hook: Callable[[dict], None] = None,
                   concurrent_fragments: int = 3,
                   ignore_errors: bool | str = 'only_download',
                   skip_hls_or_dash: list[str] | None = None,
                   chapter: list[dict[str, str | int]] = None,
                   logger=None,
                   quiet: bool = True,
                   progress_delta: float = 0):
    """
    skip_hls_or_dash: None(https), 'hls'(hls 스킵), 'dash'(dash 스킵)
    로거는 객체로 전달해야 함

    yt-dlp --quiet --concurrent-fragments 3 --quiet --format "bestvideo[height<=720]+bestaudio/best[height<=720]"
    --output "[%(upload_date>%y.%m.%d)s] %(title)s (%(uploader)s).%(ext)s"
    --paths "thumbnail:dirname" --paths "home:dirname"
    --write-thumbnail --convert-thumbnails jpg --embed-thumbnail
    --embed-chapters --embed-info-json --embed-metadata --embed-subs
    --merge-output-format mkv
    --write-comments --extractor-args "youtube:comment_sort=top;max_comments=10,10,0,0;lang=ko;skip=translated_subs"
    --download-archive "video_download_archive.txt"
    https://www.youtube.com/watch?v=e69muZQyTXY
    """
    # "private", "premium_only", "subscriber_only", "needs_auth", "unlisted" or "public"
    if type(urls) is str:
        urls = [urls]
    if inner_folder:
        inner_folder += "\\"
    ydl_opts = {'concurrent_fragment_downloads': concurrent_fragments,
                'extractor_args': {'youtube': {'skip': ['translated_subs']}},
                'format': f'bestvideo{restrict_format}+bestaudio/best{restrict_format}',
                'merge_output_format': ext,
                'noprogress': False,
                'outtmpl': {
                    'default': f"{inner_folder}%(title)s (%(uploader)s) [%(upload_date>%y.%m.%d)s].%(ext)s",
                    'chapter': f'{inner_folder}%(title)s - %(section_title)s (%(uploader)s) '
                               f'[%(upload_date>%y.%m.%d)s].%(ext)s'},
                'paths': {'home': video_path,
                          'chapter': video_path,
                          'temp': f"{video_path}\\temp" if not temp_path else temp_path,
                          'thumbnail': thumbnail_path if thumbnail_path else f"{video_path}\\thumbnails"},
                'postprocessors': [{'format': 'jpg',
                                    'key': 'FFmpegThumbnailsConvertor',
                                    'when': 'before_dl'},
                                   {'already_have_subtitle': False,
                                    'key': 'FFmpegEmbedSubtitle'},
                                   {'already_have_thumbnail': True, 'key': 'EmbedThumbnail'},
                                   {'add_chapters': True,
                                    'add_infojson': embed_info_json,
                                    'add_metadata': True,
                                    'key': 'FFmpegMetadata'}],
                'subtitleslangs': ['kr', 'jp', 'en'],
                'writesubtitles': True,
                'quiet': quiet,
                'writethumbnail': True,  # 없으면 썸내일 안들어감
                'ignoreerrors': ignore_errors,
                'nopart': True,
                'progress_delta': progress_delta
                }
    if split_chapters:
        ydl_opts["postprocessors"].append({'force_keyframes': False, 'key': 'FFmpegSplitChapters'})
    if progress_hook:
        ydl_opts['progress_hooks'] = [progress_hook]
    if download_archive_name:  # 이름 빈칸으로 하면 x
        ydl_opts['download_archive'] = f"{download_archive_path}\\{download_archive_name}" if download_archive_path \
            else download_archive_name
    if skip_hls_or_dash:
        ydl_opts['extractor_args']['youtube']['skip'] += skip_hls_or_dash
    if logger:
        ydl_opts["logger"] = logger

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.add_post_processor(EmbedChapter(chapter=chapter), when='before_dl')
        error_code = ydl.download(urls)

    return error_code


def download_music(*, music_path: str,
                   urls: list[str] | str,
                   inner_folder: str = "",
                   thumbnail_path: str = "",
                   download_archive_path: str = '',
                   download_archive_name: str = '',
                   temp_path: str = '',
                   split_chapters: bool = False,
                   embed_info_json: bool = False,
                   album: str = "%(uploader)s",  # playlist필드는 없음. 엘범에는 inner넣기
                   artist: str = "%(uploader)s",  # 트랙이 뭐 들어가는지 확인
                   progress_hook: Callable[[dict], None] = None,
                   concurrent_fragments: int = 3,
                   skip_hls_or_dash: list[str] | None = None,
                   chapter: list[dict[str, str | int]] = None,
                   ignore_errors: bool | str = 'only_download',
                   logger=None,
                   quiet: bool = True,
                   progress_delta: float = 0):
    """
    skip_hls_or_dash: None(https), 'hls'(hls 스킵), 'dash'(dash 스킵)
    로거는 객체로 전달해야 함

    m4a, 자막, 오디오만, 챕터 분리 다운로드 가능, 제목 수정
    여긴 썸내일 제거하면 미리보기가 아니라 꼬깔콘이 나옴
    엘범 부분에는 플리명 넣으면 알아서 됨
    python cli_to_api.py yt-dlp --quiet --no-progress --format "bestaudio/best" --concurrent-fragments 3
    --extract-audio --audio-quality 0 --remux-video mka
    --output "home:%(title)s (%(uploader)s).%(ext)s"
    --output "chapter:%(section_title)s - %(title)s (%(uploader)s).%(ext)s"
    --output "thumbnail:[%(upload_date>%y.%m.%d)s] %(title)s (%(uploader)s).%(ext)s"
    --paths "home:dirname" --paths "chapter:dirname" --paths "thumbnail:dirname"
    --convert-thumbnails jpg --embed-thumbnail --write-thumbnail
    --embed-chapters --embed-info-json --embed-metadata
    --write-comments --extractor-args "youtube:comment_sort=top;max_comments=10,10,0,0;lang=ko;skip=translated_subs"
    --split-chapters --download-archive "music_download_archive.txt"
    --parse-metadata "" --parse-metadata "" --parse-metadata ""
    https://youtu.be/jMSXPPSmsVo?si=C-x0Ah8OlTaLq2O6

    --parse-metadata "description:(?s)(?P<meta_comment>.+)"
    """
    if type(urls) is str:
        urls = [urls]
    if inner_folder:
        inner_folder += "\\"
    ydl_opts = {'concurrent_fragment_downloads': concurrent_fragments,
                'extractor_args': {'youtube': {'skip': ['translated_subs']}},
                'final_ext': 'mka',
                'format': 'bestaudio/best',
                'noprogress': False,
                'outtmpl': {
                    'default': f"{inner_folder}%(title)s (%(uploader)s).%(ext)s",
                    'chapter': f'{inner_folder}%(section_title)s - %(title)s (%(uploader)s).%(ext)s'},
                'paths': {'home': music_path,
                          'chapter': music_path,
                          'temp': f"{music_path}\\temp" if not temp_path else temp_path,
                          'thumbnail': thumbnail_path if thumbnail_path else f"{music_path}\\thumbnails"},
                'postprocessors': [{'format': 'jpg',
                                    'key': 'FFmpegThumbnailsConvertor',
                                    'when': 'before_dl'},
                                   {'key': 'FFmpegExtractAudio',
                                    'nopostoverwrites': False,
                                    'preferredcodec': 'best',
                                    'preferredquality': '0'},
                                   {'key': 'FFmpegVideoRemuxer', 'preferedformat': 'mka'},
                                   {'add_chapters': True,
                                    'add_infojson': embed_info_json,
                                    'add_metadata': True,
                                    'key': 'FFmpegMetadata'},
                                   {'actions': [(yt_dlp.postprocessor.metadataparser.MetadataParserPP.interpretter,
                                                 album,
                                                 '%(meta_album)s'),
                                                (yt_dlp.postprocessor.metadataparser.MetadataParserPP.interpretter,
                                                 artist,
                                                 '%(meta_artist)s')],
                                    'key': 'MetadataParser',
                                    'when': 'pre_process'},
                                   {'already_have_subtitle': False,
                                    'key': 'FFmpegEmbedSubtitle'}
                                   ],
                'subtitleslangs': ['kr', 'en', 'jp'],
                'writesubtitles': True,
                'quiet': quiet,
                'writethumbnail': True,
                'ignoreerrors': ignore_errors,
                'nopart': True,
                'progress_delta': progress_delta
                }

    if split_chapters: # and not chapter:
        ydl_opts["postprocessors"].append({'force_keyframes': False, 'key': 'FFmpegSplitChapters'})
##    else:  # 챕터 나누지 않으면
    ydl_opts["postprocessors"].append({'already_have_thumbnail': True, 'key': 'EmbedThumbnail'})
    if progress_hook:
        ydl_opts['progress_hooks'] = [progress_hook]
    if download_archive_name:  # 이름 빈칸으로 하면 x
        ydl_opts['download_archive'] = f"{download_archive_path}\\{download_archive_name}" if download_archive_path \
            else download_archive_name
    if skip_hls_or_dash:
        ydl_opts['extractor_args']['youtube']['skip'] += skip_hls_or_dash
    if logger:
        ydl_opts["logger"] = logger

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.add_post_processor(EmbedChapter(chapter=chapter), when='before_dl')  # 메타데이터 임베딩 하기 전이어야 함
        error_code = ydl.download(urls)

    return error_code


def bring_playlist_info(url: str, logger=None) -> dict:
    """플리의 title수정
    로거는 객체로 전달해야 함

    비디오별 타이틀은 그대로임. 이건 아래에 엔트리에서 수정
    parse-metadata는 각 영상마다 작동하지만 결과는 전체에만 적용되는 듯
    yt-dlp --flat-playlist --quiet --skip-download
    --extractor-args "youtube:lang=ko;skip=translated_subs"
    """
    ydl_opts = {'extract_flat': 'in_playlist',
                'noprogress': True,
                'quiet': True,
                'skip_download': True,
                'extractor_args': {'youtube': {'skip': ['translated_subs']}}
                }
    if logger:
        ydl_opts['logger'] = logger

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict: dict = ydl.extract_info(url, download=False)
        info_dict["old_title"] = info_dict.get("title")
        info_dict["title"] = format_filename(info_dict.get("title"))
        info_dict = ydl.sanitize_info(info_dict)

    return info_dict


def bring_video_info(url: str, playlist_name: str = "", logger=None) -> tuple[dict, str]:
    """
    전체 수, 댓글 전체수는 제한 없고 각 댓글마다 5개씩 20개 가져옴
    webpage_url이 아니라 url임.
    yt-dlp --skip-download --quiet
    --write-comments --extractor-args "youtube:comment_sort=top;max_comments=all,20,all,5;lang=ko;skip=translated_subs"
    https://youtu.be/FMn6hSMNXZQ?si=qipAvVcCy8RntzEK
    """
    ydl_opts = {'format': f'bestvideo[height<=1080]+bestaudio/best[height<=1080]',
                'extractor_args': {'youtube': {'comment_sort': ['top'],
                                               'max_comments': ['all', '20', 'all', '5'],
                                               'skip': ['translated_subs']}},
                'getcomments': True,
                'noprogress': True,
                'quiet': True,
                'skip_download': True,
                'writeinfojson': True}
    if logger:
        ydl_opts["logger"] = logger

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            ydl.add_post_processor(ExtractChapter(), when='after_filter')
            info_dict: dict = ydl.extract_info(url, download=False)
            info_dict["old_title"] = info_dict.get("title")
            info_dict["title"] = format_filename(info_dict.get("title"))
            if playlist_name:  # 비디오에서는 플리명을 모르기 때문에
                info_dict["playlist"] = playlist_name

            for key in ["formats", "requested_formats", "automatic_captions", "heatmap", "thumbnails", "heatmap"]:
                if key in info_dict.keys():
                    del info_dict[key]

            info_dict = ydl.sanitize_info(info_dict)
            tb = None
        except yt_dlp.DownloadError:
            info_dict = {}
            tb = traceback.format_exc()

    return info_dict, tb


def change_video_dict_list(channel_info_dict: dict) -> list[dict]:
    """채널 받아서 이름 포메팅 된 entries 내의 동영상 딕셔너리 리스트 반환"""
    entries: list[dict] = channel_info_dict.get("entries")
    video_list: list[dict] = []  # 비디오 딕셔너리 목록 담을 리스트
    # 만약 엔트리에 플리가 있으면 그거 붙이고 비디오면 append
    for entry in entries:
        if entry.get("_type") == "playlist":
            video_list += entry.get("entries")  # +=과 같은거임
        elif entry.get("_type") == "url":  # 비디오면
            video_list.append(entry)
    # 비디오 타이틀 변경. 이건 플리에서 바꾸는건데 플리에선 각 비디오 이름은 안바뀌므로
    for idx, video in enumerate(video_list):
        video["old_title"] = video.get("title")
        video["title"] = format_filename(video.get("title"))
        video["webpage_url"] = video.get('url')

    return video_list

# 구버전
# def change_video_dict_list(channel_info_dict: dict) -> list[dict]:
    # """채널 받아서 이름 포메팅 된 entries 내의 동영상 딕셔너리 리스트 반환"""
    # entries: list[dict] = channel_info_dict.get("entries")
    # video_list: list[dict] = []  # 비디오 딕셔너리 목록 담을 리스트
    # 만약 엔트리에 플리가 있으면 그거 붙이고 비디오면 append
    # if entries[0].get("_type") == "playlist":
        # [video_list.extend(playlist.get("entries")) for playlist in entries]  # +=과 같은거임
    # elif entries[0].get("_type") == "url":  # 비디오면
        # video_list = entries
    # 비디오 타이틀 변경. 이건 플리에서 바꾸는건데 플리에선 각 비디오 이름은 안바뀌므로
    # for video in video_list:
        # video["old_title"] = video.get("title")
        # video["title"] = format_filename(video.get("title"))
        # video["webpage_url"] = video.get('url')
# 
    # return video_list
