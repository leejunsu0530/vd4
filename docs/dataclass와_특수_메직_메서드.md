# dataclass와 특수 메직 메서드

# dataclass 전용 메서드 및 특성 정리

파이썬의 `@dataclass`는 일반 클래스에서는 제공하지 않는 특수 메서드나 속성들을 제공합니다. 아래는 `dataclass`에서만 사용 가능한 주요 기능들과 예시입니다.

---

## 1. `__post_init__`

- 자동 생성된 `__init__` 이후에 호출됨
- 검증, 파생 필드 계산 등에 사용

```python
from dataclasses import dataclass

@dataclass
class Circle:
    radius: float
    area: float = 0.0

    def __post_init__(self):
        self.area = 3.14 * self.radius ** 2

```

---

## 2. `__dataclass_fields__`

- 클래스 수준에서 자동 생성되는 딕셔너리
- 모든 필드의 메타정보를 담고 있음

```python
from dataclasses import dataclass

@dataclass
class Person:
    name: str
    age: int

print(Person.__dataclass_fields__)
# {'name': Field(...), 'age': Field(...)}

```

---

## 3. `__dataclass_params__`

- `@dataclass`에 설정된 인자 정보를 저장함
- 예: frozen=True, init=False 등

```python
from dataclasses import dataclass

@dataclass(frozen=True)
class Point:
    x: int
    y: int

print(Point.__dataclass_params__)
# dataclass(frozen=True, ...)

```

---

## 4. 자동 생성되는 메서드들

- `__init__`, `__repr__`, `__eq__`, `__hash__`, `__lt__` 등은 dataclass 옵션에 따라 자동 생성됨
- 필요시 직접 오버라이드 가능

```python
from dataclasses import dataclass

@dataclass(order=True)
class Student:
    grade: int
    name: str

# Student 객체는 이제 <, >, <=, >= 비교가 가능함

```

---

## 5. 기타 (`pydantic.dataclasses` 한정)

- `__post_init_post_parse__()`는 Pydantic의 dataclass에서만 존재하는 메서드이며, 표준 dataclass에는 없음

---

## 요약 표

| 메서드 / 속성 | 설명 | 자동 생성 | 오버라이드 가능 |
| --- | --- | --- | --- |
| `__post_init__` | 후처리 메서드 | ❌ | ✅ |
| `__dataclass_fields__` | 필드 메타정보 딕셔너리 | ✅ | ❌ |
| `__dataclass_params__` | 데코레이터 설정 정보 | ✅ | ❌ |
| `__init__` | 생성자 | ✅(옵션) | ✅ |
| `__repr__`, `__eq__`, `__lt__` 등 | 비교, 출력, 해시용 메서드들 | ✅(옵션) | ✅ |

---

## 참고

- `@dataclass(order=True)`를 지정하면 `__lt__`, `__le__`, `__gt__`, `__ge__` 비교 연산자도 자동으로 생성됩니다.
- `frozen=True`를 지정하면 불변 객체처럼 동작합니다 (속성 할당 금지).