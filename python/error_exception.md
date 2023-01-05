# Error and Exception
## Syntax Error
- 문법이 틀렸을 때 발생하며, `SyntaxError`가 발생하면 프로그램이 실행되지 않는다.
- 파일 이름, 줄 번호, `^` 문자를 통해 파이썬이 코드를 읽어 나갈 때(parser) 문제가 발생한 위치를 표현한다.
- 줄에서 에러가 감지된 가장 앞의 위치를 캐럿`caret` 기호(`^`)로 표시한다.
- `EOL`, `EOF`, `invalid syntax`, `cannot assign to literal`
<br></br>

## Exception
- 실행 도중 예상치 못한 상황을 맞이하면 프로그램 실행을 멈춘다.
- 문장이나 표현식이 문법적으로 올바르더라도 발생한다.
- 예외는 여러 타입으로 나타나는데, 타입이 메시지의 일부로 출력된다.
- 모든 내장 예외는 `Exception Class`를 상속받아 이뤄진다.
- 사용자 정의 예외를 만들어 관리할 수 있다.
- `ZeroDivisionError`: 0으로 나누는 일이 생겼을 때 발생한다.
- `NameError`: namespace 상에 이름이 없을 때 발생한다.
- `TypeError`: 타입 불일치, argument 부족, argument 초과 등의 이유로 발생한다.
- `ValueError`: 타입은 올바르나 값이 올바르지 않거나 없는 경우 발생한다.
- `IndexError`: Iterable의 요소 개수에서 벗어나는 index를 사용했을 때 발생한다.
- `KeyError`: Iterable에 없는 key를 사용했을 때 발생한다.
- `ModuleNotFoundError`: 존재하지 않는 모듈을 import할 때 발생한다.
- `ImportError`: 모듈은 있으나 거기 존재하지 않는 클래스나 함수를 import할 때 발생한다.
- `IndentationError`: Indentation이 적절하지 않을 때 발생한다.
- `KeyboardInterrupt`: 임의로 프로그램을 종료했을 때 발생한다.
- 이 외에도 내장 예외가 더 존재한다.
<br></br>

# Handling Exceptions
## try statement
```python
try:
    # code block 1
except group as var1:
    # code block 2
except group as var2:
    # code block 3
else:
    # code block 3
finally:
    # code block 4
```
- `try`를 사용하면 최소한 하나의 `except`를 사용해야 한다. 나머지는 선택사항이다.
- `except`는 `code block 1`에서 예외가 발생했을 때 실행된다.
- `else`는 `code block 1`에서 예외가 발생하지 않았을 때 실행된다.
- `finally`는 예외의 발생 여부와 관계없이 언제나 실행된다.
<br></br>

# Raising Exceptions
## raise statement
```python
raise <expression>(message)
# 이런 식으로
raise ValueError('Wrong!')
```
`raise`를 이용해 예외를 강제로 발생시킬 수 있다.
<br></br>

## assert statement
```python
assert <expression>, <message>
# 이런 식으로
assert DarthSidious == 'Jedi', 'Not Jedi'
```
- `assert`를 이용해 예외를 강제로 발생시킬 수 있다.
- 상태 검증에 사용되며, 표현식이 `False`인 경우 `AssertionError`가 발생한다.
- 일반적으로 디버깅 용도로 사용한다.