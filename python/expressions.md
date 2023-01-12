# Conditional Expression
```python
if <expr>:
    var = value1
else:
    var = value2

var = value1 if <expr> else value2
```
<br></br>

# Displays for lists, sets and dictionaries
- List Comprehension
    ```python
    [<expr1> for <var> in <iterable>]
    [<expr2> for <var> in <iterable> if <condition>]
    ```

- Set Comprehension
    ```python
        {<expr1> for <var> in <iterable>}
        {<expr2> for <var> in <iterable> if <condition>}
    ```

- Dictionary Comprehension
    ```python
    {key: value for <var> in <iterable>}
    {key: value for <var> in <iterable> if <condition>}
    ```
<br></br>

# Lambda Expression
```python
lambda parameters: expression
```
- 람다함수
    - 표현식을 계산한 결과값을 반환하는 함수.
    - 이름이 없으므로 익명함수라고도 한다.
- 특징
    - `return`문을 가질 수 없다.
    - 간편 조건문 외의 조건문이나 반복문을 가질 수 없다.
- 장점
    - 함수를 정의해서 사용하는 것보다 간결하게 사용할 수 있다.
    - `def`를 사용할 수 없는 곳에서도 사용할 수 있다.
