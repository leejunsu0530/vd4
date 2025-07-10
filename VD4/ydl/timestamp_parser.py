import re
from ..newtypes.format_str_tools import format_time, format_filename

# 시간 형식을 위한 패턴 (hh:mm:ss, h:mm:ss 또는 mm:ss)
TIME_PATTERN = r'(?:\d{1,2}[:.])?\d{1,2}[:.]\d{2}'

# 선행 문자(숫자, 대시, 글머리 기호 등)를 무시하기 위한 패턴
OPTIONAL_PREFIX = r'^(?:\s*(?:[-*•]|\d+[.)]))*\s*'

# 새로 추가된 패턴: 시간 범위를 나타내는데, 종료 시간과 제목은 선택적임.
pattern_range = re.compile(
    OPTIONAL_PREFIX + r'(?P<start>' + TIME_PATTERN + r')\s*[~-]\s*(?P<end>' + TIME_PATTERN + r')?\s*(?P<title>.+)?$'
)

# 기존 패턴: 제목 앞에 시간 (시간이 먼저 있는 경우)
pattern4 = re.compile(
    OPTIONAL_PREFIX + r'(?P<title>.+?)\s*[-:]\s*(?P<start>' + TIME_PATTERN + r')\s*[~-]\s*(?P<end>' + TIME_PATTERN + r')\s*$'
)
pattern2 = re.compile(
    OPTIONAL_PREFIX + r'(?P<start>' + TIME_PATTERN + r')\s*(?:[-:]\s*)?(?P<title>.+)$'
)
pattern3 = re.compile(
    OPTIONAL_PREFIX + r'(?P<title>.+?)\s*(?:[-:]\s*)?(?P<start>' + TIME_PATTERN + r')\s*$'
)
# 추가 패턴: 제목 뒤에 괄호로 감싼 시간
pattern5 = re.compile(
    OPTIONAL_PREFIX + r'(?P<title>.+?)\s*(?:\(\s*|\[\s*)(?P<start>' + TIME_PATTERN + r')\s*[)\]]\s*$'
)

# 추가 패턴: 괄호로 감싼 시간이 앞에 있는 경우
pattern6 = re.compile(
    OPTIONAL_PREFIX + r'(?:\(\s*|\[\s*)(?P<start>' + TIME_PATTERN + r')\s*[)\]]\s*(?P<title>.+)$'
)


def convert_time_str_to_second_int(time_str):
    """
    "hh:mm:ss" 또는 "mm:ss" 형식의 문자열을 초 단위 정수로 변환합니다.
    """
    parts = time_str.split(':')
    parts = [int(p) for p in parts]
    if len(parts) == 3:
        h, m, s = parts
    elif len(parts) == 2:
        h = 0
        m, s = parts
    else:
        return 0
    return h * 3600 + m * 60 + s


def parse_chapter_line(line):
    """
    한 줄에서 챕터 정보를 파싱합니다.
    반환값은 {'start': 시작시간, 'end': 종료시간 (없으면 None), 'title': 챕터 제목} 형태의 딕셔너리입니다.
    """
    for pattern in [pattern_range, pattern4, pattern2, pattern3, pattern5, pattern6]:
        match = pattern.match(line)
        if match:
            groups = match.groupdict()
            if groups.get('start'):
                groups['start'] = groups['start'].replace('.', ':')
            if groups.get('end'):
                groups['end'] = groups['end'].replace('.', ':')
            # 만약 그룹이 None이면 빈 문자열로 변환 (특히 title)
            if groups.get('title') is None:
                groups['title'] = ''
            return groups
    return None


def parse_chapters(text: str, video_duration: int | str | None = None, return_int: bool = True):
    """
    전체 텍스트(여러 줄)에서 각 줄의 챕터 정보를 파싱하여
    [{'start': 시작시간, 'end': 종료시간(없으면 None), 'title': 챕터 제목}, ...] 형태의 리스트를 반환합니다.
    """
    chapters = []
    lines = text.splitlines()
    for line in lines:
        if not line.strip():
            continue
        result = parse_chapter_line(line)
        if result:
            chapters.append({
                'start': result.get('start'),
                'end': result.get('end') if result.get('end') else None,
                'title': format_filename(result.get('title').strip())
            })
    if isinstance(video_duration, str):
        video_duration = convert_time_str_to_second_int(video_duration)
    adjust_chapter_boundaries(chapters, video_duration)
    check_start_and_end(chapters)
    if return_int:
        for chapter in chapters:
            chapter['start_time'] = convert_time_str_to_second_int(chapter.pop('start'))
            if chapter['end']:
                chapter['end_time'] = convert_time_str_to_second_int(chapter.pop('end'))
    return chapters


def adjust_chapter_boundaries(chapters: list[dict], video_duration: int | None = None):
    """
    video_duration은 문자열 형식이 아닌 시간
    챕터 리스트를 시작 시간(초 기준)으로 정렬한 후,
    종료 시간이 없는 챕터는 다음 챕터의 시작 시간을 종료 시간으로 할당합니다.
    마지막 챕터의 종료 시간이 없으면, video_duration(문자열 형식)가 제공된 경우 그 값을 할당합니다.
    """

    for chapter in chapters:
        chapter['start_sec'] = convert_time_str_to_second_int(chapter['start'])

    chapters.sort(key=lambda x: x['start_sec'])
    for i in range(len(chapters) - 1):
        if not chapters[i]['end']:
            chapters[i]['end'] = chapters[i + 1]['start']
    if chapters and video_duration and not chapters[-1]['end']:
        chapters[-1]['end'] = format_time(video_duration, return_int=True)
    for chapter in chapters:
        chapter.pop('start_sec')
    return chapters


def check_start_and_end(chapter_list: list[dict[str, str | int]]):
    for idx, chapter in enumerate(chapter_list):
        if chapter.get("end") and chapter.get("start") > chapter.get("end"):
            del chapter_list[idx]
