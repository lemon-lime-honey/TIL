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
<br></br>

## class
```python
class Mandalorian:
    planet = 'Mandalore'
    moon = 'Concordia'
    capital = 'Keldabe'

    def __init__(self, name, always_helmet):
        self.name = name
        self.always_helmet = always_helmet
    
    @classmethod
    def capitalTransfer(cls, city):
        cls.capital = city
    
    @staticmethod
    def theWay():
        print('This is the Way')
    
din = Mandalorian('Din Djarin', True)
bokatan = Mandalorian('Bo-Katan Kryze', False)

din.theWay()
Mandalorian.capitalTransfer('Sundari')
print(Mandalorian.capital)
```
- class attribute
    - 한 클래스의 모든 인스턴스가 같은 값을 가지고 있는 속성
    - 클래스 선언 내부에서 정의한다.
    - `<classname>.<name>`으로 접근 및 할당한다.
- class method
    - 클래스가 사용할 메소드
    - `@classmethod` 데코레이터를 사용하여 정의한다.
        - 데코레이터: 함수를 어떤 함수로 꾸며서 새로운 기능을 부여한다.
    - 호출 시, 첫 번째 인자로 클래스(`cls`)가 전달된다.
- static method
    - 인스턴스나 클래스를 사용하지 않는 메소드
    - `@staticmethod` 데코레이터를 사용하여 정의한다.
    - 호출 시 어떠한 인자도 전달되지 않는다. 
    - 클래스 및 인스턴스 정보에 접근 또는 수정이 불가하다.
- 인스턴스와 클래스 간의 이름 공간
    - 클래스를 정의하면 클래스와 해당하는 이름 공간이 생성된다.
    - 인스턴스를 만들면 인스턴스 객체가 생성되고 이름 공간이 생성된다.
    - 인스턴스에서 특정 속성에 접근하면 인스턴스-클래스 순으로 탐색한다.
<br></br>

# Inheritance
```python
class Jedi:
    name = 'name'
    rank = 'rank'

class Apprentice:
    rank = 'Padawan'
    def __init__(self, name):
        self.name = name

class Knight(Jedi):
    rank = 'Knight'
    def __init__(self, name):
        self.name = name
    
    def greeting(self):
        print(f"I'm Jedi {Knight.rank} {self.name}.")

class Padawan(Jedi, Apprentice):
    def greeting(self):
        print(f"I'm Jedi {Apprentice.rank} {self.name}!")

kenobi = Knight('Obi-Wan Kenobi')
skywalker = Padawan('Anakin Skywalker')

kenobi.greeting()
skywalker.greeting()
```
## class inheritance
- 두 클래스 사이 부모-자식 관계를 정립하는 것
    - 예) 모든 파이썬 클래스는 object를 상속받는다.
- 부모에 정의된 속성이나 메소드를 활용하거나 오버라이딩(재정의)를 하여 활용한다.
    - 코드의 재사용성을 높이고 클래스 간의 계층적 관계를 활용한다.
- 관련 함수와 메소드
    - `isinstance(object, classinfo)`
        object가 classinfo의 instance이거나 subclass인 경우 `True`를 반환한다.
    - `issubclass(class, classinfo)`
        - class가 classinfo의 subclass이면 `True`를 반환한다.
        - classinfo는 클래스 객체의 tuple일 수 있으며, classinfo의 모든 항목을 검사한다.
    - `super()`
        - 자식 클래스에서 부모 클래스를 사용하고 싶은 경우 활용한다.
- method overriding
    - 상속 받은 메소드를 재정의한다.
        - 상속받은 클래스에서 같은 이름의 메소드로 덮어쓴다.
        - 부모 클래스의 메소드를 실행시키고 싶은 경우 `super`를 활용한다.
- 다중 상속
    - 파이썬은 두 개 이상의 클래스를 상속 받을 수 있다.
    - 상속 받은 모든 클래스의 요소를 활용할 수 있다.
    - 중복된 속성이나 메소드가 있는 경우 상속 순서에 의해 결정된다.