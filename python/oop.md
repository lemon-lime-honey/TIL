# Object-Oriented Programming?
- 프로그램을 여러 개의 독립된 객체들과 그 객체들 간의 상호작용으로 파악하는 프로그래밍 방법
- 프로그램을 유연하고 변경하기 쉽도록 만들기 때문에 대규모 소프트웨어 개발에 많이 사용된다.
- 소프트웨어 개발과 보수를 쉽게 하고, 보다 직관적인 코드 분석을 가능하게 한다.
<br></br>

# Class and Instance
- class: 객체들의 분류
- instance: 객체 하나하나
- attribute: 특정 데이터 타입/클래스의 객체들이 가지게 될 상태 혹은 데이터
- method: 특정 데이터 타입/클래스의 객체에 공통적으로 적용 가능한 함수
- 객체 비교하기: `==`과 `is`
    - `==`
        - 동등한(equal)
        - 변수가 참조하는 객체의 내용이 같은 경우 `True` 반환
        - 두 변수가 실제로 동일한 대상을 가리키고 있다는 것을 보장할 수는 없다.
    - `is`
        - 동일한(identical)
        - 두 변수가 동일한 객체를 가리키는 경우 `True` 반환
<br></br>

## Instance
```python
class Sith:
    def __init__(self, name, hometown):
        self.name = name
        self.hometown = hometown
    
    def __del__(self):
        print(f'{self.name} is from {self.hometown}')
        print(f'{self.name} is deceased.')

sidious = Sith('Darth Sidious', 'Naboo')
maul = Sith('Darth Maul', 'Dathomir')
vader = Sith('Darth Vader', 'Tatooine')

```
- 인스턴스 변수
    - 인스턴스가 각자 가지고 있는 속성
    - 각 인스턴스의 고유한 변수
    - 생성자 메소드에서 `self.<name>`으로 정의한다.
    - 생성 후 `instance.<name>`으로 접근 또는 할당할 수 있다.
- 인스턴스 메소드
    - 인스턴스 변수를 사용하거나, 인스턴스 변수에 값을 설정하는 메소드
    - 클래스 내부에 정의되는 메소드의 기본
    - 호출 시, 첫 번째 인자로 인스턴스 자기자신(`self`)이 전달된다.
- `self`
    - 인스턴스 자기자신
    - 파이썬에서 인스턴스 메소드는 호출 시 첫 번째 인자로 인스턴스 자신이 전달되도록 설계되어있다.
        - 매개변수 이름으로 `self`를 첫 번째 인자로 정의한다.
        - 다른 단어를 사용해도 작동하지만 보통 `self`를 사용한다.
- 생성자 메소드 (constructor method)
    - 인스턴스 객체가 생성될 때 자동으로 호출되는 메소드
    - 인스턴스 변수들의 초기값을 설정한다.
        - 인스턴스 생성
        - `__init__` 메소드 자동 호출
- 소멸자 메소드 (destructor method)
    - 인스턴스 객체가 소멸되기 직전에 호출되는 메소드
- 매직 메소드 (magic method)
    - Double underscore(`__`)가 있는 메소드
    - 특수한 동작을 위해 만들어졌다.
    - 스페셜 메소드라고도 한다.
    - 특정 상황에 자동으로 호출된다.
- 매직 메소드의 예시
    - `__str__(self)`
        - 해당 객체의 출력 형태를 지정한다.
        - 프린트 함수를 호출할 때 자동으로 호출된다.
        - 어떤 인스턴스를 출력하면 `__str__`의 `return` 값이 출력된다.
    - `__len__(self)`
        - `len()` 함수를 호출할 때 자동으로 호출된다.
    - `__repr__(self)`
        - `repr()` 함수를 호출할 때 자동으로 호출된다.
    - `__lt__(self, other)`
        - `<`에 의해 호출된다.
    - `__le__(self, other)`
        - `<=`에 의해 호출된다.
    - `__eq__(self, other)`
        - `==`에 의해 호출된다.
    - `__gt__(self, other)`
        - `>`에 의해 호출된다.
    - `__ge__(self, other)`
        - `>=`에 의해 호출된다.
    - `__ne__(self, other)`
        - `!=`에 의해 호출된다.
