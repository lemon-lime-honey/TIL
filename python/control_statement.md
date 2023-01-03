# Control Statement
## Conditional Statement
### Basic
```python
if <expression>:
    # Run this code block
else:
    # Run this code block
```
- expression은 참/거짓에 대한 조건식이다.
    - 조건이 참일 경우 이후 들여쓰기 되어 있는 코드 블럭을 실행한다.
    - 이외의 경우 else 이후 들여쓰기 되어 있는 코드 블럭을 실행한다.

### The elif Clause
```python
if <expr1>:
    # code block 1
elif <expr2>:
    # code block 2
elif <expr3>:
    # code block 3
else:
    # code block 4
```
- elif: else if

### Nested Conditional
```python
if <expr1>:
    # code block 1
    if <expr2>:
        # code block 2
else:
    # code block 3
```
<br></br>

## Loop Statement
### while Loop
```python
while <expression>:
    # code block
```
- 조건이 참인 경우 들여쓰기 되어 있는 코드 블록이 실행된다.
- 코드 블록이 모두 실행된 후 조건식을 검사하고 다시 코드 블록이 실행되는 것을 반복한다.
- 종료 조건이 없으면 무한 루프에 빠지게 된다.

### for Loop
- 시퀀스를 포함한 모든 Iterable한 객체 요소를 모두 순회한다.
- 처음부터 끝까지 모두 순회하므로 종료 조건이 필요하지 않다.

### Loop Control
- `break`: 반복문 종료
- `continue`: 이후의 코드 블록을 수행하지 않고 다음 반복을 수행한다.
- `for-else`
    - 끝까지 반복문을 실행한 후 else문을 실행한다.
    - break를 통해 중간에 종료되는 경우에는 else문을 실행하지 않는다.