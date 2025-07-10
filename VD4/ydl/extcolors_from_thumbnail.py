import extcolors
import os
import requests


# 포스트 프로세서로 만들고 싶은데,
# 경로를 채널다운 함수에 제공하면 가능은 한데 경로가 채널 다운 이후에 정해져서 불가.
# 그리고 애초에 플리가 아니라 채널 썸내일이라 다름
def thumbnail_selector(info_dict: dict) -> tuple[dict | None, dict | None]:
    """썸내일과 채널아트 반환"""
    thumbnails = info_dict.get('thumbnails')
    if not thumbnails:  # 아무 썸내일도 없으면
        return None, None

    # 썸내일 찾기
    channel_profiles: list[dict] = [t for t in thumbnails if t.get("height") == t.get("width")
                                    and t.get('id') != "avatar_uncropped" and t.get('id') != "banner_uncropped"]
    if channel_profiles:  # 잘린 썸내일이 있으면
        channel_profile = channel_profiles[0]
    else:  # 없으면 언크롭 가져오기
        channel_profile_uncropped = [t for t in channel_profiles if t.get('id') == "avatar_uncropped"]  # 안잘린 거 찾기
        if channel_profile_uncropped:  # 안잘린게 있으면
            channel_profile = channel_profile_uncropped[0]
        else:
            channel_profile = None

    # 채널아트 찾기
    channel_arts: list[dict] = [t for t in thumbnails if t.get("height") != t.get("width")]
    if channel_arts:  # 잘린 썸내일이 있으면
        channel_art = channel_arts[0]
    else:  # 없으면 언크롭
        channel_arts_uncroped = [t for t in channel_arts if t.get('id') == "banner_uncropped"]  # 안잘린 거 찾기
        if channel_arts_uncroped:  # 안잘린게 있으면
            channel_art = channel_arts_uncroped[0]
        else:
            channel_art = None

    return channel_profile, channel_art


def download_thumbnail(thumbnail_dict: dict, channel_name: str, folder_path: str) -> tuple[int, str, str]:
    """

    성공 여부 코드는 0일때 성공, 1일때 실패
    Return:
        (성공 여부 코드, 메시지, 저장된 경로)
        """
    # preference가 가장 낮은게 사용됨. 아바타는 채널 썸내일, 배너는 채널 아트. uncropped는 원본임.

    url = thumbnail_dict.get('url')
    file_name = f"{channel_name}.jpg"
    file_path = f"{folder_path}\\{file_name}"
    os.makedirs(folder_path, exist_ok=True)

    if os.path.exists(file_path):
        return 0, f"이미지 {file_name}가 이미 저장되어 있음. ", file_path
    response = requests.get(url)
    if response.status_code == 200:  # 웹 요청이 성공적으로 처리됨. 서버가 요청한 리소스를 반환함.
        with open(file_path, 'wb') as f:  # 작성, 바이너리로 엶
            f.write(response.content)
        return 0, f"이미지 {file_name}가 {folder_path}에 성공적으로 저장됨. ", file_path
    else:
        return 1, f"이미지 다운로드 실패. error code: {response.status_code}. ", file_path


def bring_major_colors(image_path: str) -> list[str]:
    colors, pixel_count = extcolors.extract_from_path(image_path)
    color_string = [f"rgb({c[0]},{c[1]},{c[2]})" for c, pixel_num in colors]
    return color_string


if __name__ == '__main__':
    from rich import print

    path = ("C:\\Users\\user\\Desktop\\PROGRAMMING\\VScodeWorkspace\\PythonWorkspace\\test\\pl_thumb\\ㅗ디ㅣㅐ.png"
            "top.jpg")
    cl = bring_major_colors(path)
    [print(f"[{c}]{c}") for c in cl]
