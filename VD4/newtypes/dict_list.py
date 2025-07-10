import json


def bring_key_list(lst: list[dict], key: str) -> list:
    return [dict_.get(key) for dict_ in lst]


def dict_set_union(list1: list[dict], list2: list[dict]) -> list[dict]:
    set1 = {json.dumps(item, sort_keys=True) for item in list1}
    set2 = {json.dumps(item, sort_keys=True) for item in list2}

    # 집합 연산 수행
    sum_json = set1 | set2

    # JSON 문자열을 다시 딕셔너리로 변환
    sum_ = [json.loads(item) for item in sum_json]

    return sum_


def dict_set_diff(list1: list[dict], list2: list[dict]) -> list[dict]:
    set1 = {json.dumps(item, sort_keys=True) for item in list1}
    set2 = {json.dumps(item, sort_keys=True) for item in list2}

    # 집합 연산 수행
    diff_json = set1 - set2

    # JSON 문자열을 다시 딕셔너리로 변환
    difference = [json.loads(item) for item in diff_json]

    return difference


def dict_set_inter(list1: list[dict], list2: list[dict]) -> list[dict]:
    set1 = {json.dumps(item, sort_keys=True) for item in list1}
    set2 = {json.dumps(item, sort_keys=True) for item in list2}

    # 집합 연산 수행
    inter_json = set1 & set2

    # JSON 문자열을 다시 딕셔너리로 변환
    intersection = [json.loads(item) for item in inter_json]

    return intersection


if __name__ == '__main__':
    list_a = [{'id': 1, 'name': 'Alice'}, {'id': 2, 'name': 'Bob'}]
    list_b = [{'id': 2, 'name': 'Bob'}, {'id': 3, 'name': 'Charlie'}]

    print(dict_set_union(list_a, list_b))
    print(dict_set_diff(list_a, list_b))
    print(dict_set_inter(list_a, list_b))
