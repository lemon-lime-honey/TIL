# What is function?
## Function
- 특정한 기능을 하는 코드의 묶음
- 특정 명령을 수행하는 코드를 매번 다시 작성하지 않고, 필요 시에만 호출하여 간편하게 사용한다.
<br></br>

## Custom Function
```python
def function_name(argument):
    # code block
    return returning_value
```
- 사용자가 직접 함수를 작성해서 사용할 수도 있다.
<br></br>

# Built-in Function
## Frequently used
- `print()`
    - `sep`을 사용하여 구분자를 변경할 수 있다.(기본값: 공백 한 칸)
    - `end`를 사용하여 입력된 객체를 출력 후 출력할 것을 지정할 수 있다. (기본값: `\n`)
        ```python
        print('Hello', 'there', sep = ', ', end = '!\n')
        # Hello, there!
        ```
- `len(s)`
    - 객체의 길이를 반환한다. 인자는 시퀀스 또는 컬렉션이다.
- `sum(iterable, start = 0)`
    - iterable의 항목의 합을 반환한다. 이때 start의 값은 offset의 역할을 한다.
    - iterable의 항목은 대개 숫자이며, start 값은 문자열이 될 수 없다.
- `max(iterable)`
    - iterable에서 가장 큰 항목이나 두 개 이상의 인자 중 가장 큰 것을 반환한다.
    - 여러 항목이 최대일 때, 처음으로 만난 항목을 반환한다.
- `min(iterable)`
    - iteralbe에서 가장 작은 항목이나 두 개 이상의 인자 중 가장 작은 것을 반환한다.
    - 여러 항목이 최소일 때, 처음으로 만난 항목을 반환한다.
- `map(function, iterable)`
    - iterable의 모든 요소에 function을 적용하고, 그 결과를 map object로 변환한다.
        ```python
        age = '25 19 14'
        jedi = list(map(int, age.split()))
        print(jedi)
        # 25, 19, 14
        # str.split(sep = None, maxsplit = -1)
        ```
<br></br>

## Mathematics
- `abs(x)`
    - 숫자의 절댓값을 반환한다.
    - 인자는 정수, 실수 또는 `__abs__()`를 구현하는 객체이다.
    - 인자가 복소수이면 그 크기를 반환한다.
- `divmod(a, b)`
    - 두 수를 받아 몫과 나머지를 반환한다.
- `pow(base, exp, mod = None)`
    - base의 exp 거듭제곱을 반환한다.
    - mod가 있을 경우 base의 exp 거듭제곱을 mod로 나눴을 때의 나머지를 반환한다.
- `round(number, ndigits = None)`
    - number를 소수점 아래 ndigits번째 자리로 반올림한 값을 반환한다.
    - ndigits이 생략되거나 None이면 입력에 가장 가까운 정수를 반환한다.
<br></br>

## Logic
- `all(iterable)`
    - iterable의 모든 요소가 참이면(또는 iterable이 비어있으면) True를 반환한다.
- `any(iterable)`
    - iterable의 요소 중 하나라도 참이면 True를 반환한다.
    - iterable이 비어 있으면 False를 반환한다.
<br></br>

## etc
- `bin(x)`
    - 정수를 `0b` 접두사가 붙은 이진 문자열로 반환한다.
- `hex(x)`
    - 정수를 `0x` 접두사가 붙은 16진수 문자열로 반환한다.
- `oct(x)`
    - 정수를 `0o` 접두사가 붙은 8진수 문자열로 반환한다.
- `ord(c)`
    - 문자 c에 대응되는 유니코드 코드 포인트를 반환한다.
- `chr(i)`
    - 유니코드 코드 포인트에 대응되는 문자를 반환한다.
<br></br>

# Method
- class body 안에서 정의되는 함수
## string
| 문법 | 설명 |
| --- | --- |
| `s.find(x)` | x의 첫 번째 위치 반환. 없으면 -1 반환 |
| `s.index(x)` | x의 첫 번째 위치 반환. 없으면 오류 발생 |
| `s.isalpha()` | 문자(유니코드 기준)면 True 반환 |
| `s.isupper()` | 대문자면 True 반환 |
| `s.islower()` | 소문자면 True 반환 |
| `s.istitle()` | 타이틀 형식이면 True 반환 |
| `s.isdecimal()` | 문자열 내의 모든 문자가 십진수 문자이고, 적어도 하나의 문자가 존재하는 경우 True 반환. 십진수 문자는 십진법으로 숫자를 구성할 때 사용될 수 있는 문자 |
| `s.isdigit()` | 문자열 내의 모든 문자가 digit이고, 적어도 하나의 문자가 존재하는 경우 True 반환. digit은 십진수 문자 뿐만 아니라 특수처리가 필요한 숫자 등이 포함함 |
| `s.isnumeric()` | 문자열 내의 모든 문자가 숫자이고, 적어도 하나의 문자가 존재하는 경우 True 반환. 숫자는 digit와 유니코드 숫자 값 속성을 갖는 모든 문자를 포함함 |
| `s.replace(old, new[,count])` | old를 new로 바꿈 |
| `s.strip([chars])` | 공백이나 특정 문자 제거 |
| `s.split(sep = None, maxsplit = -1)` | 공백이나 특정 문자를 기준으로 분리 |
| `'separator'.join([iterable])` | 구분자로 iterable을 병합 |
| `s.capitalize()` | 가장 첫 번째 글자를 대문자로 변경 |
| `s.title()` | ' 또는 공백 이후 첫 글자를 대문자로 변경 |
| `s.upper()` | 모두 대문자로 변경 |
| `s.lower()` | 모두 소문자로 변경 |
| `s.swapcase()` | 대문자는 소문자로, 소문자는 대문자로 변경 |
<br></br>

## list
| 문법 | 설명 |
| --- | --- |
| `L.append(x)` | 리스트 마지막에 항목 x 추가 |
| `L.insert(i, x)` | 리스트 인덱스 i에 항목 x 삽입 |
| `L.remnove(x)` | 리스트 가장 왼쪽에 있는 항목(첫 번째) x 제거\n항목이 존재하지 않을 경우 ValueError 발생 |
| `L.pop()` | 리스트 가장 오른쪽에 있는 항목(마지막)을 반환 후 제거 |
| `L.pop(i)` | 리스트의 인덱스 i에 있는 항목을 반환 후 제거 |
| `L.extend(m)` | 순회형 m의 모든 상목을 리스트 끝에 추가(+=) |
| `L.index(x, start, end)` | 리스트에 있는 항목 중 가장 왼쪽에 있는 항목 x의 인덱스 반환 |
| `L.reverse()` | 리스트를 역순으로 뒤집음 |
| `L.sort()` | 리스트 정렬(매개변수 이용가능) |
| `L.count(x)` | 리스트에서 항목 x가 몇 개 존재하는지 반환 |
| `L.clear()` | 모든 항목 삭제 |
<br></br>

## set
| 문법 | 설명 |
| --- | --- |
| `s.copy()` | 세트의 shallow copy를 반환 |
| `s.add(x)` | 항목 x가 세트 s에 없으면 추가 |
| `s.pop()` | 세트 s에서 무작위로 항목을 반환 하고 제거. 빈 세트일 경우 KeyError 발생 |
| `s.remove(x)` | 항목 x를 세트 s에서 제거. 항목이 존재하지 않을 경우 KeyError 발생 |
| `s.discard(x)` | 항목 x가 세트 s에 있는 경우 x를 s에서 제거 |
| `s.update(t)` | 세트 t에 있는 항목 중 s에 없는 항목 추가 |
| `s.clear()` | 모든 항목 제거 |
| `s.isdisjoint(t)` | 세트 s가 세트 t와 공통된 항목을 가지지 않은 경우 True 반환 |
| `s.issubset(t)` | 세트 s가 세트 t의 부분집합일 때 True 반환 |
| `s.issuperset(t)` | 세트 s가 세트 t의 상위집합일 때 True 반환 |
cf) shallow copy: 새로운 객체를 만들고 원본 객체의 참조를 새 객체에 삽입하는 것
<br></br>

## dictionary
| 문법 | 설명 |
| --- | --- |
| `d.clear()` | 모든 항목 제거 |
| `d.keys()` | 딕셔너리 d의 모든 키를 담은 뷰 객체 반환 |
| `d.values()` | 딕셔너리 d의 모든 값을 담은 뷰 객체 반환 |
| `d.items()` | 딕셔너리 d의 모든 키-값의 쌍을 담은 뷰 객체 반환 |
| `d.get(k)` | 키 k의 값 반환. 없을 경우 None 반환 |
| `d.get(k, v)` | 키 k의 값 반환. 없을 경우 v 반환 |
| `d.pop(k)` | 키 k의 값을 반환하고 항목 제거. 없을 경우 KeyError 발생 |
| `d.pop(k, v)` | 키 k의 값을 반환하고 항목 제거. 없을 경우 v 반환 |
| `d.update([other])` | 딕셔너리 d의 값을 매핑하여 업데이트 |