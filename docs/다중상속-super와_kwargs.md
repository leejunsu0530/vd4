# 다중상속-super와 kwargs

# Python Multiple Inheritance 정리

---

## 1. 다중 상속에서 `__init__`이 자동으로 동작하는가?

### Q:

파이썬에서 클래스 여럿을 상속할 때, `__init__`을 오버라이딩하지 않으면 모든 부모의 `__init__`이 순서대로 동작해?

### A:

- ❌ 아니요. `__init__`을 오버라이딩하지 않으면, **MRO(Method Resolution Order)** 상 가장 앞에 있는 부모의 `__init__`만 자동으로 실행됩니다.
- 나머지 부모의 `__init__`은 **명시적으로 호출**하지 않으면 실행되지 않습니다.

```python
class A:
    def __init__(self):
        print("A init")

class B:
    def __init__(self):
        print("B init")

class C(A, B):
    pass

c = C()  # 출력: A init

```

---

## 2. 모든 `__init__`을 실행하려면?

### 방법:

- `super().__init__()`을 사용하고,
- 각 클래스에서 `args`, `*kwargs`로 인자를 받고,
- 필요한 인자만 추출 후 나머지를 다시 `super().__init__()`에 넘겨야 함.

```python
class A:
    def __init__(self, a_val, **kwargs):
        print(f"A init: {a_val}")
        super().__init__(**kwargs)

class B:
    def __init__(self, b_val, **kwargs):
        print(f"B init: {b_val}")
        super().__init__(**kwargs)

class C(A, B):
    def __init__(self, a_val, b_val, **kwargs):
        print("C init")
        super().__init__(a_val=a_val, b_val=b_val, **kwargs)

c = C(a_val=10, b_val=20)

```

**출력:**

```
C init
A init: 10
B init: 20

```

---

## 3. 다중 상속은 체인 형태인가?

### Q:

A(B, C)면 B(C)를 A가 상속하는 식으로 이해해야 하나?

### A:

- ❌ 아닙니다. `class A(B, C)`는 `A`가 `B`와 `C`를 **동시에 상속**하는 것입니다.
- `B(C)`처럼 체인처럼 상속하는 게 아니라, **각 클래스는 서로 sibling 관계**입니다.
- 실제 호출 순서는 **MRO**(Method Resolution Order)에 따라 결정됩니다.

```python
print(A.__mro__)
# (<class '__main__.A'>, <class '__main__.B'>, <class '__main__.C'>, <class 'object'>)

```

---

## 4. 기능 모듈을 다중 상속으로 조합 (인자 있는 메서드)

### 예시:

```python
class Logger:
    def log(self, message: str):
        print(f"[LOG]: {message}")

class Authenticator:
    def authenticate(self, user: str, password: str) -> bool:
        print(f"Authenticating {user}...")
        return password == "secret123"

class DataSaver:
    def save(self, data: dict, path: str):
        print(f"Saving data to {path}: {data}")

class App(Logger, Authenticator, DataSaver):
    def run(self, user, password, data, path):
        if self.authenticate(user, password):
            self.log("Authentication successful")
            self.save(data, path)
        else:
            self.log("Authentication failed")

app = App()
app.run("alice", "secret123", {"score": 95}, "data.json")

```

**출력:**

```
Authenticating alice...
[LOG]: Authentication successful
Saving data to data.json: {'score': 95}

```

---

## 5. 각각 다른 `__init__`을 가진 클래스 다중 상속 예시

```python
class Logger:
    def __init__(self, log_prefix, **kwargs):
        self.log_prefix = log_prefix
        print(f"Logger init: prefix = {log_prefix}")
        super().__init__(**kwargs)

class Authenticator:
    def __init__(self, auth_method, **kwargs):
        self.auth_method = auth_method
        print(f"Authenticator init: method = {auth_method}")
        super().__init__(**kwargs)

class DataSaver:
    def __init__(self, save_path, **kwargs):
        self.save_path = save_path
        print(f"DataSaver init: path = {save_path}")
        super().__init__(**kwargs)

class App(Logger, Authenticator, DataSaver):
    def __init__(self, log_prefix, auth_method, save_path):
        print("App init")
        super().__init__(log_prefix=log_prefix, auth_method=auth_method, save_path=save_path)

app = App(log_prefix="[APP]", auth_method="token", save_path="/tmp/data.json")

```

**출력:**

```
App init
Logger init: prefix = [APP]
Authenticator init: method = token
DataSaver init: path = /tmp/data.json

```

---

## ✅ 핵심 요약

- 다중 상속 시 `__init__`은 자동으로 모두 호출되지 않는다.
- `super().__init__(**kwargs)`를 사용하여 각 클래스의 초기화 함수를 협력적으로 실행해야 한다.
- 각 클래스는 자신이 필요한 인자만 사용하고, 나머지는 `*kwargs`로 넘겨야 한다.
- `class A(B, C)`는 A가 B와 C를 **동시에 상속**하는 것이며, B(C)의 의미는 아니다.