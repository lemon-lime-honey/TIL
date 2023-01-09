# Data Type
## Number
### Numeric Type
#### int
- 파이썬에서 모든 정수의 타입은 int이다.
- 매우 큰 수를 나타낼 때 오버플로우가 발생하지 않는다.

#### float
- 파이썬에서 정수가 아닌 모든 실수는 float 타입이다.
- 부동소수점(floating point): 컴퓨터가 실수를 표현하는 방법
- *Floating point rounding error*: 실수 연산 과정에서 발생 가능
    - 두 실수를 비교할 때 주의해야 한다.
        - 두 수의 차의 절대값이 아주 작은 수보다 작은지를 확인하는 방법
        - math모듈을 활용하는 방법

#### complex
- 실수부와 허수부로 구성된 복소수
- 허수부를 j로 표현한다.

### Boolean Type
- True 또는 False
- 비교/논리 연산을 수행할 때 활용된다.
- `0, 0.0, (), [], {}, '', None`은 모두 False로 취급된다.
<br></br>

## Sequence
- 시퀀스형 주요 공통 연산자
    | 연산 | 내용 |
    | --- | --- |
    | s[i] | s의 i번째 항목 |
    | s[i:j] | s의 i에서 j까지의 슬라이스 |
    | s[i:h:k] | s의 i에서 j까지 스텝 k의 슬라이스 |
    | s + t | s와 t 연결 |
    | s * n 또는 n * s | s를 n회 반복 |
    | x in s | s에 x가 있으면 True 없으면 False |
    | x not in s | s에 x가 없으면 True 있으면 False |
    | len(s) | s의 길이 |
    | min(s) | s에서 가장 작은 원소 |
    | max(s) | s에서 가장 큰 원소 |

### String (Immutable, Iterable)
- 모든 문자는 str 타입
- 문자열은 작은 따옴표나 큰 따옴표를 활용하여 표기한다.
    - 문자열을 묶을 때에는 동일한 문장부호를 사용한다.
    - PEP8에서는 소스코드 내에서 하나의 문장부호를 선택하여 유지하도록 권장한다.
- Escape sequence

    | 예약문자 | 내용 |
    | --- | --- |
    | `\n` | 줄 바꿈 |
    | `\t` | 탭|
    | `\r` | 캐리지 리턴 |
    | `\0` | Null |
    | `\\` | \ |
    | `\'` | 작은 따옴표 |
    | `\"` | 큰 따옴표 |

#### String Formatting
- 문자열을 변수를 활용하여 만드는 법
- %-formatting
    ```python
    master = 'Qui-Gon Jinn'
    padawan = 'Obi-Wan Kenobi'
    age = 25

    print('When %s, the Padawan of %s, went to Tatooine, he was %d years old.' % (padawan, master, age))

    # When Obi-Wan Kenobi, the Padawan of Qui-Gon Jinn, went to Tatooine, he was 25 years old.
    ```
- str.format
    ```python
    master = 'Obi-Wan Kenobi'
    padawan = 'Anakin Skywalker'
    age = 19

    print('{} is the Padawan of {}.'.format(padawan, master))
    print('{} became Knight when he was {} years old.'.format(padawan, age))

    # Anakin Skywalker is Padawan of Obi-Wan Kenobi.
    # Anakin Skywalker became Knight when he was 19 years old.
    ```
- f-string
    ```python
    master = 'Anakin Skywalker'
    padawan = 'Ahsoka Tano'
    age = 14

    print(f'When {padawan} became {master}\'s Padawan, she was {age} years old.')

    # When Ahsoka Tano became Anakin Skywalker's Padawan, she was 14 years old.
    ```

### Tuple (Immutable, Iterable)
- 변경 불가능한 값들이 나열된 자료형
- 순서를 가지며, 서로 다른 타입의 요소를 가질 수 있다.
- 항상 소괄호 형태로 정의하며 원소는 반점으로 구분한다.
- 생성과 접근
    - 생성: `()` 또는 `tuple()`
    - 접근: 인덱스를 통해 접근할 수 있다.

### List (Mutable, Iterable)
- 변경 가능한 값들이 나열된 자료형
- 순서를 가지며, 서로 다른 타입의 요소를 가질 수 있다.
- 항상 대괄호 형태로 정의하며 원소는 반점으로 구분한다.
- 생성과 접근
    - 생성: `[]` 또는 `list()`
    - 순서가 있는 시퀀스로, 인덱스를 통해 접근할 수 있다.
- 값 추가: `.append()`
- 값 삭제: `.pop()`

### Range (Immutable, Iterable)
- 숫자의 시퀀스를 나타내기 위해 사용
- 기본형: `range(n)`
- 범위 지정: `range(n, m)`
- 범위 및 스텝 지정: `range(n, m, s)`
<br></br>

## Collection
### Set (Mutable, Iterable)
- 유일한 값들의 모음
- 순서와 중복된 값이 없다.
- 순서가 없으므로 반복의 결과가 정의한 순서와 다를 수 있다.
- 다른 컨테이너에서 중복된 값을 쉽게 제거할 수 있으나 이후 순서가 무시되기 때문에 순서가 중요한 경우에는 사용하지 않는다.
- 생성과 접근
    - 생성: `{}` 또는 `set()`
        - 빈 set을 만들기 위해서는 `set()`을 반드시 활용해야 한다.
    - 순서가 없어 별도의 값에 접근할 수 없다.
- 값 추가: `.add()`
- 값 삭제: `.remove()`
<br></br>

### Dictionary (Mutable, Iterable)
- key-value 쌍으로 이뤄진 [Mapping Type](https://docs.python.org/3/library/stdtypes.html#mapping-types-dict)
    - key: immutable 자료형만 가능(List, Dictionary 등은 불가)
    - value: 제한 없음
- key와 value는 콜론으로, 개별 요소는 반점으로 구분된다.
- 기본적으로 반복하면 key를 순회하며, key를 통해 value를 활용할 수 있다.
- `dict_name[key_name] = value`: key와 value의 값 추가 또는 변경
    - 이미 key가 존재하면 value의 값이 바뀐다.
    - key가 존재하지 않으면 새로운 쌍이 추가된다.
- `dict_name.pop()`: key 삭제
- `KeyError`: key가 존재하지 않는 경우 발생한다.
- `dict_name.keys()`: key의 모음을 반환한다.
- `dict_name.values()`: value의 모음을 반환한다.
- `dict_name.items()`: `(key, value)`의 튜플의 모음을 반환한다.
<br></br>

## None
- 파이썬 자료형 중 하나
- 파이썬에서는 값이 없음을 표현하기 위해 None 타입이 존재한다.
- 일반적으로 반환 값이 없는 함수에서 사용하기도 한다.
<br></br>

## Typecasting
- Implicit Typecasting
    - 사용자가 의도하지 않고 파이썬 내부적으로 자료형을 변환하는 경우
- Explicit Typecasting
    - 사용자가 특정 함수를 활용하여 의도적으로 자료형을 변환하는 경우
    - `str*`, `float` to `int`
    - `str*`, `int` to `float`
    - `int`, `float`, `list`, `tuple`, `dict` to `str`
    - *: 형식에 맞는 문자열만 가능
<br></br>

# Operator
- 산술 연산자

    | 연산자 | 내용 |
    | --- | --- |
    | + | 덧셈 |
    | - | 뺄셈 |
    | * | 곱셈 |
    | % | 나머지 |
    | / | 나눗셈 |
    | // | 몫 |
    | ** | 거듭제곱 |

- 복합 연산자: 연산과 할당이 함께 이루어진다.

    | 연산자 | 내용 |
    | --- | --- |
    | a += b | a = a + b |
    | a -= b | a = a - b |
    | a *= b | a = a * b |
    | a %= b | a = a % b |
    | a /= b | a = a / b |
    | a // b | a = a // b |
    | a ** b | a = a ** b |

- 비교 연산자: 값을 비교하여 True 또는 False를 반환한다.

    | 연산자 | 내용 |
    | --- | --- |
    | < | 미만 |
    | <= | 이하 |
    | > | 초과 |
    | >= | 이상 |
    | == | 같음 |
    | != | 같지 않음 |
    | is | 객체 아이덴티티 |
    | is not | 객체 아이덴티티가 아닌 경우 |

- 논리 연산자: 논리식을 판단하여 True 또는 False를 반환한다.

    | 연산자 | 내용 |
    | --- | --- |
    | A and B | A, B 둘 다 True: True |
    | A or B | A, B 둘 중 하나 True: True |
    | not | True는 False, False는 True로 |