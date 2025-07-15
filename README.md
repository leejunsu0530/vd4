# vd4
유튜브의 플레이리스트나 채널을 다운로드하기 위한 모듈

[노션에서 보기](https://icy-puppet-ec6.notion.site/README-22dc7b1bc4808023a415d1060d6ef564?pvs=73)

[https://github.com/leejunsu0530/vd5](https://github.com/leejunsu0530/vd5)

[https://github.com/leejunsu0530/vd4](https://github.com/leejunsu0530/vd4)

- [README](#readme)
- [1. 사용된 주요 개념](#1-사용된-주요-개념)
	- [1.1. 사용된 모듈 설명](#11-사용된-모듈-설명)
		- [1.1.1. yt-dlp](#111-yt-dlp)
		- [1.1.2. rich](#112-rich)
		- [1.1.3. extcolors](#113-extcolors)
		- [1.1.4. pathlib](#114-pathlib)
	- [1.2. 포멧팅](#12-포멧팅)
		- [**1.2.1. %포멧팅**](#121-포멧팅)
		- [**1.2.2. `.format()`을 이용한 포맷팅**](#122-format을-이용한-포맷팅)
		- [**1.2.3. f-string 포멧팅**](#123-f-string-포멧팅)
		- [1.2.4. f-string의 단점](#124-f-string의-단점)
		- [1.2.5. yt-dlp에서의 % 포멧팅](#125-yt-dlp에서의--포멧팅)
	- [1.3. 컴프리헨션](#13-컴프리헨션)
	- [1.4. 주소에 의한 참조의 변경](#14-주소에-의한-참조의-변경)
		- [1.4.1. 리스트](#141-리스트)
		- [1.4.2. 함수(센티널 패턴)](#142-함수센티널-패턴)
	- [1.5. 타입 힌팅](#15-타입-힌팅)
		- [1.5.1. 사용 이유](#151-사용-이유)
		- [1.5.2. 이외 타입 힌트들](#152-이외-타입-힌트들)
	- [1.6. 클래스](#16-클래스)
		- [1.6.1. 클래스 변수](#161-클래스-변수)
		- [1.6.2. 메직 메소드 (Magic Method)](#162-메직-메소드-magic-method)
		- [1.6.3. 상속](#163-상속)
		- [1.6.4. 다중상속](#164-다중상속)
		- [1.6.5. 추상 클래스](#165-추상-클래스)
		- [1.6.6. `@staticmethod`와 유틸리티 클래스](#166-staticmethod와-유틸리티-클래스)
	- [1.7. 기타 개념](#17-기타-개념)
		- [1.7.1. 언패킹](#171-언패킹)
		- [1.7.2. 함수에서의 인자에 * 사용](#172-함수에서의-인자에--사용)
		- [1.7.3. 람다식과 함수](#173-람다식과-함수)
		- [1.7.4. for문과 enumerate에서의 del](#174-for문과-enumerate에서의-del)
		- [1.7.5. sum 함수](#175-sum-함수)
		- [1.7.6. sort에서의 키 설정](#176-sort에서의-키-설정)
- [2. 코드 구조](#2-코드-구조)
	- [2.1. 기본 구조](#21-기본-구조)
	- [2.2. `VideosManager`](#22-videosmanager)
	- [2.3. `Videos`](#23-videos)
- [3. 개선 사항](#3-개선-사항)
	- [3.1. 적용된 개선 사항](#31-적용된-개선-사항)
	- [3.2. 적용할 개선사항](#32-적용할-개선사항)



# 1. 사용된 주요 개념

## 1.1. 사용된 모듈 설명

### 1.1.1. yt-dlp

 

1. 기본 설명
    
    **yt-dlp**는 유튜브 등의 지원하는 동영상 사이트를 파싱해서, 영상 및 재생목록의 정보를 가져오고 영상을 다운로드받을 수 있는 기능을 제공하는 프로그램이다. 업데이트가 중단된 youtube_dl의 포크 중에서, 현재 가장 활발히 업데이트를 하고 있다. 
    
    원래는 cmd 창 등에서 `yt-dlp —path “C:Users/user/Desktop” —output “파일명” “url”` 등의 형식으로 명령어로 입력하여 실행하지만, 이 프로그램이 파이썬으로 만들어져 있기에 파이썬 모듈로 호출해서 사용할 수도 있다.
    
    [https://github.com/yt-dlp/yt-dlp](https://github.com/yt-dlp/yt-dlp)
    
    ```python
    # pip install yt-dlp로 설치
    
    from yt_dlp import YoutubeDL
    ydl_opts = {}
    with YoutubeDL(ydl_opts) as ydl:
        # url의 정보 가져오기
        # info_dict = ydl.extract_info("url1", download=False)
        # 리스트 내 url들 다운로드
        ydl.download(["url1", "url2"])
    ```
    
    기본적인 사용 방식은 위와 같다. 더 자세한 내용은 **EMBEDDING YT-DLP** 항목을 참조하길 바란다.
    
     `ydl_opts` 딕셔너리에 다양한 인자를 넣어서 할 작업을 지정할 수 있는데, 이에 대한 자세한 설명은 위 깃허브의 `USAGE AND OPTIONS` 항목 및 `EXTRACTOR ARGUMENTS`에 있는 명령어 목록을 확인하면 알 수 있다. 해당 명령어들은 cmd 상에서 사용하는 명령어들이고 이를 아래 프로그램에서 실행시키면 딕셔너리 형태로 얻어낼 수 있다. 이를 `ydl_opts` 부분에 넣어서 작동하면 된다.
    
    [yt-dlp/devscripts/cli_to_api.py at master · yt-dlp/yt-dlp](https://github.com/yt-dlp/yt-dlp/blob/master/devscripts%2Fcli_to_api.py)
    
    이하에서는 내가 사용한 명령어들만을 자세히 설명한다.
    
2. 모듈 내 자료형 및 키 설명
    
    출력 템플릿의 자세한 항목들(`title, filesize, uploader` 등)은 깃허브의 `OUTPUT TEMPLATE`와 `Filtering Formats`를 참조하길 바란다.
    
    정보를 가져올 때, 대상 url과 이를 가져오는 옵션의 종류에 따라 몇 가지로 분류해볼 수 있다.
    
    먼저 대상 url에 따른 분류이다.
    
    - **개별 동영상의 url**: 정보가 json 형식(파이썬에서 처리할 때는 딕셔너리 형식)으로 불러와진다. 내부에는 `title, duration, filesize, filesize_approx, upload_date, uploader, channel, thumbnails, format, subtitles, description, like_count, availability, channel_url` 등의 값이 있다.
    - **재생목록의 url**: 재생목록의 정보를 딕셔너리 형식으로 가져온다. 이때 재생목록 내의 개별 동영상의 정보들은 `entries` 항목에 개별 영상이 딕셔너리로 든 리스트 형태로 저장된다. 재생목록 자체의 `title, thumbnails, uploader, like_count` 등의 값이 있다.
    - **채널의 홈페이지 url**: yt-dlp에서는 채널도 재생목록과 유사하게 처리하여, 채널 내 모든 동영상의 정보를 읽어온다. 이때 채널 내의 탭(라이브, 동영상, shorts 등의 탭)을 각각 아래의 재생목록과 같게 취급하여, 각 재생목록이 든 리스트 형태로 반환한다.
    - **채널의 /featured 탭 url**: 최근에 패치되었을지도 모르지만 마지막 테스트 기준으로는 데이터가 올바르게 든 형식으로 불러와지지 않는다. 사이트 상에서는 /featured를 제거한 것과 형태가 동일하다.
    
    데이터 내의 정보 중에, 다른 것들은 공식 깃허브에 설명이 자세히 나와있으니 특기할만한 것만 설명한다.
    
    - `uploader`와 `channel`: 다른 사이트에서는 다를 수 있으나 유튜브에서는 둘이 동일하다.
    - `uploader_id`와 `channel_id`: 어느 url에서 추출했냐에 따라 둘이 다를 수 있으며, 플레이리스트의 경우에는 둘 중 하나가 없을 수 있다.
    - `id`: 유튜브의 id는 플레이리스트의 경우에는 playlist?list=부분 뒤의 문자열이며, 영상의 경우에는 watch=뒤의 문자열이다. 그리고 채널의 경우에는 유튜브가 업데이트됨에 따라 형식이 바뀌었으며, 예전 형식 또한 유효하다. 채널의 형식은 위의 플레이리스트/영상과 비슷한 형태의 문자열([http://youtube.com/c/](http://youtube.com/c/)id 형태, 구버전) 또는 @로 시작하는 채널 헨들러의 형태(신버전)이다.
    - `url`과 `webpage_url`: 재생목록이나 채널의 링크는 url, 동영상의 링크는 webpage_url에 들어있다.
    - `thumbnails`: 딕셔너리가 든 리스트 형식으로, 해당도에 따라 다른 링크와 해상도 등의 정보들이 들어있고, 우선도가 있어 숫자가 작은 게 유튜브에 표시되는 형식이다. 채널의 경우에는 배너(채널아트)와 썸내일(채널의 동그란 사진)이 같이 포함되어 있다. 각각은 딱히 구분 표지가 없으나 채널의 썸내일은 정사각형의 해상도를 지닌다. 그 외에 크기에 맞게 잘리지 않은 썸내일이 uncropped가 붙은 이름으로 들어있다. 이 형식에는 우선 순위, 해상도 등의 일부 정보가 없다.
    
    다음으로 플레이리스트나 채널의 url의 정보를 가져오는 방식을 설명하겠다.
    
    - **그냥 가져오기**: 아무 제한 옵션 없이 정보를 가져오면 영상을 다운로드하고, 채널 내 모든 영상의 자세한 정보를 가져온다. 이는 각 영상마다 따로 페이지에 접속하여 정보를 가져오는 것으로, 그냥 yt-dlp만으로는 시간이 오래 걸린다. 이 코드에서는 이를 파이썬의 멀티스레딩으로 해결했다.
    - **--skip-download**: 영상을 다운로드하지 않고 정보를 가져온다. 위의 방식과 다른 점은 영상 파일을 다운로드하지는 않는다는 점 뿐이다.
    - **--flat-playlist**: 각 영상의 세부정보 없이 그냥 가져올 수 있는 값만을 가져오고, 플레이리스트의 정보도 간략화되어 있다. 예를 들어 영상의 availability 값은 원래 기본적으로 “public”이고 비공개 동영상이나 맴버십 한정, 숨김 처리된 영상일 경우 등에 각각에 해당하는 값이 들어있다. 하지만 이 방식으로 가져오면 기본적으로 None이 들어있고 비공개 등일 때 해당하는 값이 들어있게 된다. 또한 업로드 날짜는 키값은 있으나 안에 None이 들어있다. 속도가 빨라져 1~2분 안에 정보를 모두 불러올 수 있다.
3. 정보 가져오기 함수 옵션 설명
    
    위의 설명대로, flat-playlist 옵션을 적용해 개략적인 정보를 가져온 후 각 영상의 url을 따로 가져와 멀티스레딩을 통해 빠르게 하는 방법을 택해 속도를 높였다. 함수의 구현은 아래에서 설명하고, 여기서는 함수에 사용된 ydl_opts만 설명한다.
    
    ```python
    def bring_playlist_info(url: str, logger=None, change_lang: bool = False) -> PlaylistInfoDict | ChannelInfoDict:
        ydl_opts: dict[str, Any] = {
            "extract_flat": "in_playlist",
            "noprogress": True,
            "quiet": True,
            "skip_download": True,
            "extractor_args": {
                "youtube": {
                    "skip": ["translated_subs"],
                }},
        }
        if logger:
            ydl_opts["logger"] = logger
        if change_lang:
            ydl_opts["extractor_args"]["youtube"]["lang"] = ['ko']
    
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict: PlaylistInfoDict | ChannelInfoDict = ydl.extract_info(
                url, download=False)
            info_dict["old_title"] = info_dict.get("title", "")
            info_dict["title"] = format_filename(info_dict.get("title", ""))
            info_dict = ydl.sanitize_info(info_dict)
    
        return info_dict
    
    def bring_video_info(url: str,
                         playlist_name: str = "", playlist_uploader: str = "",
                         logger=None) -> tuple[VideoInfoDict, str | None]:
        ydl_opts = {
            "format": "bestvideo[height<=1080]+bestaudio/best[height<=1080]",
            "extractor_args": {
                "youtube": {
                    "comment_sort": ["top"],
                    "max_comments": ["all", "20", "all", "5"],
                    "skip": ["translated_subs"],
                }
            },
            "getcomments": True,
            "noprogress": True,
            "quiet": True,
            "skip_download": True,
            "writeinfojson": True,
        }
        if logger:
            ydl_opts["logger"] = logger
    
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            try:
                ydl.add_post_processor(ExtractChapter(), when="after_filter")
                info_dict: VideoInfoDict = ydl.extract_info(url, download=False)
                info_dict["old_title"] = info_dict.get("title", "")
                info_dict["title"] = format_filename(info_dict.get("title"))
                if playlist_name:  # 비디오에서는 플리명을 모르기 때문에
                    info_dict["playlist"] = playlist_name
                if playlist_uploader:
                    info_dict["playlist_uploader"] = playlist_uploader
    
                info_dict = ydl.sanitize_info(info_dict)
                tb = None
            except yt_dlp.DownloadError:
                info_dict = {}
                tb = traceback.format_exc()
    
        return info_dict, tb
    
    ```
    
    위쪽의 함수는 **플레이리스트/채널에서 정보를 가져오는 함수**이다. 
    
    - `extract_flat, skip_download`: 플레이리스트의 정보를 간략하게 가져온다
    - `noprogress, quiet`: 프로그래스 바와, 다른 진행상황 출력을 끈다
    - `extractor_args` 내 `youtube`: 유튜브에서만 적용되는 설정이다
        - `skip`의 `translated_subs`: 자동번역된 자막을 가져오지 않아 속도를 향상시킨다
        - `lang`의 `ko`: 언어를 한국어로 바꾼다
    - `logger`: 사용자가 정의한 로거(깃허브의 임베딩 부분에 나온 예제를 활용해 만든 클래스)를 사용해 진행상황을 출력한다
    
    추출 이후, 제목을 파일명으로 사용하여 데이터를 저장하기 때문에 윈도우 환경에서 파일명에 사용 불가한 문자(/, \, ‘, “, ?, : 등)를 해당 문자의 전각 문자로 바꾼다
    
    두번째 함수는 **개별 영상에서 자세한 정보를 가져오는 함수**이다
    
    - `format`: 여러 화질의 영상/소리 파일 중 어느 것을 고를지를 선택한다. 여기에 사용된 옵션은 화질이 1080p 미만인 최선의 영상과 오디오를 가져와 병합하는 걸 시도하고(bestbideo+bestaudio), 실패 시(/), 화질이 1080p 미만인 최선의 영상과 오디오가 통합된 파일(best)을 가져온다. 이에 대한 자세한 설명은 깃허브의 FORMAT SELECTION 부분에 있다
    - `extractor_args` 내 `youtube`: 위와 같다
        - `comment_sort`의 `top`: 댓글을 인기순으로 가져온다
        - `max_comment`: **최대 전체 댓글 수, 최대 부모 댓글(대댓글이 아닌 댓글) 수, 최대 전체 대댓글 수, 각 댓글마다 대댓글 수**를 각각 지정한다. all이면 갯수에 제한이 없는 대신 모든 댓글을 가져오느라 더 오래 걸린다. 여기 설정에서는 각 부모 댓글마다 5개의 대댓글을 가져오고, 부모를 총 20개 가져와서 전체 댓글 수는 100개가 된다
        - `skip`의 `translated_subs`: 위와 같다
    - `getcomments, writeinfojson`: 이 설정까지 켜야 댓글을 가져온다
    - `noprogress, quiet, skip_download`: 위와 같다.
    
4. 영상/음악 다운로드 함수 옵션 설명
    
    기본 다운로드 옵션
    
    - `concurrent_fragment_downloads`: yt-dlp 내의 자체적인 멀티스레딩 기능을 사용할 때, 동시에 할 작업 수. 유튜브에서는 효율성을 위해 한 영상을 여러 조각으로 나눠서 다룬다. 이를 이용하면 영상이 여러 조각으로 나뉜 경우에 여럿을 동시에 처리할 수 있다.
    - `extractor_args`: `{"youtube": {"skip": ["translated_subs"]}}`, 자동 번역 자막을 가져오지 않는다.
        - `skip_hls_or_dash` 값이 있을 경우 이 리스트에 추가된다. 이 경우 hls나 dash 데이터를 생략하여 속도를 높인다.
    - `format`: 선택한 제한 조건에 맞춰 형식을 제한한다
        - 비디오: `bestvideo{restrict_format}+bestaudio/best{restrict_format}`
        - 오디오: `bestaudio/best`
    - `merge_output_format`: 비디오 다운로드가 끝난 후, 컨테이너 형식을 설정한다. 컨테이너는 아래에 설명되어 있다.
    - `final_ext`: 오디오 파일을 다운로드 한 후 최종 형식을 mka로 설정한다.
    - `noprogress`: `False`, 프로그래스 바를 띄운다
    - `quiet`: 상황 출력 여부를 결정한다
    - `ignoreerrors`: 에러를 출력하지 않는다. 로거에는 잘 전달되어, 로거에서는 출력할 수 있다
    - `nopart`: `True`, 영상을 .part 파일로 나눠 저장한 후 합치지 않고, 나눈 것을 한번에 합친 후 저장한다. 관리자 권한이나 케시 부족 등으로 오류가 발생하여 추가한 옵션이다
    - `progress_delta`: 프로그래스 바가 업데이트될 때까지의 시간을 지정한다
    - `progress_hooks`: 다운로드 시에 실행되는 함수(보통 로깅 용도로 사용)을 추가한다
    - `logger`: 로거를 추가한다
    
    ---
    
    출력 경로 및 파일명 관련
    
    - `outtmpl`: 출력할 파일명을 지정한다. paths 같은 곳에서는 %()s 형태의 포멧팅이 적용되지 않고 넣은 그대로 나오는데(ex: %(uploader)s라 적으면 %(uploader)s라 저장된다), 여기서는 알맞은 항목에 맞게 바뀌기 때문에(ex: %(uploader)s라 적으면 그 부분에 업로더 이름이 들어간다), 이를 이용해 inner_folder 부분에 폴더 형식을 넣으면 해당 형식에 맞춰 폴더와 영상이 나뉘게 하였다. 예를 들어 inner_folder에 %(uploader)s가 들어가면 플레이리스트 내 영상의 업로더에 따라 하위 폴더가 생기고 이에 맞게 영상이 분류된다. 이 부분은 추후 업데이트 시 하위 폴더를 내가 지정하는 방식으로 바꿔 제거하였다. 여러 종류의 파일마다 저장할 이름을 각기 다르게 지정할 수 있다. 또한 마지막에 %(ext)s를 적어야 확장자가 망가지지 않고 적용된다.
    - `paths`: 영상을 저장할 경로로, home이면 후처리까지 완료된 영상의 경로, chapter는 챕터별로 쪼개진 영상의 경로, temp는 중간의 영상 조각이나 썸내일 등이 거쳐가는 경로, thumbnail은 썸내일이 저장되는 경로로, temp와 thumbnail은 만일 경로를 따로 지정하지 않을 시 비디오 경로 내에 저장하게 하였다.
    
    ---
    
    후처리기 (postprocessors)
    
    ---
    
    공통
    
    - `format: "jpg"`
        
        썸내일을 jpg 형식으로 바꾼다. 이렇게 해야 영상에 메타데이터로 잘 적용된다.
        
    - `key: "FFmpegThumbnailsConvertor"`
        
        썸내일을 변환하는 후처리기이다.
        
    - `when: "before_dl"`
        
        다운로드 전에 실행한다. 썸네일 변환 시 필요하다.
        
    - `already_have_subtitle: False`
        
        자막이 이미 존재하지 않는 것으로 간주하고 삽입한다.
        
    - `key: "FFmpegEmbedSubtitle"`
        
        자막을 삽입한다.
        
    - `already_have_thumbnail: True`
        
        이미 썸내일이 존재하는 것으로 간주하고, 썸내일을 영상/오디오에 삽입한다.
        
    - `key: "EmbedThumbnail"`
        
        썸내일을 미디어 파일에 삽입하는 역할을 한다.
        
    - `key: "FFmpegMetadata"`
        
        메타데이터 관련 후처리기로, 챕터 정보와 함께 infojson 데이터 등을 삽입한다.
        
    - `add_chapters: True`
        
        챕터 정보를 메타데이터에 기록한다. 이는 팟플레이어의 책갈피 등의 기능으로 볼 수 있다.
        
    - `add_infojson: embed_info_json`
        
        info.json의 내용을 메타데이터로 삽입한다.
        
    - `add_metadata: True`
        
        메타데이터 전체 삽입 여부.
        
    - `key: "FFmpegSplitChapters"`
        
        챕터별로 별개의 영상/오디오 파일로 나눈다.
        
    - `force_keyframes: False`
        
        챕터 분할 시 키프레임에 정렬하지 않도록 한다.
        
        ---
        
        오디오 전용
        
    - `key: "FFmpegExtractAudio"`
        
        FFmpeg로 오디오를 추출한다.
        
    - `nopostoverwrites: False`
        
        기존파일 덮어쓰기 허용.
        
    - `preferredcodec: "best"`
        
        최상의 코덱을 선택한다.
        
    - `preferredquality: "0"`
        
        최고 음질로 설정한다.
        
    - `key: "FFmpegVideoRemuxer"`
        
        파일의 컨테이너를 변경한다. remux는 인코딩을 새로 하지 않고 컨테이너를 변경한다.
        
    - `preferedformat: "mka"`
        
        remux 시 사용할 최종 컨테이너 형식.
        
        자막 관련
        
    - `subtitleslangs: ["kr", "jp", "en"]`
        
        자막의 언어를 지정한다. 이외의 언어는 들어가지지 않는다. 적힌 순서대로 우선순위가 적용된다.
        
    - `writesubtitles: True`
        
        자막을 기록한다.
        
    
    ---
    
    기타
    
    - `writethumbnail: True`:썸내일을 파일로 저장한다. 없으면 썸내일이 파일에 들어가지 않는다.
    - `download_archive`: 이름을 빈칸으로 하면 작동하지 않는다. 다운로드한 영상을 기록하고 다시 다운로드할 때 스킵하는, 다운로드 아카이브 파일을 지정한다.
    - `skip_hls_or_dash`: 자막 외에도 추가적으로 필요없는 데이터를 스킵한다. 이 필요없는 데이터는 최고 품질의 영상이 무엇인지 확인한 후, 그 외의 형식을 생략하는 형태이다.
    - `ChangeInfoDict`: 정보를 변경하는 클래스를 후처리기로 추가하였다.
    
5. 컨테이너와 코덱 및 메타데이터 설명
    - 컨테이너: mkv, mp4, mka, m4a 등 파일의 확장자로 기록된 것으로, 메타데이터가 어떻게 들어갈지 등을 포함한다. 포장지와 비슷한 개념이다. 아래의 페이지에 자세하게 정리하였다. 나는 mkv와 mp4 중 기능이 더 뛰어난 mkv를 사용하였다. 오디오의 형식에는 mka와 m4a가 있는데, 각각 mkv와 mp4의 오디오 버전이다.
    
    [컨테이너 개념](./docs/컨테이너_개념.md)
    
    - 코덱: 영상이나 오디오의 압축 방식이다. 컨테이너가 달라도 코덱은 동일할 수 있다.

### 1.1.2. rich

- rich로 할 수 있는 작업의 대략적인 내용과 예제가 있는 리드미:

[https://github.com/Textualize/rich](https://github.com/Textualize/rich)

- 자세한 함수 등의 사용법이 적힌 docs:
    
    [Welcome to Rich’s documentation! — Rich 13.6.0 documentation](https://rich.readthedocs.io/en/stable/)
    

rich는 다양한 출력을 제공하는 라이브러리이다.

해당 프로젝트에 사용된 rich의 주요 기능은 style, table, progress, prompt 등이다. 각각의 자세한 적용은 아래에서 설명하고 공통적으로 적용되는 내용만 설명한다.

- `Console` : rich에서 출력을 하는데 필요한 객체이다. 한 프로젝트에서 하나만을 만들고, 다른 파일들에서는 이를 임포트해서 사용한다. console.print를 통해 기존의 print 함수처럼 출력할 수 있으며, rich의 표나 패널 등의 객체도 이를 통해 출력한다. 자세한 것은 https://rich.readthedocs.io/en/stable/console.html 참고.
- **스타일:** rich에서는 모든 텍스트에 다양한 색과 취소선, 볼드체 등의 스타일을 적용할 수 있다. rich의 객체들은 이를 여러 방법으로 지정할 수 있다. 여기 설명되지 않은 자세한 내용은 https://rich.readthedocs.io/en/stable/style.html를 참조하라.
    - **색상:**
        1. “red”처럼 https://rich.readthedocs.io/en/stable/appendix/colors.html#appendix-colors을 참조하여, 해당 이름을 문자열로 적으면 rich에서 인식할 수 있다.
        2. “#FF0000” 등의 #이 앞에 붙은 헥스 형식도 인식 가능
        3. “rgb(255,0,0)” 형태의 문자열도 인식 가능. “rgb” 라 적고 그 뒤에 띄어쓰기 없이 0~255까지의 숫자를 적은 후 괄호를 닫으면 된다.
    - **볼드체, 취소선, 밑줄, 이탤릭체** 등의 스타일: 위 스타일에 관한 docs에 나온 대로, 각각 **bold 또는 b**, ~~strike 또는 s~~, underline 또는 u, *italic 또는 i*를 적으면 된다. 또한 **dim**을 적으면 색상이 어두워진다.
    - **배경:** 색상과 같은 형식을, on 뒤에 적으면 된다. 예를 들면 “white on red”는 붉은 배경에 하얀 글씨를 적는다.
    - 이를 조합하면, **“bold s red on #0000FF”** 같은 식으로 적을 수 있다. 이는 hello world라는 문자열에 적용 시 **~~hello world~~** 같은 형식이 된다.
    - 이 외에도 "link [https://google.com](https://google.com/)" 같은 형식의 스타일은 해당 스타일이 적용되는 글자에 링크를 걸 수 있다.
    - `Style` 객체: 위의 문자열을 사용하는 대신 스타일 객체를 만들어서 사용할 수 있다. 이는 `from rich.style import Style`로 임포트하며 `Style(color=’red’, bold=True)`처럼, 속성들을 일일히 설정할 수 있다. 이는 객체이기 때문에 다른 스타일 객체와 더해 스타일을 수정할 수 있다. 위의 문자열을 `Style.parse(“bold s red on #0000FF”)` 이렇게 안에 넣어 스타일 객체로 만들 수 있다.

위와 같은 방식으로 만든 스타일도 적용하는 방법이 여러가지 있다.

- rich의 `print` 함수나 `console` 객체를 사용한 출력(즉, 표, 프로그래스 바 등을 포함한 rich에서 지원하는 모든 종류의 출력) 내에서는, 문자열에 []를 통해 적용할 수 있다. 예를 들어 `“[bold red]hello world[/]”` 라 적으면 해당 부분으로 감싸진 부분에 스타일이 적용된다. [/]은 앞에서 적용된 스타일을 모두 제거하는 역할이고, [/red]라 적으면 빨간색만 사라지고 bold는 유지된다.
- 표나 프로그래스 바 등에서는 해당 객체를 만들 때 세세하게 스타일을 설정할 수 있다. 예를 들어 표는 제목, 각 줄, 테두리 등에 따로 별개의 스타일을 적용할 수 있다. 이런 식의 적용은 각 객체의 docs에 설명이 나와있다.

이외에 이 프로젝트에서 사용된 rich의 기능들은 docs에 설명이 자세하게 나와있으므로 이로 대체한다.

표: https://rich.readthedocs.io/en/stable/tables.html - 영상 정보의 출력에 사용되었다.

└ 박스: https://rich.readthedocs.io/en/stable/appendix/box.html#appendix-box

프로그래스 바: https://rich.readthedocs.io/en/stable/progress.html - 다운로드 진도 표시에 사용되었다.

└ 스피너: `python -m rich.spinner` 로 확인가능

패널: https://rich.readthedocs.io/en/stable/panel.html - 정보를 네모 칸 안에 표시하는데 사용되었다.

그룹: https://rich.readthedocs.io/en/stable/group.html - 여러 객체를 하나로 묶는데 사용되었다.

라이브: https://rich.readthedocs.io/en/stable/live.html - 프로그래스 바와 패널이 묶인 객체를 업데이트하기 위해 사용되었다. 패널은 프로그래스 바처럼 자동 업데이트가 되지 않는다. 참고로, 프로그래스 바 등의 객체들도 내부에서는 live 객체를 사용한다.

트레이스백: https://rich.readthedocs.io/en/stable/traceback.html - 코드 상단의 `install` 구문을 통해 더 보기 쉬운 오류 메시지를 출력한다.

### 1.1.3. extcolors

썸내일에서 메인 색상을 추출하기 위해 사용되었다. 별로 복잡하지 않으니 딱히 설명하진 않고 pypi의 설명을 남겨놓겠다. 

[Client Challenge](https://pypi.org/project/extcolors/)

### 1.1.4. pathlib

파이썬에서는 원래 경로를 `os.path.join()`으로 다루거나 그냥 문자열로 다룬다. 또한 os, glob, shutil의 라이브러리를 통해 여러 기능을 수행한다. 하지만 파이썬 3.4버전 이후부터는 pathlib 라이브러리를 통해 이 모든 기능을 한번에 다룰 수 있다.

이 라이브러리의 장점과 특징은 아래와 같다.

1. 라이브러리의 `Path()` 객체를 통해 경로를 다룰 수 있다. 객체의 인자에는 다른 `Path` 객체, 문자열로 된 경로 등이 들어갈 수 있다.
2. 경로가 객체가 되어 문자열과는 연산자를 정의할 수 있게 되었다. 이 라이브러리에서는 “C:Users/user/Desktop”라는 경로를 `Path("C:Users") / Path(“user”) / “Desktop”`와 같이 / 연산자로 이을 수 있으며 문자열도 이를 통해 객체에 연결할 수 있다. 이를 통해 가독성이 기존 방식들보다 향상된다. 물론 전통적인 join처럼 `Path(”C:Users”, Path(“user”), “Desktop”)` 형태도 동일하게 기능한다.
3. 내부에 여러 파일에 관련된 메소드들이 있다. `read_text, write_text, cwd, glob, parent, name, joinpath, replace` 등의 메소드로 경로에서 바로 작업을 수행할 수 있다.

더 자세한 활용에 대해서는, 참고한 링크를 남겨놓는다.

[035 파일 경로를 객체로 다루려면? ― pathlib](https://wikidocs.net/110182)

## 1.2. 포멧팅

파이썬에는 여러 포멧팅이 있다. 현 시점에서는 이를 모두 자세히 알 필요는 없지만 구버전에 사용되던 포멧팅이 현재에서도 적용되는 경우가 있으므로, 그런 것이 있다는 정도로는 알 필요가 있다.

### **1.2.1. %포멧팅**

C언어와 유사한 방식으로, 현재는 잘 쓰이지 않는다.

```python
print("%d" % 10) # 10
print("%s" % 10) # 10 
# 원래 정수는 %d가 맞지만, 파이썬에서는 자동으로 str을 적용한 값이 출력되므로 %s가 모든 자료형에 적용될 수 있다.
print("%10.2f" % 3.14159) # '      3.14' (폭 10칸, 소숫점 둘째자리까지)
# 실수의 자릿수 제어는 %s가 불가능하다.

data = {"name": "철수", "age": 20}
print("이름: %(name)s, 나이: %(age)d" % data)
# 출력: 이름: 철수, 나이: 20
# %(key)s 형식은 딕셔너리를 % 포맷에 넘겨 해당 키의 값을 삽입할 때 사용.
```

%를 문자로 출력하고 싶을 경우 %%라고 적는다.

### **1.2.2. `.format()`을 이용한 포맷팅**

문자열에 정의된 메소드를 사용하는 방법이다.

```python
print("{}".format(10))               # 10 
# 자료형에 상관없이 작동한다.
print("{:10.2f}".format(3.14159))   # '      3.14' (width 10, 2 decimal places)

data = {"name": "철수", "age": 20}
print("이름: {name}, 나이: {age}".format(**data))
# 출력: 이름: 철수, 나이: 20
# 딕셔너리의 언패킹을 이용한 방법이다. 언패킹에 대해선 아래 언패킹 부분에서 더 자세히 설명한다.

# 또는 이렇게 적어도 동일하다.
data = {"name": "철수", "age": 20}
print("이름: {name}, 나이: {age}".format(name="철수", age=20))

```

그냥 {}를 출력할 경우 {{}}라 적어야 한다. 예를 들어 {title}이라 적을 경우 “{{title}}”이라 적는다.

이 외에도 딕셔너리를 언패킹없이 바로 넣을 수 있는 format_map() 메소드도 있다. 이에 대해서는 아래에서 좀 더 자세히 설명한다.

### **1.2.3. f-string 포멧팅**

파이썬 3.6부터 추가되었으며 현재 주류 방식이다.

```python
print(f"{10}")               # 10
print(f"{10}")               # 10
print(f"{3.14159:10.2f}")   # '      3.14'

data = {"name": "철수", "age": 20}
print(f"이름: {data['name']}, 나이: {data['age']}")
# 출력: 이름: 철수, 나이: 20
# 이렇게 적는 것이 가능하지만, 위의 포멧팅과 달리 이렇게 굳이 적을 필요는 없다.

name = "철수"
age = 20
print(f"이름: {name}, 나이: {age}")
# 이렇게 변수를 바로 적을 수 있다는 단순함 때문에 가장 많이 쓰인다.
```

### 1.2.4. f-string의 단점

현재는 f 포멧팅이 주로 사용되며, 다른 포멧팅은 f 포멧팅으로 바꿀 수 있을 경우 IDE에서 바꾸라는 권고가 뜨기도 한다.

하지만 f 포멧팅에 비해 다른 포멧팅이 가지는 이점이 있기도 하다.

- 아직 생성되지 않은 변수의 위치 지정:
    - 먼저 문자열을 만들어 놓고 나중에 값을 채우려면 f 포멧팅이 아닌 다른 포멧팅이 필요하다.
        
        ```python
        text = f"{trainer}은/는 {pokemon}을/를 잡았다!" # f포멧팅의 경우 변수가 없어 에러가 난다.
        
        text = "{trainer}은/는 {pokemon}을/를 잡았다!"
        text.format(trainer="한지우", pokemon="피카츄") # 나중에 적용할 수 있다.
        ```
        
    - f-string은 아직 정의되지 않은 인자 또는 이름을 알지 못하는 인자에 적용될 수 없기 때문에 이러한 경우에는 format 메소드를 사용한다. ex) 한 함수에서 두 개의 인자를 받고 한 인자가 다른 인자를 사용할 경우
        
        ```python
        def return_formatted_string(name, string_to_format, **kwargs):
            return string_to_format.format(name=name,**kwargs)
            
        template = "안녕하세요, {name}님. {subject} 수업은 {time}에 시작합니다."
        result = return_formatted_string(
            name="영희",
            string_to_format=template,
            subject="수학",
            time="2시"
        )
        print(result)
        # 출력: 안녕하세요, 영희님. 수학 수업은 2시에 시작합니다.
        ```
        
- 딕셔너리의 값 적용: f 포멧팅은 다른 두 포멧팅과 달리 딕셔너리를 곧바로 적용할 수 없다.
    - 안전한 포멧팅: 원래 포멧팅을 할 때는 인자가 없으면 에러가 나는데, 딕셔너리를 적용할 수 있는 두 포멧팅은 딕셔너리 자체의 구조를 수정하여 에러가 나지 않는 포멧팅을 만들 수 있다.
        
        ```python
        
        class SafeDict(dict):
            def __missing__(self, key):
                return f"{{{key}}}"  # format 스타일 기본
        
            def __getitem__(self, key):
                # % 포맷팅에서만 호출됨
                try:
                    return super().__getitem__(key)
                except KeyError:
                    return f"%({key})s"
        
            def safe_format_all(self, template: str) -> str:
                """
                {key}와 %(key)s 포맷이 섞인 문자열을 모두 처리
                """
                # 1단계: format-style {key} 처리
                result = template.format_map(self)
        
                # 2단계: %-style %(key)s 처리
                try:
                    result = result % self
                except TypeError:
                    # 예: %(key)d처럼 숫자 기대할 경우 대응 불가
                    result = result
                return result
        
        template = "이름: {name}, 점수: {score}, 이름: %(name)s, 점수: %(score)s"
        data = SafeDict(name="영희")  # 'score'는 없음
        
        print(data.safe_format_all(template))
        # 출력: 이름: 영희, 점수: {score}, 이름: 영희, 점수: %(score)s
        
        ```
        

### 1.2.5. yt-dlp에서의 % 포멧팅

yt-dlp에서는 %포멧팅을 일부 수정하여, 해당 특수 포멧팅을 출력 형식 지정, 메타데이터 변경 등에서 사용한다. 기본적으로 %()s에서 괄호 안에 `uploader` 등의 데이터 명을 적으면 해당 데이터가 들어간 상태로 출력되며, 그 외에도 몇 가지 간단한 연산 작업 등을 포멧팅 내에서 할 수 있다.

1. 객체 순회: `%(tags.0)s` (tags 리스트의 첫 번째 값을 가져온다), `%(id.3:7)s` (:로 슬라이싱을 할 수 있다) 등
2. 간단한 산술 연산: `%(playlist_index+10)s` 
3. 날짜, 시간 포멧팅(strftime 형식): `>` 를 사용한다. ex) `%(duration>%H-%M-%S)s`, `%(upload_date>%Y-%m-%d)s`, `%(epoch-3600>%H-%M-%S)s`
4. 대안 값: 값이 없을 경우 사용할 값을 지정한다. `,` 를 사용한다. ex)`%(release_date,upload_date)s` 
5. 비어 있지 않을 때 대체: `%` 와 `|` 를 사용하여, `%` 앞의 값이 존재하면 `%`와 `|` 사이의 값을, 존재하지 않거나 비어있으면 `|` 뒤의 값을 사용한다. ex) `%(chapters&has chapters|no chapters)s`
6. 기본 문자열: `|` 를 사용한다. ex) `%(uploader|Unknown)s` . `|` 앞에 여러 값이 있으면 그 중에 모두 없는 경우에 `|` 뒤의 값을 넣는다.

## 1.3. 컴프리헨션

파이썬만의 특징 중 하나로, 이터러블한 객체를 간결하고 효율적으로 만들 수 있도록 해주는 문법들이다. 반복문과 조건문을 조합해 한 줄로 리스트를 생성할 수 있으며, 형태가 정형화되어 있기 때문에 최적화가 잘 적용되어 속도가 for 문보다 빠르다.

- 리스트 컴프리헨션
    
    ```python
    [x * x for x in range(5)]
    # → [0, 1, 4, 9, 16]
    ```
    
- 집합 컴프리헨션
    
    ```python
    {x % 3 for x in range(6)}
    # → {0, 1, 2}
    ```
    
- 딕셔너리 컴프리헨션
    
    ```python
    {x: x * x for x in range(3)}
    # → {0: 0, 1: 1, 2: 4}
    ```
    
- 제너레이터
    
    ```python
    (x * x for x in range(5))
    # → `<generator object ...>`
    # (반복문이나 `next()`로 값을 꺼내 사용)
    ```
    

당연하지만, 이를 2중으로 겹칠 수도 있으며, 가독성이 떨어질 수 있지만 적절하게 사용하면 유용하다.

if 문을 적용하거나 함수를 실행하는 예제는 리스트 컴프리헨션을 예시로 들겠다. 다른 경우에도 비슷하게 적용할 수 있다.

1. **조건 필터링 (`if`를 맨 뒤에)**
    
    ```python
    [x for x in range(10) if x % 2 == 0]
    ```
    
    → `[0, 2, 4, 6, 8]`
    
2. **`if-else` 표현식 사용**
    
    ```python
    ["even" if x % 2 == 0 else "odd" for x in range(5)]
    ```
    
    → `['even', 'odd', 'even', 'odd', 'even']`
    
3. **리턴값이 없는 함수 실행 (부수 효과)**
    
    ```python
    [print(x) for x in range(3)]
    ```
    
    출력:
    
    ```
    0
    1
    2
    ```
    
4. **함수의 반환값으로 리스트 만들기**
    
    ```python
    def tag(x): return f"<li>{x}</li>"
    [tag(item) for item in ["apple", "banana", "cherry"]]
    ```
    
    → `['<li>apple</li>', '<li>banana</li>', '<li>cherry</li>']`
    

## 1.4. 주소에 의한 참조의 변경

### 1.4.1. 리스트

```python
lst = [1, 2, 3]
foo = lst
foo[0] = 5
# lst = [5, 2, 3]
```

리스트는 주소에 의한 참조를 하기 때문에 같은 식으로 접근하여 `foo`를 수정할 시 `lst`도 수정된다. 이는 예기치 않은 문제를 낳을 수 있으므로 리스트를 수정할 때에는 아래와 같은 방법을 사용해야 한다.

1. 리스트 컴프리헨션
    
    리스트 컴프리헨션은 새로운 리스트를 만드므로 이 경우에 사용할 수 있다. 단순히 이전 리스트를 그대로 리스트 컴프리헨션으로 다시 만드는 건 실용성이 떨어지고, 추가적인 조건문 등을 적용할 때 고려할 만하다.
    
2. 슬라이싱 사용
    
    `foo = lst[:]` 같은 식으로 사용하면 `lst` 를 맨 처음부터 맨 끝까지 가져온 새 리스트를 만들어 변수에 대입하므로 복제가 된다.
    
3. `copy` 함수 사용
    
    리스트를 복제하는 함수는 여러가지가 있다. 리스트 내에도 `copy` 메서드가 있으며(위의 슬라이싱과 동일하게 복제된 리스트를 반환한다), `copy` 모듈의 `copy(객체)` 형태의 함수를 사용할 수도 있다.
    

위의 방법들은 모두 얕은 복사로, 리스트 자체는 복제되지만 그 안에 다른 리스트 같이 주소를 참조하는 객체가 있다면 그 객체는 여전히 주소를 참조한다. 내부에 있는 객체까지 모두 복제하려면 깊은 복사를 해야 한다. 이는 `copy` 모듈의 `deepcopy` 함수를 사용하면 된다.

### 1.4.2. 함수(센티널 패턴)

```python
def foo(lst=[1, 2]):
    lst += [3]
    return lst
    
foo() 
# [1, 2, 3]
foo()
# [1, 2, 3, 3]
```

함수의 인자에 기본값으로 변경 가능한 객체를 넣는 것은 위험하다. 이는 해당 기본값이 계속 같은 주소를 참조하기 때문이다. 이 때문에 함수 내에서 기본값을 수정하게 되면 이후에도 기본값이 수정된 상태로 변경된다. 수정이 아니라 인자에 새 값을 대입하는 것은 기본값 객체 [1, 2]는 그대로고 변수에 대입하는 것이기 때문에 상관없다.

이를 해결하는 방법은 두가지가 있다.

1. 튜플은 변경 불가능하므로, 기본값으로 넣어도 안전하다. 변경 불가능한 객체라면 해당 객체가 변경될 수 없으므로 새로운 객체를 만들어서 반환하기 때문에 원래 객체가 바뀌지는 않는다.
    
    ```python
    def bar(x=(1, 2)):
        x += (3,)
        return x
    
    bar() # (1, 2, 3)
    bar() # (1, 2, 3)
    
    def bar(x=()):
        print("Before:", id(x), x)
        x += (1,)
        print("After :", id(x), x)
        return x
    
    bar()
    #Before: 140041... ()
    #After : 140042... (1,)
    bar()
    #Before: 140041... ()
    #After : 140043... (1,)
    # 초기 주소는 같지만(=초기값 ()는 동일한 객체이지만), += 이후에는 새 객체가 생긴다
    ```
    
2. 센티널 패턴
    
    센티널 패턴은 인자에 기본값으로 변경 가능한 객체를 넣어야 할 때 대신 `None`을 넣고, 내부에서 None인지 확인해서 기본값을 설정하는 방법이다.
    
    ```python
    def foo(x=None):
        if x is None:
            x = []
    
    # None도 인자로 사용해서 구분이 필요할 때
    _sentinel = object()
    
    def foo(x=_sentinel):
        if x is _sentinel:
            x = []
    ```
    

## 1.5. 타입 힌팅

### 1.5.1. 사용 이유

타입 힌팅은 동적 언어인 파이썬에서 변수의 타입을 명시하는 것이다. 타입을 틀리게 사용해도 작동에는 이상이 없지만, mypy 같은 타입 체커를 사용한다면 경고를 띄워준다. 이는 코드가 길어지고 복잡해질 때 실수로 잘못된 타입을 넣는 것을 방지해준다.

예시

1. 리스트에 딕셔너리를 합침
    
    ```python
    my_list = []
    my_dict = {"a": 1}
    my_list += my_dict  # 오류 없이 작동하지만 리스트에는 키만 들어간다: ["a"]
    
    my_list: list = []
    my_dict: dict = {"a": 1}
    my_list += my_dict # 이 경우 경고를 띄운다.
    ```
    
2. 서로 다른 타입이 섞인 리스트가 있음
    
    ```python
    from rich import Style
    lst = [Style("red"), "green"]
    for i in lst:
        i += Style(bold=True)
        # 두번째 요소에서 오류가 남. Style 객체는 다른 Style 객체와만 합칠 수 있음
        
    # 이 경우에 lst를 아래와 같게 적으면 미리 경고를 해준다
    lst: list[Style] = [Style("red"), "green"]
    ```
    

또한 `Literal`이나 `TypedDict` 등의 타입 힌트를 사용하면 들어갈 종류가 정해지므로 IDE에서 자동완성을 할 수 있다. 이를 통해 편리하게 들어갈 타입을 알릴 수 있다.

### 1.5.2. 이외 타입 힌트들

자세하고 구체적인 기능을 제공하는 것들은 `typing` 모듈에서 제공한다. 

원래 특정 객체가 들어간 리스트(`List[str]`), 튜플(`Tuple[int]`)이나 여러 타입 중 하나를 나타내는 타입(`Union[int, str]`)도 이 모듈로만 나타낼 수 있었는데, 이후 버전에서 업데이트 되면서 기본 파이썬에서 `list[str], tuple[int], int | str` 와 같은 형식으로 나타낼 수 있게 되었다.

1. 튜플: 다음 페이지에 자세하게 정리하였다. [튜플의 요소의 갯수별 타입 힌트](./docs/튜플의_요소의_갯수별_타입_힌트.md)

2. `TypedDict`: 정해진 키를 가진 딕셔너리를 타입 안전하게 다룸
    
    ```python
    from typing import TypedDict
    
    class User(TypedDict): # 이 이외의 타입을 넣으면 경고가 뜬다. 
    # class User(TypedDict, total=False):  같은 식으로 정의하면 이외의 값도 허용한다.
        name: str
        age: int
    
    def greet(user: User) -> str:
        return f"안녕하세요, {user['name']}님! 나이는 {user['age']}세입니다."
    ```
    
3. `Self`: 메서드가 자기 자신을 반환할 때 사용
    
    ```python
    from typing import Self
    
    class Counter:
        def __init__(self) -> None:
            self.value = 0
    
        def increment(self) -> Self:
            self.value += 1
            return self  # 체이닝 가능: counter.increment().increment()
    ```
    
4. `Any` : 아무 타입이나 허용, 타입 검사 무시
    
    ```python
    from typing import Any
    
    def process(data: Any) -> None:
        print(data)  # data는 어떤 타입이든 허용
    ```
    
5. `TypeGuard` : 사용자 정의 타입 판별 함수 정의
    
    ```python
    from typing import TypeGuard
    
    def is_str_list(val: list[object]) -> TypeGuard[list[str]]:
        return all(isinstance(x, str) for x in val)
    
    def handle(data: list[object]):
        if is_str_list(data):
            print("문자열 리스트입니다:", data)  # data를 list[str]로 추론 가능
        else:
            print("문자열 리스트가 아닙니다.")
    ```
    
6. `Literal` : 정해진 값들만 허용
    
    ```python
    from typing import Literal
    
    def set_mode(mode: Literal["r", "w", "a"]) -> None:
        print(f"모드가 {mode}로 설정되었습니다.")
    
    set_mode("r")  # ✅
    set_mode("x")  # ❌ mypy 등 정적 분석기가 경고
    ```
    

## 1.6. 클래스

파이썬은 추상화된 클래스의 재사용과 상속을 통해 개발의 편의성과 효율성을 추구하는 객체 지향적 언어이다. 이에 따라, 파이썬에서 가장 중요한 개념 중 하나는 클래스라고 말할 수 있다.

아래의 내용 외에도 내가 따로 정리해둔 개념을 여기 기록한다.

참고한 링크들

- [파이썬 코딩 도장: 36.5 다중 상속 사용하기](https://dojang.io/mod/page/view.php?id=2388)

- [4-8. Multiple Inheritance(다중상속)](https://wikidocs.net/234375)

- [파이썬 클래스 상속, 오버라이딩, 다중상속, 추상 클래스](https://velog.io/@yeonu/%ED%8C%8C%EC%9D%B4%EC%8D%AC-%ED%81%B4%EB%9E%98%EC%8A%A4-%EC%83%81%EC%86%8D)

- [[ Python 3 ] 클래스의 super( ) 에 대해 제대로 알아보자! ( super().__init__(), super()의 위치)](https://supermemi.tistory.com/entry/Python-3-%ED%8C%8C%EC%9D%B4%EC%8D%AC-%ED%81%B4%EB%9E%98%EC%8A%A4%EC%9D%98-super-%EC%97%90-%EB%8C%80%ED%95%B4-%EC%A0%9C%EB%8C%80%EB%A1%9C-%EC%95%8C%EC%95%84%EB%B3%B4%EC%9E%90-superinit-super%EC%9D%98-%EC%9C%84%EC%B9%98)

정리해 둔 gpt와의 대화
- 기본 개념 및 클래스 구조
  - [내부 클래스](./docs/내부_클래스.md)
  - [추상 클래스](./docs/추상_클래스.md)
  - [추상화하는 경우와, 다중상속 주의사항](./docs/추상화하는_경우와,_다중상속_주의사항.md)

- 상속 및 다중상속 관련
  - [상속과 다중상속에서의 타입 맹글링](./docs/상속과_다중상속에서의_타입_맹글링.md)
  - [다중상속](./docs/다중상속.md)
  - [다중상속-super와 kwargs](./docs/다중상속-super와_kwargs.md)

- 기타 유틸리티 및 함수 관련
  - [데코레이터 및 staticmethod 주의사항](./docs/데코레이터_및_staticmethod_주의사항.md)
  - [dataclass와 특수 메직 메서드](./docs/dataclass와_특수_메직_메서드.md)
  - [self 없이 사용하는 것들](./docs/self_없이_사용하는_것들.md)
  - [유틸리티 클래스](./docs/유틸리티_클래스.md)

### 1.6.1. 클래스 변수

클래스 변수는 **클래스 전체에서 공유되는 변수**로, 인스턴스 간에 값을 공유한다.

```python
class MyClass:
    count = 0  # 클래스 변수

    def __init__(self):
        MyClass.count += 1

A = MyClass()
# A.count = 1
B = MyClass()
# A.count = 2
# B.count = 2
MyClass.count = 10
# A.count = 10
# B.count = 10
A.count = 3
# B.count = 10
# MyClass.count = 10
```

- `MyClass.count`는 모든 인스턴스가 공유
- 인스턴스에서 `self.count`로 접근하면 같은 값이지만, 인스턴스에서 값을 바꾸면 **새로운 인스턴스 변수**가 생김

---

### 1.6.2. 메직 메소드 (Magic Method)

파이썬에서 `__init__`, `__str__`, `__iter__` 같은 특수 이름의 메소드는 **특정 동작을 자동으로 연결해줌**.

1.  `__enter__`와 `__exit__` – with 문 컨텍스트 관리
    
    ```python
    class Resource:
        def __enter__(self):
            print("자원 열기")
            return self
    
        def __exit__(self, exc_type, exc_val, exc_tb):
            print("자원 닫기")
    
    with Resource() as r:
        print("작업 중")
    
    ```
    
    - `with` 문 진입 시 `__enter__`, 종료 시 `__exit__` 자동 호출
2.  `__init__`과 `__post_init__` – 생성자와 후처리 (dataclass 전용)
    
    ```python
    from dataclasses import dataclass
    
    @dataclass
    class Item:
        name: str
        price: int
    
        def __post_init__(self):
            if self.price < 0:
                raise ValueError("가격은 0 이상이어야 합니다.")
    
    ```
    
    - `__init__`은 객체 생성 시 자동 실행
    - `__post_init__`은 `dataclass`에서 생성자 다음에 실행되는 후처리 함수
3.  `__iter__`와 `__next__` – 반복자 구현
    
    ```python
    class CountUp:
        def __init__(self, limit):
            self.current = 0
            self.limit = limit
    
        def __iter__(self):
            return self
    
        def __next__(self):
            if self.current < self.limit:
                self.current += 1
                return self.current
            raise StopIteration
    
    ```
    
    - `for` 루프에서 객체를 사용할 수 있게 함
    - `__iter__`는 자기 자신(또는 반복자)을 반환해야 하고, `__next__`는 다음 값을 반환

---

### 1.6.3. 상속

상속은 **기존 클래스를 기반으로 새로운 클래스를 정의**하는 기능이다.

```python
class Animal:
    def speak(self):
        print("소리를 낸다")

class Dog(Animal):
    def speak(self):
        print("멍멍")

```

- `Dog`는 `Animal`을 상속받아 `speak`를 오버라이딩

---

### 1.6.4. 다중상속

다중상속은 여러 클래스로부터 동시에 상속받는 기능이다.

```python
class A:
    def method(self):
        print("A")

class B:
    def method(self):
        print("B")

class C(A, B):
    pass

c = C()
c.method()  # A → MRO(Method Resolution Order)에 따라 A 우선

```

- 파이썬은 C3 선형화 방식으로 메서드 탐색 순서를 정의함

---

### 1.6.5. 추상 클래스

추상 클래스는 직접 인스턴스를 만들 수 없으며, **필수 구현 메서드**를 강제한다.

```python
from abc import ABC, abstractmethod

class Shape(ABC):
    @abstractmethod
    def area(self) -> float:
        pass

class Circle(Shape):
    def __init__(self, r: float):
        self.r = r

    def area(self) -> float:
        return 3.14 * self.r * self.r

```

- `Shape`는 `area` 구현을 강제함
- `Circle`은 반드시 `area`를 구현해야 객체 생성 가능

---

### 1.6.6. `@staticmethod`와 유틸리티 클래스

- `@staticmethod`는 **인스턴스나 클래스와 무관하게 작동**하는 메서드
- 유틸리티 클래스는 상태 없이 함수 모음 역할을 하는 클래스

```python
class MathUtil:
    @staticmethod
    def square(x):
        return x * x

print(MathUtil.square(4))  # 16

```

- `self`, `cls`를 사용하지 않기 때문에 독립적인 유틸리티 함수로 적합

## 1.7. 기타 개념

### 1.7.1. 언패킹

리스트, 딕셔너리는 각각 `*`와 `**`를 통해 언패킹할 수 있으며, 함수 등에 인자로 전달할 때 유용하다.

```python
lst = ["철수", "영희"]
dictionary = {"a":4, "b":5}

def foo(name1, name2, a, b):
    pass
    
foo(*lst, **dictionary)
# foo("철수", "영희", a=4, b=5)와 동일
```

이를 이용하면 `…` 형식으로 인자를 받는 경우에도 (즉, 인자의 기본값이 없어 기본값으로 전달하지 못하는 경우에도) 인자를 전달할지 여부를 선택할 수 있다.

```python
def foo(a=1, b=...):  # b는 기본값이 없다는 의도 표현. 기본값으로 None을 사용하지 않은 것은 None도 유효한 값으로 사용될 수 있기 때문이다.
    print("a:", a)
    print("b:", b)
    
# 인자 하나만 넘긴 경우: b는 기본값 Ellipsis가 그대로 들어감
d1 = {"a": 2}
foo(**d1)  
# 출력: a: 2, b: Ellipsis

# b도 명시적으로 전달한 경우
d2 = {"a": 3, "b": 4}
foo(**d2)
# 출력: a: 3, b: 4
```

### 1.7.2. 함수에서의 인자에 * 사용

함수에서 `*인자명`을 사용하면 튜플로 인자를 받는다는 의미이고, `**인자명`을 사용하면 딕셔너리 형식으로 인자를 받는다는 의미이고 그냥 `*`만 사용하면 그 뒤는 전부 명시적으로 받는다는 의미이다.

```python
def foo(a, *args):
    print("a:", a)
    print("args:", args)

foo(1, 2, 3, 4)
# a: 1
# args: (2, 3, 4)

def bar(a, **kwargs):
    print("a:", a)
    print("kwargs:", kwargs)

bar(1, x=10, y=20)
# a: 1
# kwargs: {'x': 10, 'y': 20}

def baz(a, *, b, c):
    print("a:", a)
    print("b:", b)
    print("c:", c)

baz(1, b=2, c=3)  # ✅ OK
# baz(1, 2, 3)    # ❌ 에러: b, c는 반드시 이름을 붙여서 전달해야 함
```

### 1.7.3. 람다식과 함수

| 항목 | `lambda` 표현식 | 일반 함수 정의 (`def`) |
| --- | --- | --- |
| 문법 | `lambda x: x + 1` | `def f(x): return x + 1` |
| 구조 | 단일 표현식만 가능 | 여러 줄 가능 |
| 이름 | 익명 (보통 변수에 대입) | 명시적 이름 존재 |
| 사용 용도 | 주로 인자로 전달하거나 짧은 일회성 처리용 | 일반적인 기능 정의 |
| 디버깅 | `<lambda>`로 표시되어 추적 어려움 | 함수 이름이 traceback에 표시됨 |
| 확장성 | 문서화/타입힌트 어려움 | docstring, type hint, 리팩터링 용이 |

▸ 인자 하나

```python
f = lambda x: x * 2
print(f(3))  # 6
```

▸ 인자 여러 개

```python
add = lambda x, y: x + y
print(add(2, 3))  # 5
```

▸ 인자 없음

```python
hello = lambda: "Hello"
print(hello())  # Hello
```

▸ 디버깅이 불리한 예

```python
f = lambda x: x * 2
# 에러 발생 시 함수 이름은 <lambda>로 표시되어 추적 어려움
```

권장: 한 줄 함수라도 def로 작성

```python
def double(x): return x * 2
# 이름이 있으므로 추적과 디버깅에 유리
```

람다식은 **일회성 함수가 필요한 곳의 인자**로 많이 사용됨.

▸ 예: `sorted()`에서 키 정렬

```python
names = ["Alice", "bob", "charlie"]
sorted_names = sorted(names, key=lambda x: x.lower())
```

▸ 예: `map()`과 `filter()`

```python
nums = [1, 2, 3, 4]
squares = list(map(lambda x: x**2, nums))      # [1, 4, 9, 16]
evens = list(filter(lambda x: x % 2 == 0, nums))  # [2, 4]
```

> 이렇게 짧고 이름이 필요 없는 경우에만 lambda를 사용하는 것이 좋다.
> 

### 1.7.4. for문과 enumerate에서의 del

```python
lst = [1, 2, 3, 4, 5]

for idx, val in enumerate(lst):
    if val % 2 == 0:
        del lst[idx]  # ❌ 위험!

```

문제가 생기는 이유

- `for` 루프는 내부적으로 **인덱스를 자동 증가**시키며 순회함
- 그런데 `del lst[idx]`로 중간에 요소를 삭제하면,
    - 리스트 길이가 줄어들고
    - **인덱스가 밀리게 되어** 건너뛰는 요소가 생김
- 결과적으로 **의도한 요소가 일부 삭제되지 않거나**, **IndexError**가 발생할 수 있음

예시:

```python
lst = [1, 2, 3, 4, 5]
for idx, val in enumerate(lst):
    print(f"{idx=}, {val=}")
    if val == 2:
        del lst[idx]  # 이후 순회가 꼬임

```

안전한 대안 1: 리스트 컴프리헨션

**삭제가 아니라 "필요한 요소만 남기는 방식"으로 해결**

```python
lst = [1, 2, 3, 4, 5]
lst = [x for x in lst if x % 2 != 0]
print(lst)  # [1, 3, 5]

```

- 읽기 쉽고
- **원본을 건드리지 않고 새로운 리스트 생성**하므로 안전

대안 2: 새 리스트에 조건 만족하는 요소만 추가

```python
original = [1, 2, 3, 4, 5]
filtered = []

for x in original:
    if x % 2 != 0:
        filtered.append(x)

print(filtered)  # [1, 3, 5]

```

- 더 명시적인 방식
- 조건이 복잡하거나 디버깅이 필요한 경우 적절함

대안 3: 뒤에서부터 삭제 (역순 루프)

```python
lst = [1, 2, 3, 4, 5]

for i in range(len(lst) - 1, -1, -1):
    if lst[i] % 2 == 0:
        del lst[i]

print(lst)  # [1, 3, 5]

```

- 리스트를 뒤에서부터 삭제하면 **앞쪽 인덱스에 영향을 주지 않음**
- 하지만 여전히 **루프에서 직접 삭제**하는 것은 복잡도와 오류 위험이 있음

### 1.7.5. sum 함수

`sum` 함수는 기본적으로 정수에서만 작동하는데, 그 이유는 그 함수가 정수만 받을 수 있어서가 아니라 (실제로도 내부를 보면 이터러블 전부를 받을 수 있다), 초기값이 0으로 되어 있기 때문이다.

내부 구조는 이렇게 되어 있다.

```python
def sum(iterable: Iterable[bool | _LiteralInteger], /, start: int = 0)
```

start를 더할 값들과 같은, 오류가 나지 않는 타입으로 바꾸면 TypeError가 나지 않는다.

```python
lists = [[1, 2], [3], [4, 5]]
print(sum(lists, start=[]))  # ➜ [1, 2, 3, 4, 5]
```

다만 문자열은

```python
    print(sum(["h", "e", "l", "l", "o"], start=" "))
          ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
TypeError: sum() can't sum strings [use ''.join(seq) instead]
```

이렇게 오류가 나는데, 기술적으로 이게 불가능해서 막은 게 아니라 join 메서드가 성능상으로 낫기 때문에 이를 대신 사용하라고 권고하는 것이다.

### 1.7.6. sort에서의 키 설정

`sort`나 `sorted`의 `key` 인자는 **정렬 기준이 되는 값을 반환하는 함수**를 지정한다.

```python
sorted(iterable, key=기준함수)
```

1. 문자열 길이로 정렬
    
    ```python
    words = ["apple", "banana", "kiwi", "grape"]
    sorted_words = sorted(words, key=len)
    print(sorted_words)
    # ['kiwi', 'grape', 'apple', 'banana']
    
    ```
    
    - `key=len`은 문자열의 길이를 기준으로 정렬한다.
2. 튜플의 두 번째 요소 기준 정렬
    
    ```python
    data = [("Alice", 25), ("Bob", 20), ("Charlie", 23)]
    sorted_data = sorted(data, key=lambda x: x[1])
    print(sorted_data)
    # [('Bob', 20), ('Charlie', 23), ('Alice', 25)]
    
    ```
    
    - `lambda x: x[1]`은 각 튜플의 두 번째 요소를 기준으로 정렬한다.
3. 대소문자 구분 없이 정렬
    
    ```python
    words = ["banana", "Apple", "cherry"]
    sorted_words = sorted(words, key=str.lower)
    print(sorted_words)
    # ['Apple', 'banana', 'cherry']
    
    ```
    
    - `str.lower`를 기준 함수로 사용하여 대소문자를 무시하고 정렬한다.

# 2. 코드 구조

### 2.1. 기본 구조

주요 구조만을 설명한다. 설명명은 개발이 완료된 VD4를 기준으로 한다.

기본적으로 플레이리스트 하나당의 정보를 하나의 `Videos`에 담아서 다룬다. 그리고 여기에 정보를 담고 일괄적으로 관리하며 다운로드하는 것은 `VideosManager`가 수행한다. rich의 기능들이나 다른 서브모듈들은 이를 보조하고 결과를 출력하는 등의 기능을 한다.

```python
# 사용법
manager = VideosManager(
     Videos(
         "https://www.youtube.com/playlist?list=exmaple1",
         inner_folder_split="%(uploader)s",
         artist_name="%(uploader)s",
     ),
    "https://www.youtube.com/playlist?list=example2", 
    "https://www.youtube.com/@channel1", 
    parent_videos_dir="C:\\Users\\user\\Desktop\\영상 폴더",
    parent_file_dir="C:\\Users\\user\\Desktop\\정보 폴더",
)

manager.show_total_info()
ask.ask_continue("전체 표를 출력하시겠습니까?")
manager.show_total_table([
    'title',
    "playlist",
    "uploader",
    ('upload_date', formatstr.date)],
)

answer = ask.ask_choice(
"어떤 방식으로 다운로드 하시겠습니까?",
["영상 파일", "음악 파일", "다운로드 안함"],
"다운로드 안함",
)
if answer == "영상 파일":
    manager.download_as_video()
elif answer == "음악 파일":
    manager.download_as_music()
else:
    pass
```

세세한 내용을 설정하려면 `Videos` 객체를 만들고 설정할 수 있고, 그렇지 않으면 그냥 링크만 넣어도 내부에서 `Videos` 객체로 만들어서 다룬다.

각 파일별 함수의 역할

### 2.2. `VideosManager`

- `__init__`:
    1. 파일을 저장할 경로와 영상/음악 파일을 저장할 경로를 따로 설정할 수 있다. 또한 개별 비디오의 정보를 강제 업데이트할지 여부와, 기본 스타일을 설정할 수 있다.
    2. 일련의 `Videos`객체 또는 url 문자열을 받아서 이를 `Videos` 객체로 바꾸고, 설정한 경로에 맞게 폴더를 만든다. 
    3. url을 통해 플레이리스트의 flat한 정보를 가져오고, 이를 바탕으로 각 영상의 구체적인 정보를 멀티스레딩을 통해 가져온다. 각각은 json 파일로 각각의 폴더에 저장된다
        - `__bring_playlist_json`: 플레이리스트 폴더에서 플레이리스트 정보를 찾아오고, 없으면 `ydl_tools`의 `bring_playlist_info`를 사용해 정보를 가져온다.
        - `__bring_detailed_info`: 개별 영상에 대해 정보를 json 파일에서 가져오길 시도하고 존재하지 않으면 `ydl_tools`의 `bring_video_info`를 통해 정보를 읽어온다.
        - `__bring_detailed_info_list`: 위의 함수를 멀티스레딩을 통해 실행하며 진도를 프로그래스 바로 출력하는 함수이다.
    4. `Videos` 객체 내의 경로들과 영상 정보 등을 설정한다.
    5. 스타일이 따로 지정되지 않았다면, 플레이리스트 정보에서 채널 정보를 확인하고 채널 정보를 가져온 후, 썸내일을 다운로드해 색상을 분석한다. 최대 3개의 색만이 필요하기에 그 중 가장 비중이 큰 3개의 색을 스타일로 설정한다. 한번 설정한 스타일은 json에 저장해 다음에 썸내일을 다운로드하고 분석할 필요가 없게 만든다.
        - `__get_thumbnail_colors`: `request`로 썸내일을 다운받고, `extcolors`로 색을 추출한다.
    6. 자신의 비디오스 리스트에 각 `Videos`들을 넣는다.
- `set_to_download_list`: 비디오스들을 다운할 비디오스 목록으로 설정한다.
- `show_total_table`: 지정한 키에 따라 전체 영상들의 정보를 담은 표를 만든다. 인자로는 키의 이름과 그 키에 적용할 포멧팅 함수(날짜의 형태를 yy.mm.dd로 바꾸는 등)를 튜플로 받는다. 표의 형태(테두리 등)를 설정할 수 있으며 띄울 비디오를 제한할 수 있다. 값들을 설정한 후 rich_VD4의 `make_info_table` 함수로 표를 만든다.
- `show_total_info`, `show_total_head`: 단순히 비디오스 내의 info나 head를 출력하는 함수를 반복적으로 호출한다.
- `__download` : 일련의 비디오스를 다운로드하는 함수이다. 다운로드 아카이브를 참조해 이미 다운로드된 영상의 갯수를 바에 띄운다. 전체 다운로드의 프로그래스 바를 만들고 `프로그래스 훅`으로 다운로드 진도와 영상 이름 등을 표시한다.
    - `DLLogger` : 비디오 다운로드시 사용하는 로거이다. `LoggerForRich` 를 상속하여 rich의 출력에 적용할 수 있게 하고, 기존 yt-dlp의 로그를 패널로 감싸 프로그래스 바와 함께 출력한다. 이를 위해 rich의 live를 사용한다.
    - `download_as_video`, `download_as_music` : `__download` 를 실행한다.

### 2.3. `Videos`

기본적으로 정보를 담는 기능을 하고, 개별 비디오스의 표 등을 출력할 수 있다.

- `MAJOR_KEYS` : 주요한 키들을 Literal로 지정한다.
- `InfoDict` : 주요한 키가 든 딕셔너리를 타입 힌트로 지정한다.
- `__init__`: 가져올 비디오의 조건을 지정하는 함수, 플레이리스트의 제목 변경, 내부 폴더를 나눌 이름(%(uploader)s 등), 챕터를 쪼갤지 여부, 스타일, 플레이리스트 json을 업데이트할지, 작곡가와 엘범의 이름을 설정할 수 있다. 추가 키를 VideosManager에서 설정할 수 있으며, 설정하지 않을 시 기본으로 중복 여부와 다운로드 여부가 들어간다.
- 영상을 모든 영상 / 다운로드 가능 / 불가능 / 중복됨으로 나눠 리스트로 관리한다. 이때 모든 영상을 기본적으로 다루고, 나머지 리스트는 여기서 분류해 넣는 형태이다.
- `change_value` : init에서 설정한 값을 바꿀 수 있다.
- `update`: 위의 리스트를 재분류하고 정렬하며, style을 다른 함수 등에서 오류나지 않게 지정하며 영상들에 대해 추가 키를 추가한다.
- `info`, `head` : 전자는 정보를 색이 입혀진 패널이 씌워진 문자열로 내보내며, 후자는 초기 5개의 영상 정보를 출력한다.
- `sort` : 키값과 오름차순 여부를 기준으로 리스트를 정렬한다.
- `cut` : 파이썬의 슬라이싱과 같다. 새 객체를 반환할지 여부를 정할 수 있다.
- `filtering, filtering_keyword` : 전자는 조건을 주면 해당 조건에 맞는 걸 필터링하고, 후자는 키워드 문자열들을 주면 제목, 설명, 댓글에서 해당 키워드가 있는 걸 필터링한다.
- `bring_da_list`: 다운로드 아카이브를 읽어온다
- `show_table` : 위의 표 출력과 동일하다.
- `calculate_table_info` : VideosManager에서 전체 표를 출력할 때 또는 여기서 표를 출력할 때 하단에 적힐 정보를 계산한다.
- `__add__, __sub__, __and__`: 자신과 다른 비디오스의 영상 목록에 대해 합, 차, 교집합을 수행한다.
    - `dict_list` 의 `dict_set_union, dict_set_diff, dict_set_inter` : 각각 합, 차, 교집합을 정의한다. 객체를 집합으로 만드는 건 int 같은 변경 불가능한 값이 있을 때에만 가능해서, json 형식으로 바꾸고 연산한 뒤 다시 딕셔너리로 바꾼다.

# 3. 개선 사항

### 3.1. 적용된 개선 사항

- 집합의 연산을 유틸리티 클래스로 묶는다.
    
    ```python
    class DictSetOperator: # 이 구조를 추상화한다.
        """여차하면 이거 내부 클래스로 통합할 수도?"""
        @staticmethod
        def union(list1: list[VideoInfoDict | EntryInPlaylist], list2: list[VideoInfoDict | EntryInPlaylist]) -> list[VideoInfoDict | EntryInPlaylist]:
            """합집합"""
            set1 = {json.dumps(item, sort_keys=True) for item in list1}
            set2 = {json.dumps(item, sort_keys=True) for item in list2}
    
            # 집합 연산 수행
            sum_json = set1 | set2
    
            # JSON 문자열을 다시 딕셔너리로 변환
            sum_ = [json.loads(item) for item in sum_json]
    
            return sum_
    
        @staticmethod
        def diff(list1: list[VideoInfoDict | EntryInPlaylist], list2: list[VideoInfoDict | EntryInPlaylist]) -> list[VideoInfoDict | EntryInPlaylist]:
            """차집합"""
            set1 = {json.dumps(item, sort_keys=True) for item in list1}
            set2 = {json.dumps(item, sort_keys=True) for item in list2}
    
            # 집합 연산 수행
            diff_json = set1 - set2
    
            # JSON 문자열을 다시 딕셔너리로 변환
            difference = [json.loads(item) for item in diff_json]
    
            return difference
    
        @staticmethod
        def inter(list1: list[VideoInfoDict | EntryInPlaylist], list2: list[VideoInfoDict | EntryInPlaylist]) -> list[VideoInfoDict | EntryInPlaylist]:
            """교집합"""
            set1 = {json.dumps(item, sort_keys=True) for item in list1}
            set2 = {json.dumps(item, sort_keys=True) for item in list2}
    
            # 집합 연산 수행
            inter_json = set1 & set2
    
            # JSON 문자열을 다시 딕셔너리로 변환
            intersection = [json.loads(item) for item in inter_json]
    
            return intersection
    ```
    
- 표는 `VideosManager`와 `Videos`둘 다 사용하고 구조가 겹치므로, 아래와 같이 추상화하여 각각에서 상속하여 사용한다. 이때 키를 다루기 위한 클래스를 하나 정의하고, 문자열로도 이를 재현할 수 있게 해 유연성을 높인다.
    
    ```python
    @dataclass
    class TableKey:
        """표에 사용되는 구체적인 키 설정. alias는 생성하지 않았을 시 자동으로 key로 설정"""
        @staticmethod
        def return_str(value) -> str:
            # 람다 경고 회피. 그리고 직접 정의보다 이게 더 직관적인듯?
            # gpt는 그냥 str(함수니까) 쓰면 된다 하는데, 나중에 내가 햇갈릴거 같아서
            return str(value)
    
        key: str
        alias: str = ""
        formatter: Callable[..., str] = return_str
        formatter_kwargs: dict[str, Any] = field(default_factory=dict)
    
        def __post_init__(self):
            if self.alias == "":
                self.alias = self.key
    
    class VideosTableMixin(ABC):  # 이건 메니져에서도 상속.
        # 기본 표 키 정의
        default_keys_to_show: tuple[TableKey, ...] = (
            TableKey("title"),
            TableKey("upload_date", formatter=FormatStr.date),
            TableKey("view_count", formatter=FormatStr.number),
            TableKey("like_count", formatter=FormatStr.number),
            TableKey("duration", formatter=FormatStr.time),
            TableKey("filesize_approx", formatter=FormatStr.bytes)
        )
    
        @property
        @abstractmethod
        def videos_list_for_table(self) -> list["Videos"]:
            """return [self]같은 식으로 재정의"""
    
        def print_table(self,
                        *keys: str | tuple[str, Callable[[Any], str]] | TableKey,
                        restrict: Callable[[VideoInfoDict |
                                            EntryInPlaylist], bool] = None,  
                        box_: box.Box | None = box.HEAVY_HEAD,
                        show_lines: bool = False,
                        skow_edge: bool = True,
                        expand: bool = False,
                        no_wrap: bool = False,
                        highlight: bool = False
                        ) -> None:
            """
            테이블을 만드는 건 여기서.
    
            Args:
                keys: 아래의 형태 중 하나가 들어갈 수 있음
                    - 딕셔너리의 키가 되는 문자열
                    - (키, 포메팅 함수) 형태의 튜플 (※함수는 하나의 인자만 가능)
                    - TableKey 객체. 키, 표시할 키의 이름, 포메팅 함수, 포메팅 함수에 전달할 인자를 설정 가능
                restrict: 제한할 조건 
    
            """
            new_keys: list[TableKey] = []
            for key in keys:
                if isinstance(key, str):
                    new_keys.append(TableKey(key))
                elif isinstance(key, tuple):
                    k, formatter = key
                    new_keys.append(TableKey(k, formatter=formatter))
                elif isinstance(key, TableKey):
                    new_keys.append(key)
                else:
                    raise TypeError(f"지원하지 않는 키 형식({type(k)})입니다: {k}")
    
            # 각 요소에 대한 정보를 지닌 리스트
            _columns_str: list[str] = ["index"] + [tk.alias for tk in new_keys]
            columns: list[Column] = [
                Column("index", max_width=5, no_wrap=no_wrap)] + [Column(tk.alias, no_wrap=no_wrap) for tk in new_keys]  # 전과는 달리 뒤쪽은 max 지정 안함. 일단은
            # columns에서 일반 색/어두운 색으로 구체화 << 이거 보기에 안좋아서 그냥 box.HEAVY_HEAD로 줄 나눔
    
            # 만약 비디오스에서 호출한거면 정렬순으로 강조
            if len(self.videos_list_for_table) == 1:
                sort_key, sort_reverse = self.videos_list_for_table[0].sort_by
                if sort_key in columns:
                    idx = _columns_str.index(sort_key)
                    arrow = "▼" if sort_reverse else "▲"
                    columns[idx] = Column(
                        f"[bold bright_magenta]{columns[idx]}{arrow}[/]")
    
                # 일단 pl_folder_name을 사용하는 쪽으로 지정.
                title = f"{self.videos_list_for_table[0].pl_folder_name} Table"
            else:
                title = "Total Table"
    
            # 캡션 달기
            caption = ""
            table_infos: list[dict] = []
            for videos in self.videos_list_for_table:
                caption += f"{videos.format_table_info()}\n"  # 색은 저쪽에서 자동으로 입혀줌
                table_infos.append(videos.calculate_table_info())
            total_table_info = dict(sum((Counter(i)
                                    for i in table_infos), Counter()))
            caption += self.format_table_info(
                total_table_info)
    
            table = Table(
                *columns,
                title=title,
                caption=caption,
                box=box_,
                show_lines=show_lines,
                show_edge=skow_edge,
                expand=expand,
                highlight=highlight,
            )
    
            index = [0]
            if restrict is None:
                def restrict(d) -> Literal[True]:  # pylint: disable=unused-argument
                    return True
            row_styles: list[Style] = []
            for videos in self.videos_list_for_table:
                info_dict_list = [
                    video_dict for video_dict in videos.videos_list.all_videos if restrict(video_dict)]
                self._make_table(table, info_dict_list,
                                 videos.colors, new_keys, index, row_styles)
            table.row_styles = row_styles
    
            my_console.print(table)
    
        def _make_table(self, table: Table,
                        info_dict_list: list[EntryInPlaylist | VideoInfoDict],
                        colors: "Videos._Colors",
                        keys: list[TableKey],
                        latest_idx: list[int],
                        row_styles: list[Style]) -> None:
            """색을 입혀서 열을 지정. 캡션은 밖에서 처리. idx는 밖에서 받아오기"""
            # 색은 끊기거나 덮일까봐, 그냥 밖에서 리스트 두고 스타일을 하나씩 넣은 뒤 나중에 row_styles에 반영
            for video_dict in info_dict_list:  # 각 비디오 딕셔너리마다
                row_style = next(colors)
                row: list[Any] = latest_idx[:]
                for k in keys:
                    row.append(k.formatter(video_dict.get(
                        k.key), **k.formatter_kwargs))
                table.add_row(*map(str, row))
                latest_idx[0] += 1
                # 배경에 색 입히기
                if video_dict.get("availability") != "public":
                    row_style += Style(bgcolor="red", strike=True)
                elif video_dict.get("is_repeated"):
                    row_style += Style(bgcolor="yellow")
                elif video_dict.get("is_downloaded"):
                    row_style += Style(bgcolor="green")
                row_styles.append(row_style)
    
    ```
    
- 내부 클래스는 보통 구조가 종속적인 클래스들을 관리할 때 사용하는데, 스타일과 다운로드 아카이브, 비디오의 목록은 `Videos`에 종속적이므로 내부 클래스로 만든다. 또한 스타일을 이터러블하게 만들고 무한히 반복하게 하면 `next`로 값을 계속 꺼내오면서 매번 다른 색으로 칠할 수 있다. 이를 표의 각 행에 값을 추가할 때마다 적용하여 각 행마다 다른 색으로 칠하면 표의 가독성을 높일 수 있다.
    
    ```python
    class Videos(VideosTableMixin):
        """메인에서 업데이트 호출 > 
        메인 내에서 컬러랑 da 먼저 직접 호출 > 
        비디오스 분류에서 자체 정의 업데이트로 업데이트하고 super 호출 > 
        사칙연산에서 업데이트하고 super 호출 안함.
        """
        class _Colors:
            """햇갈리니까 이름을 color로 바꿈. (원랜 style인데). 반복되는 색은 next(객체명)으로 호출"""
    
            def __init__(self, styles: list[Style | str] | tuple[Style | str, ...] = ("none", "dim")):
                self._idx: int = 0
                self.color_list: list[Style] = [s if isinstance(
                    s, Style) else Style.parse(s) for s in styles]
                self.color: Style = self.color_list[0]
                self.need_setting = True if self.color_list == (
                    "none", "dim") else False
    
            def update(self, styles: list[Style | str] | tuple[Style | str, ...] | None = None):
                """이번에는 스타일스가 한칸짜리면 그냥 냅두기. 이래도 상관 없을 듯. 
                업데이트는 매번 호출하는 게 아니라 한번만 해도 되지 않을까?
                styles 인자는 재설정시 사용
                """
                if styles is not None:
                    self.color_list = [s if isinstance(
                        s, Style) else Style.parse(s) for s in styles]
                self.color_list = [s if isinstance(
                    s, Style) else Style.parse(s) for s in self.color_list]
                self.color = self.color_list[0]
    
            def __iter__(self) -> Self:
                return self
    
            def __next__(self) -> Style:
                if self._idx >= len(self.color_list):
                    self._idx = 0
                result = self.color_list[self._idx]
                self._idx += 1
                return result
    
        class _VideoList:
            def __init__(self) -> None:
                self.all_videos: list[VideoInfoDict | EntryInPlaylist] = []
                self.can_download: list[VideoInfoDict | EntryInPlaylist] = []
                self.cannot_download: list[VideoInfoDict | EntryInPlaylist] = []
                self.downloaded: list[VideoInfoDict | EntryInPlaylist] = []
                self.repeated: list[VideoInfoDict | EntryInPlaylist] = []
    
        class _DownArchive:
            def __init__(self) -> None:
                """여기에 % playlist_info_dict 해야 하는데, 그건 나중에 다운로더에 전달할 때 한꺼번에 함(객체를 더하거나 할 때 바뀔 수 있음)"""
                self.down_archive_path: Path = Path()  # 전체 경로
    
            def set_init(self, dir_: str | Path, type_: str):
                self.down_archive_path = Path(dir_, f"{type_}.archive")
    
            def inherit_other_da(self, other: "Videos._DownArchive") -> None:
                """다른 da로 덮어씌움"""
                other_file = other.down_archive_path.read_text("utf-8")
    
                self.down_archive_path.write_text(other_file, "utf-8")
    
            def sum_with_other_da(self, other: "Videos._DownArchive") -> None:
                """다른 da와 합침"""
                other_file = other.down_archive_path.read_text("utf-8")
                other_lines = other_file.splitlines()
                self_file = other.down_archive_path.read_text("utf-8")
                self_lines = self_file.splitlines()
    
                new_self_text = "\n".join(set(other_lines + self_lines))
                self.down_archive_path.write_text(new_self_text, "utf-8")
    
            def bring_id_list(self) -> list[str]:
                """파일 읽어오기. 딕셔너리에 is_da넣기는 아래에서"""
                da_lines = self.down_archive_path.read_text("utf-8").splitlines()
                return [line.split(" ")[1] for line in da_lines if line]
    
            def check_is_downloaded(self, id_to_check: str) -> bool:
                return id_to_check in self.bring_id_list()
    
    ```
    
- 모듈의 `__init__`에 원래 시작 시에 `yt-dlp` 모듈이 최신 버전인지 확인하고 이를 업데이트하는 함수가 있었는데, `subprocess`로 `pip install —upgrade 모듈명`을 실행할 때 `popen`으로 실시간으로 줄을 출력하고, 이를 `rich`의 패널과 라이브로 업데이트해 깔끔하게 출력한다.
    
    ```python
    def execute_cmd_realtime(command: str, print_: Callable = print, print_kwargs: dict = None, wait: bool = True):
        """run보다 복잡하고 많은 기능을 제공하는 popen 기능 사용
        Args:
            command: 실행할 명령어 문자열
            print_: 출력 함수. 필요시 rich의 console.print로 변경
            print_kwargs: print_에 전달할 인자 목록. rich를 쓸때의 {highlight: True} 등. 없는거 전달달하면 에러나니 주의
            wait: false로 하면 명령어가 끝나는 걸 기다리지 않고 다음 파이썬 구문으로 넘어감
        """
        process = None
        # cmd = shlex.split(command) # 이건 대괄호 들어간 문자열 깨짐
        if print_kwargs is None:
            print_kwargs = {}
    
        program, left_command = command.split(" ", 1)
        print(f"Command: \033[33m{program}\033[0m {left_command}")
    
        try:
            process = subprocess.Popen(
                # cmd,
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1  # 버퍼링 방식 지정. 1줄씩 출력에 필요
            )
    
            if process.stdout is None:
                raise RuntimeError("stdout을 가져오지 못했습니다.")
    
            # Popen이 성공했을 때만 stdout 읽기
            for line in iter(process.stdout.readline, ''):
                print_(line.rstrip(), **print_kwargs)
    
        except Exception:
            # Popen은 성공했는데 실행 중 에러 발생 시 생성된 서브프로세스 종료
            if process:
                process.terminate()
            raise  # 예외 다시 발생
    
        finally:
            if process and wait:
                process.wait()
                
    def check_and_update_in_panel(module_name: str, module_name_to_update: str,
                                  update: bool | Literal["ask"] = "ask", console: Console = None) -> Literal[1] | Literal[0]:
        if console is None:
            new_console = Console()
        else:
            new_console = console
        lines = []
    
        def updater(new_line: str) -> None:
            lines.append(new_line)
            panel_text = new_console.highlighter(
                Text("\n".join(lines), style="bold"))
            live.update(Panel(panel_text))  # 클로져 지원되니까 이거 문제 x
    
        with Live(Panel("시작 중..."), console=new_console, refresh_per_second=4, transient=False) as live:
            if not module_name_to_update:
                module_name_to_update = module_name
    
            updater(f"현재 가상환경: {sys.executable}")
            updater(f"모듈 이름: {module_name}")
    
            current_version, message = get_current_version(module_name)
            updater(message)
            if not current_version:
                return 1  # 오류로 종료
    
            latest_version, message = get_latest_version_pypi(module_name)
            updater(message)
            if not latest_version:
                return 1
    
            need_update, message = compare_version(current_version, latest_version)
            updater(message)  # 이 아래 질문에서 꺠지기 때문에 별도의 패널로 분리
    
        lines = []
        if need_update:
            if update == "ask":
                update = ask_y_or_n("모듈을 업데이트하시겠습니까?")
    
            if update:  # true면
                with Live(Panel("시작 중..."), console=new_console, refresh_per_second=4, transient=False) as live:
                    update_module(module_name_to_update, updater)
            print()
        return 0
    ```
    
- 안전 포멧팅을 통해, 기존에 `yt-dlp`는 자동으로 포멧팅을 적용하지 않던 ‘경로’ 등에 비디오의 데이터를 직접 넣을 수 있게 되었기 때문에, 경로를 더 세세하게 설정할 수 있게 한다.
    
    ```python
    def __init__(
            self,
            playlist_url: str,
            video_bring_restrict: Callable[[EntryInPlaylist], bool] = None,
            playlist_title: str = "",
            video_save_dir_form: Literal["%(playlist)s",
                                         "%(playlist)s (%(channel)s)",
                                         "%(channel)s/%(playlist)s",
                                         ".",
                                         "%(playlist)s (%(channel)s)/%(upload_date>%Y.%m)s",
                                         "%(channel)s/%(playlist)s/%(upload_date>%Y.%m)s"
                                         ] | str | Literal["NONE"] = "NONE",  # 따로 설정할 경우
            colors: list[Style | str] | tuple[Style | str] = ("none", "dim"),
            split_chapter: bool = False,
            update_playlist_data: bool = True,
    ```
    

### 3.2. 적용할 개선사항

- 자막을 한글로도 가져오게 한다. 또한 데이터를 가져올 때 한글이나 영어 데이터를 가져올 수 있으면 이를 우선시하게 한다.
- 자막을 별도로 저장한 후 변환해서 삽입한다. 유튜브의 자막은 https://www.reddit.com/r/youtubedl/comments/1942y10/can_youtubedl_or_ytdlp_download_the_ytt_or_ass/#:~:text=Reddit%20www.reddit.com%20%20yt,YTSubConverter%20to%20convert%20srv3. 이 형식이다.
- 추상 클래스를 사용해서 딕셔너리 리스트의 집합 연산을 클래스로 만들고 이를 상속하는 구조로 개선한다.
- `Videos` 내의 기능들을 기능에 따라 별도의 믹스인 클래스로 분류하고, `update` 메소드를 구현한 상태로 다중상속하면 파이썬이 자동으로 상속된 클래스들을 순회하며 `update` 메소드를 실행한다. 이를 통해 구조를 알아보기 쉽게 개선할 수 있다.
- 프로그래스 바를 두 개로 분리하고(전체 영상 갯수 중 현재 진도, 개별 영상의 다운로드 진도) `group`으로 합쳐서 한번에 출력한다.
- json 파일을 읽어오는 함수를 `glob` 등을 사용해 경로가 복잡하게 쪼개져 있어도 파일들을 읽을 수 있게 한다.
- url을 분석하는 함수를 만들어서, 플레이리스트나 채널이 아니라 개별 비디오의 링크를 넣었을 경우 별도의 `Videos` 객체에 넣어서 다운로드 받을 수 있게 한다.
- 챕터를 유저가 직접 설정하고 변경할 수 있게 한다. 현재는 `re`를 사용한 댓글 파서로 챕터를 읽어오는데, 유저가 원하는 형태로 되지 않는 경우가 많다.
- 딕셔너리의 추가 키를 별도의 자료형으로 만들어서, 추가나 삭제가 간편하게 한다.
- `split_chapter, album, artist`를 비디오스에 기록하지 않고 추가 키에 통합하며, 이외의 정보 가져오기 함수에서 변경되는 메타데이터들(`chapter, meta_artist, meta_album, description, title, playlist_title, comments`)도 후처리기를 통해 영상에 메타데이터로 삽입한다.
- 챕터는 `yt-dlp`의 경로 설정을 이용해 경로를 일반 비디오와 다르게 하고, 원 제목으로 폴더를 만들고 그 안에 챕터 제목을 영상 제목으로 지정한다.
- 썸내일 저장 옵션을 끄면 저장되지 않게 한다. [썸내일 저장 제거하는 법](./docs/썸내일_저장_제거하는_법.md)
- 경로들을 `pathlib` 객체로 리펙토링한다.
- 썸내일을 챕터 분할 시에도 적용되게 수정한다. 필요시 `ffmpeg` 모듈을 사용한다.
- 필터링을 아래 함수와 같은 형태로 수정한다.
    
    ```python
    # 필터링 함수 이렇게
    def filter_dicts(data, condition, modify_original=False, return_unmatched=True):
        matched = [d for d in data if condition(d)]
        unmatched = [d for d in data if not condition(d)]
        
        if modify_original:
            data[:] = unmatched  # 원본 리스트를 수정
    
        return (matched, unmatched) if return_unmatched else matched
    
    ```
    
- 인터넷 연결 여부 확인 함수를 적용한다.
    
    ```python
    # 인터넷 연결 확인 및 지연 함수
    import socket
    import time
    
    def wait_for_internet(host="8.8.8.8", port=53, timeout=3, check_interval=1):
        """
        인터넷에 연결될 때까지 프로그램을 대기시킵니다.
    
        매개변수:
            host (str): 연결을 시도할 IP 주소 (기본값: 구글 DNS).
            port (int): 연결할 포트 번호.
            timeout (int): 각 시도에 대한 타임아웃 시간 (초).
            check_interval (int): 재시도 간격 (초).
        """
        print("인터넷 연결을 기다리는 중입니다...")
        while True:
            try:
                socket.setdefaulttimeout(timeout)
                socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
                print("인터넷 연결이 감지되었습니다.")
                break
            except socket.error:
                time.sleep(check_interval)
    
    ```
    
