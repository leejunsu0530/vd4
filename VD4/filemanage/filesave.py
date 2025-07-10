import os
import json
import datetime


def write_str_to_file(file_name: str, to_write: str = "", parent_path: str = os.getcwd()):
    if not os.path.exists(parent_path):
        os.makedirs(parent_path, exist_ok=True)
    file_path = f"{parent_path}\\{file_name}"

    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(to_write)


def read_str_from_file(file_path: str) -> str | None:
    if not os.path.exists(file_path):
        return None
    else:  # 존재하면 읽어오기
        with open(file_path, 'r', encoding='utf-8') as file:
            text = file.read()
        return text


def write_dict_to_json(file_name: str, info_dict: dict, parent_path: str = os.getcwd()):
    """업데이트 여부는 호출할 함수에서 판별
    파일 이름에는 json 붙이든 말든 상관없음"""
    if not os.path.exists(parent_path):
        os.makedirs(parent_path, exist_ok=True)
    file_path = f"{parent_path}\\{file_name}" if file_name.split(".")[-1] == "json" \
        else f"{parent_path}\\{file_name}.json"

    with open(file_path, 'w', encoding='utf-8') as json_file:
        json.dump(info_dict, json_file, ensure_ascii=False, indent=4)


def read_dict_from_json(parent_path: str, file_name: str) -> dict:
    """딕셔너리 반환"""
    file_path = f"{parent_path}\\{file_name}" if file_name.split(".")[-1] == "json" \
        else f"{parent_path}\\{file_name}.json"
    if not os.path.exists(file_path):
        return {}
    else:  # 존재하면 읽어오기
        with open(file_path, 'r', encoding='utf-8') as json_file:
            info_dict: dict = json.load(json_file)
        return info_dict


# def dict_group_by(key: str, dict_list: list[dict]) -> dict[str, list[dict[str, str | int | float | None]]]:
#     """https://wikidocs.net/108940"""
#     dict_list = sorted(dict_list, key=itemgetter(key))
#     grouped_dict = groupby(dict_list, key=itemgetter(key))
#     result: dict = {}
#     for key_name, group_data in grouped_dict:
#         result[key_name] = list(group_data)
#     return result

def date_for_log() -> str:
    now = datetime.datetime.now()
    date_str = now.strftime("%Y%m%d_%H%M%S")
    return date_str
