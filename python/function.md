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