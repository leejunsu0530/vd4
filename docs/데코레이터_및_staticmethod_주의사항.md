# 데코레이터 및 staticmethod 주의사항

# 데코레이터 타입힌트 개선과 단순화 정리

## 1. 문제: `Callable[[Any], str]`의 제한

- 이 타입힌트는 "인자 하나(any 타입)만 받고 str을 반환하는 함수"로 해석됨
- `def f(a, b=3, *, c=None):` 같은 함수는 타입 불일치로 mypy에서 에러 발생
- 특히 `**kwargs`를 쓰는 함수는 감쌀 수 없음

---

## 2. 해결책: `ParamSpec`과 `TypeVar` 사용

```python
from typing import Callable, TypeVar, ParamSpec
from functools import wraps

P = ParamSpec("P")
R = TypeVar("R", bound=str)

def _try_and_return_str(func: Callable[P, R]) -> Callable[P, R]:
    @wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        try:
            return func(*args, **kwargs)
        except (TypeError, ValueError):
            return str(args)  # type: ignore
    return wrapper
```

### 구성 요소 설명

| 요소 | 의미 |
| --- | --- |
| `ParamSpec("P")` | 인자 리스트 전체를 타입으로 추적 (args, kwargs 포함) |
| `TypeVar("R")` | 반환 타입을 추적 |
| `Callable[P, R]` | "P 형태의 인자를 받고 R을 반환하는 함수"라는 의미 |

---

## 3. 단순화 버전 (타입 검사 및 자동완성 포기)

```python
def _try_and_return_str(func: Callable) -> Callable:
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (TypeError, ValueError):
            return str(args)
    return wrapper
```

- 장점: 코드가 간단하고 빠르게 쓸 수 있음
- 단점:
    - IDE에서 자동완성이 작동하지 않음
    - `mypy` 등의 정적 타입 검사기에서 오류를 찾지 못함

---

## 4. `__class__` 사용 오류

### 오류 메시지:

```python
Name "__class__" is not defined
```

### 원인:

- `@staticmethod` 안에서는 `__class__`가 자동으로 정의되지 않음
- `__class__`는 인스턴스 메서드나 클래스 메서드에서만 사용 가능

### 해결책:

- 클래스 이름을 명시적으로 사용

```python
# 잘못된 예
__class__._format_byte(...)

# 올바른 예
FormatStr._format_byte(...)
```

---

## 5. protected-access 경고

### 경고 예시:

```python
Access to a protected member _format_byte of a client class (pylint W0212)
```

### 의미:

- `_`로 시작하는 메서드는 관례상 "외부에서 직접 호출하지 말라"는 의미
- 같은 클래스 안에서 사용하는 것은 안전함

### 대응 방법:

- `_`를 제거하거나
- 경고 무시

```python
# 파일 상단에 추가
# pylint: disable=protected-access
```

---

## ✅ 정리

| 상황 | 추천 방법 |
| --- | --- |
| 자동완성 및 타입 검사 필요 | `ParamSpec`, `TypeVar`, `@wraps` 사용 |
| 간단히 쓰고 싶을 때 | 그냥 `Callable`로 받고 wrapper 정의만 사용 |
| staticmethod 내부에서 self 없이 클래스 접근 | 클래스명 직접 명시 (`ClassName.meth |