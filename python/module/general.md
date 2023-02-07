# Module
- 특정 기능을 하는 코드를 파이썬 파일(`.py`) 단위로 작성한 것
<br></br>

# Package
- 특정 기능에 관련된 여러 모듈의 집합
- 패키지 안에 또 다른 서브 패키지를 포함하기도 한다.
<br></br>

# Python Standard Library
- 파이썬에 기본적으로 설치된 모듈과 내장 함수이다.
- 여러가지가 있지만, 우선 `random`, `datetime`, `os` 모듈을 살펴본다.
- (230106 추가) `pprint`
## random
- 숫자/수학 모듈 중 의사 난수(pseudo random number)를 생성하는 모듈이다.
    - 임의의 숫자 생성, 무작위 요소의 선택, 무작위 비복원 추출(샘플링)을 위한 함수를 제공한다.
- `random.randint(a, b)`: a 이상 b 이하의 임의의 정수를 반환한다.
- `random.choice(seq)`
    - 시퀀스에서 임의의 요소를 반환한다.
    - 시퀀스가 비어있으면 `IndexError`를 발생시킨다.
- `random.shuffle(seq)`: 시퀀스를 섞은 후 저장한다.
- `random.sample(population, k)`: 길이 k로 무작위 비복원 추출한 리스트를 반환한다.
<br></br>

## datetime
- 날짜와 시간을 조작하는 객체를 제공한다.
- 사용 가능한 데이터 타입
    - `datetime.date`, `datetime.time`, `datetime.datetime`, `datetime.timedelta` 등
- `datetime.date(year, month, day)`
    - 모든 인자가 필수이다. 각 인자는 특정 범위 내에 있는 정수여야 한다.
        - `year`: 1이상 9999 이하
        - `month`: 1 이상 12 이하
        - `day`: 1과 주어진 `year`의 주어진 `month`의 날 수 차이
    - 범위를 벗어나는 인자가 주어지면 `ValueError`가 발생한다.
- `datetime.date.today()`: 현재 지역의 날짜를 반환한다.
- `datetime.datetime.today()`: 현재 지역의 `datetime`을 반환한다.
- `classmethod datetime.now(tz = None)`
    - `tz`가 `None`이거나 지정되지 않으면 `today()`와 유사하다.
    ```python
    import datetime
    
    kst = datetime.timezone(datetime.timedelta(hours = 9))
    utc_time = datetime.datetime.now(datetime.timezone.utc)
    kst_time = datetime.datetime.now(tz = kst)
    ```
<br></br>

## os
- OS를 조작하기 위한 인터페이스를 제공한다.
- `os.listdir(path = '.')`
    - path에 의해 주어진 디렉토리에 있는 항목들의 이름을 담고 있는 리스트를 반환한다.
    - 리스트는 임의의 순서로 나열되며, 특수 항목은 포함하지 않는다.
- `os.mkdir(path)`: path라는 디렉토리를 만든다.
- `os.chdir(path)`: path를 변경한다.
<br></br>

## pprint
- 임의의 파이썬 데이터 구조를 인터프리터의 입력으로 사용할 수 있는 형태로 *예쁘게 출력*할 수 있는 기능을 제공한다.
- 가능하면 객체를 한 줄에 유지하고, 허용된 너비에 맞지 않으면 여러 줄로 나눈다.
- 너비 제한을 조정하려면 `PrettyPrinter` 객체를 만든다.
- 딕셔너리는 우선 키로 정렬된다.
- `pprint.pprint(object, stream = None, indent = 1, width = 80, depth = None, *, compact = False, sort_dict = True, underscore_numbers = False)`
    - 사용할 수 있는 인자에 관한 설명은 [공식문서](https://docs.python.org/3/library/pprint.html?highlight=pprint#pprint.PrettyPrinter)에 나와있다.
    - 별 다른 설정을 할 필요가 없다면 `pprint(object)`로 사용할 수 있다.
    - 딕셔너리를 출력할 때 정렬되는게 싫다면 `sort_dict = False`를 추가하면 된다.
<br></br>

# Python Package
## PIP (Preferred Installer Program / PIP Installs Packages)
- PyPI(Python Package Index)에 저장된 외부 패키지들을 설치하도록 도와주는 패키지 관리 시스템
- 패키지 설치
    - 최신 버전 / 특정 버전 / 최소 버전을 명시하여 설치할 수 있다.
    - 이미 설치되어 있는 경우 이미 설치되어 있음을 알리고 아무것도 하지 않는다.
    ```bash
    # 최신 버전
    $ pip install SomePackage
    # 특정 버전
    $ pip install SomePackage == 1.0.5
    # 최소 버전
    $ pip install 'SomePackage >= 1.0.4'
    ```
- `$ pip uninstall SomePackage`: 패키지 삭제
    - pip은 패키지를 업그레이드하는 경우 과거 버전을 자동으로 지워준다.
- `$ pip list`: 설치된 패키지의 목록을 출력한다.
- `$ pip show SomePackage`: 특정 패키지의 정보를 출력한다.
- `$ pip freeze`
    - `pip list`와 비슷한 목록을 만들지만 `pip install`에서 활용하는 방식으로 출력한다.
    - 해당하는 목록을 `requirements.txt`로 만들어 관리한다.
- 패키지 관리하기
    ```bash
    $ pip freeze > requirements.txt
    $ pip install -r requirements.txt
    ```
    - 위와 같은 방법으로 패키지 목록을 관리하고 설치할 수 있다.
<br></br>

## 모듈과 패키지 활용
```python
# 모듈 가져오기
import module
# 모듈에서 변수, 함수, 클래스 가져오기
from module import var, function, Class
# import module과 같다
from module import *

# 패키지에서 모듈 가져오기
from package import module
# 특정 패키지의 특정 모듈에서 변수, 함수, 클래스 가져오기
from package.module import var, function, Class
```