from urllib.parse import urlparse, parse_qs


# 유튜브를 위한 모듈
def _bring_playlist_id(url: str) -> str | None:
    parsed_url = urlparse(url)
    query_params = parse_qs(parsed_url.query)  # ?뒤의 부분 추출, 파싱
    # list=PL1234567890ABCDE&other=param을 {'list': ['PL1234567890ABCDE'], 'other': ['param']}으로
    return query_params.get("list", [None])[0]  # 리스트의 첫 요소 또는 none


def _bring_channel_id(url: str) -> str | None:
    """
    1) https://www.youtube.com/channel/UCmgRYMK5d65PbjN8qkjAUBA
    2) https://www.youtube.com/@snceckie
    3) https://www.youtube.com/@snceckie/videos

    이 세 형태 중 1, 2는 가능하지만 3은 불가능
    """
    channel_id = None  # 초기화
    if 'channel' in url:  # 1
        parsed = urlparse(url)
        parts = parsed.path.split("/")
        if len(parts) >= 3 and parts[1] == 'channel':
            channel_id = parts[2]
    elif '@' in url:  # 2,3
        channel_id = f"@{url.split('@')[-1]}"
        if "/" in channel_id:  # 3: @snceckie/videos같이 뒤에 더 있으면 그냥 id로 들어가서 못 찾음
            channel_id = None

    return channel_id


def find_id(url: str) -> str | None:
    if 'list' in url:
        return _bring_playlist_id(url)
    elif '@' in url:
        return _bring_channel_id(url)
    else:
        return None


def return_korea_url():
    pass
