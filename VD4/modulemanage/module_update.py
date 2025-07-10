import requests
from packaging import version
import importlib.metadata

from .execute_cmd import execute_cmd
from ..richtext.ask_prompt import ask_y_or_n
import sys
from typing import Union, Literal


def get_current_version(package_name: str, print_: bool = True) -> str | None:
    try:
        v = importlib.metadata.version(package_name)
        if print_:
            print(f"설치된 현재 버전: {v}")
        return v
    except importlib.metadata.PackageNotFoundError:
        if print_:
            print("패키지를 찾을 수 없습니다.")
        return None


def get_latest_version_pypi(package_name: str, print_: bool = True) -> str | None:
    url = f"https://pypi.org/pypi/{package_name}/json"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data["info"]["version"]
    else:
        if print_:
            print("PyPI에서 데이터를 가져오는 중 오류 발생")
        return None


def compare_version(current_version: str, latest_version: str, print_: bool = True) -> bool:
    if version.parse(current_version) < version.parse(latest_version):
        if print_:
            print("업데이트가 필요합니다.")
        return True
    else:
        if print_:
            print("이미 최신 버전을 사용 중입니다.")
        return False


def check_and_compare_versions(module_name: str) -> tuple[str, str, bool] | None:
    """현 모듈, 최신 모듈, 업데이트 필요 여부"""
    current = get_current_version(module_name, False)
    if not current:
        return None
    latest = get_latest_version_pypi(module_name, False)
    if not latest:
        return None
    need_update = compare_version(current, latest, False)
    return current, latest, need_update


def update_module(module_name: str, print_: bool = True) -> str:
    # subprocess.check_call([sys.executable, '-m', 'pip', 'install', '--upgrade', 'module_name'])
    result = execute_cmd([sys.executable, '-m', 'pip', 'install', '--upgrade', module_name], shell=False)
    if print_:
        print(result)
    return result


def check_and_update_module(module_name: str, update: Union[bool, Literal["ask"]] = True, print_: bool = True) -> int:
    """에러코드는 0이 성공, 1이 실패,
    update가 'ask'면 프롬프트로 물어봄"""
    if print_:
        print(f"모듈 이름: {module_name}")
    current = get_current_version(module_name, print_)
    if not current:
        return 1
    latest = get_latest_version_pypi(module_name, print_)
    if not latest:
        return 1
    need_update = compare_version(current, latest, print_)
    if need_update:
        if update == "ask":
            update = ask_y_or_n("모듈을 업데이트하시겠습니까?")
        if update:
            result = update_module(module_name, print_)
            if result.startswith("Error:"):
                return 1
    print()
    return 0


if __name__ == '__main__':
    check_and_update_module('yt-dlp', "ask")
