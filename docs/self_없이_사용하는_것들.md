# self 없이 사용하는 것들

# 클래스 내에서 self 없이 변수나 메서드를 선언하는 경우

Python 클래스 안에서 self 없이 변수를 선언하거나 메서드를 정의하는 경우는 특별한 의미를 가진다.

대표적으로 다음과 같은 3가지 경우가 있다:

---

## ✅ 1. 클래스 변수 (instance가 아닌 클래스 전체에 공유되는 변수)

```python
class MyClass:
    counter = 0  # 클래스 변수, 모든 인스턴스가 공유함

```

- self.counter가 아닌 MyClass.counter로 접근 가능
- 모든 인스턴스에서 같은 값을 공유함
- 변경 시 클래스 전체에 영향을 줌

### 예시:

```python
a = MyClass()
b = MyClass()
MyClass.counter = 5

print(a.counter)  # 5
print(b.counter)  # 5

```

---

## ✅ 2. @staticmethod: 인스턴스나 클래스와 무관한 메서드

```python
class MyClass:
    @staticmethod
    def say_hello():
        print("Hello!")

```

- self나 cls를 받지 않음
- 클래스와 논리적으로 관련 있지만 상태를 참조할 필요 없는 함수
- 인스턴스를 만들지 않고도 호출 가능: MyClass.say_hello()

### 예시:

```python
MyClass.say_hello()  # Hello!

```

---

## ✅ 3. @classmethod: 클래스 자체를 첫 인자로 받는 메서드

```python
class MyClass:
    value = 10

    @classmethod
    def show_value(cls):
        print(cls.value)

```

- 첫 번째 인자 cls는 클래스 자체
- 인스턴스 없이도 호출 가능하며, 클래스 속성에 접근할 때 유용

### 예시:

```python
MyClass.show_value()  # 10

```

---

## 🔍 혼동 주의: 메서드에서 self를 생략하면?

```python
class MyClass:
    def greet():
        print("Hi")

```

- 이렇게 쓰면 일반 인스턴스 메서드로 호출할 수 없음
- TypeError: greet() takes 0 positional arguments but 1 was given
- 이유: obj.greet() 호출 시 Python은 self를 자동으로 넘기기 때문

---

## ✅ 정리 요약

| 선언 방식 | 설명 | 첫 인자 |
| --- | --- | --- |
| def method(self) | 인스턴스 메서드 | self |
| @classmethod | 클래스 자체를 받는 메서드 | cls |
| @staticmethod | 클래스/인스턴스와 무관한 함수 | 없음 |
| 클래스 내부 변수 | 모든 인스턴스가 공유하는 클래스 변수 | 없음 |