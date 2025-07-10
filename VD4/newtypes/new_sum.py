from typing import Any

def new_sum(*args: Any) -> Any:
    """
    '+' 연산자를 사용하여 전달된 모든 인자들의 합을 반환합니다.

    주의:
        - 리스트나 튜플이 전달될 경우, 내부의 개별 요소를 더하는 것이 아니라 전체 객체로서
          이어붙이게 됩니다.
          예를 들어:
              new_sum([1, 2, 3], [4, 5, 6]) 는 [1, 2, 3, 4, 5, 6]을 반환합니다.
              new_sum((1, 2, 3), (4, 5, 6)) 는 (1, 2, 3, 4, 5, 6)을 반환합니다.

    Args:
        *args: 더할 객체들.

    Return:
        제공된 모든 인자들을 '+' 연산자로 더한 결과.

    Exception:
        ValueError: 인자가 하나도 제공되지 않은 경우.
        TypeError: 서로 더할 수 없는 객체들이 포함된 경우.
    """
    if not args:
        raise ValueError("new_sum requires at least one argument")

    result = args[0]
    for arg in args[1:]:
        result = result + arg
    return result


if __name__ == '__main__':
    print(new_sum("a", "b", "c", "d"))
    print(new_sum((1, 2, 3), (4, 5, 6)))
