# Collections
[Documentation](https://docs.python.org/3/library/collections.html#module-collections)

## ChainMap objects
*버전 3.3에서 추가*
- 클래스 $\texttt{ChainMap}$은 매핑 된 숫자를 빠르게 연결해 하나의 단위로 취급될 수 있게 해준다. 딕셔너리를 생성하거나 $\texttt{update()}$를 여러 번 호출할 때보다 훨씬 빠를 수 있다.
- 이 클래스는 nested scope를 시뮬레이션 할 때 사용할 수 있으며 templating에 유용하다.
<br></br>

### $\texttt{class collections.ChainMap({\it*maps})}$
$\texttt{ChainMap}$은 여러 개의 딕셔너리나 다른 매핑된 객체들을 묶어 하나의 갱신 가능한 view로 만든다. 만약 $\texttt\it{maps}$가 특정되지 않는다면 새 chain이 언제나 최소 하나의 매핑을 가질 수 있도록 하나의 빈 딕셔너리가 주어진다.
<br><br>
Underlying mapping은 리스트에 저장된다. 이 리스트는 public이며 $\texttt{maps}$ 속성을 사용하는 동안 접근하거나 수정할 수 있다. 다른 상태는 없다.
<br><br>
조회는 키를 발견할 때까지 underlying mapping을 찾는다. 대조적으로, 쓰기, 수정, 그리고 삭제는 오직 첫 mapping에서 동작한다.
<br><br>
$\texttt{ChainMap}$은 underlying mapping을 reference로 포함한다. 그러므로 만약 underlying mapping중 하나가 수정된다면 이 변화는 $\texttt{ChainMap}$에 반영된다.
<br><br>
모든 딕셔너리 메서드가 지원된다. 추가로, subcontext를 새로 만들기 위한 $\texttt{maps}$ 메서드와 첫 번째 mapping 이외의 모든 것에 접근하기 위한 property가 있다.
- $\texttt{maps}$<br>
$\!$ 사용자가 수정할 수 있는 mapping 리스트. 이 리스트는 first-searched부터 lasted-searched로 정렬된다. 오직 저장된 상태이며, 찾은 mapping을 바꾸기 위해 변경될 수 있다. 이 리스트는 반드시 최소 하나의 mapping을 포함해야 한다.
- $\texttt{new}$ _ $\texttt{child(m = None, **kwargs)}$<br>
$\!$ 현재 상황의 모든 map 앞에 새로운 map을 포함하는 새로운 $\texttt{ChainMap}$을 반환한다. Mapping 리스트 가장 앞에 있는 새 map이 되지만 특정되지 않는 경우 빈 딕셔너리가 사용되므로 $\texttt{d.new}$ _ $\texttt{child()}$를 호출하는 것은 $\texttt{ChainMap(\{\}, *d.maps)}$를 호출하는 것과 같다. 만약 어느 keyward argument라도 특정이 된다면, passed map이나 새로운 빈 딕셔너리를 갱신한다. 이 메서드는 어느 parent mapping의 값도 바꾸지 않고 갱신될 수 있는 subcontext를 만드는데 사용된다.<br>
$\!$ *버전 3.4에서의 변경사항*: 선택 parameter $\texttt{m}$이 추가됨<br>
$\!$ *버전 3.10에서의 변경사항*: keyword argument 지원이 추가됨
- $\texttt{parents}$<br>
$\!$ 가장 첫 번째를 제외한 현재 상황의 모든 map을 포함하는 새로운 $\texttt{ChainMap}$을 반환하는 property. 첫 번째 map을 건너뛰고 검색하는데 유용하다. Use case는 Nested scope에서 $\texttt{nonlocal}$ 키워드를 사용하는 것과 비슷하다. 또한 빌트인 $\texttt{super()}$ 함수의 그것과 유사하다. $\texttt{d.parents}$의 reference는 $\texttt{ChainMap(*d.maps[1:])}$과 동등하다.
<br><br>

참고: $\texttt{ChainMap()}$의 iteration 순서는 마지막부터 처음까지 mapping을 스캔하는 것으로 정해진다.
```python
>>> baseline = {'music': 'bach', 'art': 'rembrandt'}
>>> adjustments = {'art': 'van gogh', 'opera': 'carmen'}
>>> list(ChainMap(adjustments, baseline))
['music', 'art', 'opera']
```
$\texttt{dict.update()}$의 연속이 마지막 mapping부터 시작하는 것과 같은 순서
```python
>>> combined = baseline.copy()
>>> combined.update(adjustments)
>>> list(combined)
['music', 'art', 'opera']
```
*버전 3.9에서의 변경사항*: `|`와 `|=` 연산자 지원이 추가됨. [PEP584](https://peps.python.org/pep-0584/) 참조
<br><br>

## Counter objects
$\texttt{Counter}$는 편하고 빠른 계수기를 제공합니다.
```python
>>> # Tally occurrences of words in a list
>>> cnt = Counter()
>>> for word in ['red', 'blue', 'red', 'green', 'blue', 'blue']:
...     cnt[word] += 1
>>> cnt
Counter({'blue': 3, 'red': 2, 'green': 1})

>>> # Find the ten most common words in Hamlet
>>> import re
>>> words = re.findall(r'\w+', open('hamlet.txt').read().lower())
>>> Counter(words).most_common(10)
[('the', 1143), ('and', 966), ('to', 762), ('of', 669), ('i', 631), 
 ('you', 554), ('a', 546), ('my', 514), ('hamlet', 471), ('in', 451)]
```
<br><br>

### $\texttt{class collections.Counter([{\it iterable-or-mapping}])}$
$\texttt{Counter}$는 hashable object를 세기 위한 딕셔너리의 subclass이다. 원소는 딕셔너리의 키로, 그 개수는 딕셔너리의 값으로 저장되는 collection이다. Count는 0이나 음수를 포함하는 어떠한 정수 값도 가능하다. $\texttt{Counter}$ 클래스는 다른 언어의 `bags`나 `multiset`과 유사하다.
<br><br>
Iterable에서 원소의 수를 세거나 다른 mapping 혹은 $\texttt{Counter}$에서 원소를 초기화할 수 있다.
```python
>>> c = Counter()                       # a new, empty counter
>>> c = Counter('gallahad')             # a new counter from an iterable
>>> c = Counter({'red': 4, 'blue': 2})  # a new counter from a mapping
>>> c = Counter(cats = 4, dogs = 8)     # a new counter from keyword args
```
$\texttt{Counter}$ object는 `keyError`를 발생시키는 대신 없는 원소에 0을 반환하는 것을 제외하면 딕셔너리와 유사한 interface를 가진다.
```python
>>> c = Counter(['eggs', 'ham'])
>>> c['bacon']                          # count of a missing element is zero
0
```
Count를 0으로 정하는 것은 $\texttt{Counter}$에서 원소를 제거하지 않는다. 제거하려면 `del`을 사용한다.
```python
>>> c['sausage'] = 0                    # counter entry with a zero count
>>> del c['sausage']                    # del actually removes the entry
```
*버전 3.1에서 추가됨*<br>
*버전 3.7에서의 변경사항*: $\texttt{Counter}$는 딕셔너리의 subclass이므로 입력 순서를 기억하는 기능을 상속한다. $\texttt{Counter}$ object에서의 수학 연산 또한 순서를 보존한다. 결과는 원소가 왼쪽 피연산자에서 처음 발견될 때부터 오른쪽 피연산자에서 발견되는 순서로 정렬된다.
<br><br>
$\texttt{Counter}$ object는 딕셔너리에 유효한 것 뿐만이 아니라 다음과 같은 추가적인 메서드를 지원한다.
- $\texttt{elements()}$<br>
    원소가 각각 그 수만큼 반복되는 이터레이터를 반환한다. 원소는 입력된 순서대로 반환된다. 만약 원소의 수가 1보다 작으면 $\texttt{elements()}$는 이 원소를 무시한다.
    ```python
    >>> c = Counter(a = 4, b = 2, c = 0, d = -2)
    >>> sorted(c.elements())
    ['a', 'a', 'a', 'a', 'b', 'b']
    ```
- $\texttt{most}$ _ $\texttt{common([n])}$<br>
    n개의 가장 빈도가 높은 원소와 그 개수의 목록을 가장 많은 것부터 적은 것까지의 순서로 반환한다. 만약 n이 생략되거나 `None`이라면, $\texttt{most}$ _ $\texttt{common()}$은 $\texttt{Counter}$의 모든 원소를 반환한다. 동일한 수의 원소는 입력된 순서대로 정렬된다.
    ```python
    >>> Counter('abracadabra').most_common(3)
    [('a', 5), ('b', 2), ('r', 2)]
    ```
- $\texttt{subtract([iterable-or-mapping])}$<br>
    iterable이나 다른 mapping(또는 $\texttt{Counter}$)로 원소를 감소시킨다. $\texttt{dict.update()}$와 유사하나 대체하는 대신 개수를 줄인다. 입력과 출력 모두 0 또는 음수일 수 있다.
    ```python
    >>> c = Counter(a = 4, b = 2, c = 0, d = -2)
    >>> d = Counter(a = 1, b = 2, c = 3, d = 4)
    >>> c.subtract(d)
    >>> c
    Counter({'a': 3, 'b': 0, 'c': -3, 'd': -6})
    ```
    *버전 3.2에서 추가됨*
- $\texttt{total()}$<br>
    개수의 합을 계산한다.
    ```python
    >>> c = Counter(a = 10, b = 5, c = 0)
    >>> c.total()
    15
    ```
    *버전 3.10에서 추가됨*<br>

대부분의 딕셔너리 메서드는 $\texttt{Counter}$에서는 다르게 동작하는 둘을 제외하면 $\texttt{Counter}$ object에서도 사용 가능하다.
- $\texttt{fromkeys(iterable)}$<br>
    이 메서드는 $\texttt{Counter}$ object를 위해 구현되지 않았다.
- $\texttt{update([iterable-or-mapping])}$
    iterable이나 다른 mapping(또는 $\texttt{Counter}$)로부터 원수의 개수를 구한다. $\texttt{dict.update()}$와 유사하나 개수를 대체하는 대신 더한다. 또한, iterable은 `(key, value)`쌍의 나열이 아닌 원소의 나열이어야 한다.

$\texttt{Counter}$는 `==`, `!=`, `<`, `<=`, `>`, `>=`와 같은 equality, subset, superset 관계에 관한 다양한 관계 연산자를 지원한다. 이러한 종류의 모든 test는 없는 원소를 0을 가지고 있는 것으로 취급해 `Counter(a = 1) = Counter(a = 1, b = 0)`이 `True`를 반환하도록 한다.

*버전 3.10에서 추가됨*: 다양한 관계 연산자 추가<br>
*버전 3.10에서 변경됨*: Equality text에서 없는 원소는 count가 0인 것으로 취급된다. 이전에는 `Counter(a = 3)`과 `Counter(a = 3, b = 0)`이 다른 것으로 취급되었다.

$\texttt{Counter}$ object를 사용하는 보편적인 방법
```python
c.total()                     # total of all counts
c.clear()                     # reset all counts
list(c)                       # list unique elements
set(c)                        # convert to a set
dict(c)                       # convert to a regular dictionary
c.items()                     # convert to a list of (elem, cnt) pairs
Counter(dict(list_of_pairs))  # convert from a list of (elem, cnt) pairs
c.most_common()[:-n-1:-1]     # n least common elements
+c                            # remove zero and negative counts
```

$\texttt{Counter}$ object를 결합해 multiset(0을 초과하는 count를 가지는 $\texttt{Counter}$)을 만들 수 있도록 여러 수학 연산자가 제공된다. 덧셈과 뺄셈은 $\texttt{Counter}$의 상응하는 원소들의 count를 더하거나 빼는 방법으로 결합한다. 차집합과 교집합은 상응하는 count의 최소와 최대를 반환한다. Equality와 inclusion은 상응하는 count를 비교한다. 부호가 있는 count의 입력 또한 각각의 연산에서 유효하나 0보다 작거나 같은 count를 제외한 결과값이 출력된다.
```python
>>> c = Counter(a = 3, b = 1)
>>> d = Counter(a = 1, b = 2)
>>> c + d                      # add two counters together: c[x] + d[x]
Counter({'a': 4, 'b': 3})
>>> c - d                      # subtract (keeping only positive counts)
Counter({'a': 2})
>>> c & d                      # intersection: min(c[x], d[x])
Counter({'a': 1, 'b': 1})
>>> c | d                      # union: max(c[x], d[x])
Counter({'a': 3, 'b': 2})
>>> c == d                     # equality: c[x] == d[x]
False
>>> c <= d                     # inclusion: c[x] <= d[x]
False
```

Unary addition과 subtraction은 빈 $\texttt{Counter}$에서 더하거나 빼기 위한 shortcut이다.
```python
>>> c = Counter(a = 2, b = -4)
>>> +c
Counter({'a': 2})
>>> -c
Counter({'b': 4})
```
*버전 3.3에서 추가됨*: Unary plus, unary minus, 그리고 in-place multiset 연산 지원 
<br><br>

## Deque objects
### $\texttt{class collections.deque([{\it iterable}, [, {\it maxlen}]])}$
Iteralbe로부터 데이터를 ($\texttt{append()}$를 사용하여) left-to-right으로 초기화된 새로운 $\texttt{deque}$ object를 반환한다. 만약 iterable이 특정되지 않는다면 새로운 $\texttt{deque}$는 비어있다.

"deck"으로 발음이 되고, "double-ended queue"의 약어인 $\texttt{deque}$는 `stack`과 `queue`의 일반화된 형태이다. $\texttt{deque}$는 $\texttt{deque}$ 양 끝에서의 `append`와 `pop`을 지원하는데, 이는 thread-safe하고 메모리를 효율적으로 사용하며, 어느 방향에서든 같은 `O(1)`의 성능을 보인다.

$\texttt{list}$ object가 유사한 연산을 지원하지만, 이는 빠른 고정된 길이의 연산에 최적화되어 있으며 underlying data representation에 있어 크기와 위치를 모두 바꾸는 `pop(0)`과 `insert(0, v)` 연산 에서는 `O(n)`의 메모리 이동 비용이 발생한다.

만약 *maxlen*이 특정되지 않았거나 `None`이라면, $\texttt{deque}$는 임의의 길이로 늘어날 수 있다. 그게 아니라면, $\texttt{deque}$는 특정된 최대 길이로 한정된다. 한정된 크기의 $\texttt{deque}$가 다 차면 새로운 원소가 추가되었을 때 해당하는 수 만큼의 원소가 반대쪽에서 버려진다. 고정 길이 $\texttt{deque}$는 Unix의 `tail` 필터와 유사한 기능을 제공한다. Transaction를 추적하거나 가장 최근의 활동만 관심의 대상인 데이터 풀에 유용하다.

$\texttt{deque}$ object는 다음 메서드를 지원한다.

- $\texttt{append(x)}$<br>
    $\texttt{deque}$의 오른쪽에 $\texttt{x}$를 추가한다.

- $\texttt{appendleft(x)}$<br>
    $\texttt{deque}$의 왼쪽에 $\texttt{x}$를 추가한다.

- $\texttt{clear()}$<br>
    $\texttt{deque}$의 모든 원소를 제거해 길이를 0으로 만든다.

- $\texttt{copy}$<br>
    $\texttt{deque}$의 얕은 복사를 만든다.<br>
    *버전 3.5에서 추가됨*

- $\texttt{count}$<br>
    값이 $\texttt{x}$인 $\texttt{deque}$의 원소의 개수를 센다.<br>
    *버전 3.2에서 추가됨*

- $\texttt{extend(iterable)}$<br>
    Iterable의 원소를 추가해 $\texttt{deque}$ 오른편을 늘인다.

- $\texttt{extendleft(iterable)}$<br>
    Iterable의 원소를 추가해 $\texttt{deque}$ 왼편을 늘인다. Left append의 연속은 iterable의 원소의 순서를 뒤집는다는 점에 유의한다.

- $\texttt{index(x[, start[, stop]])}$<br>
    (인덱스 *start*부터 혹은 그 이후 그리고 인덱스 *stop* 전까지의) $\texttt{deque}$에서의 $\texttt{x}$의 위치를 반환한다. 가장 처음으로 발견한 위치를 반환하거나 찾지 못한 경우 `ValueError`를 발생시킨다.<br>
    *버전 3.5에서 추가됨*

- $\texttt{insert(i, x)}$<br>
    $\texttt{deque}$의 위치 $\texttt{i}$에 $\texttt{x}$를 넣는다. 만약 데이터를 넣는 것이 고정 $\texttt{deque}$의 길이가 *maxlen*을 초과하게 한다면 `IndexError`가 발생한다.<br>
    *버전 3.5에서 추가됨*

- $\texttt{pop()}$<br>
    $\texttt{deque}$ 오른쪽에서 원소 하나를 제거하고 반환한다. 만약 원소가 없다면 `IndexError`를 발생시킨다.

- $\texttt{popleft()}$<br>
    $\texttt{deque}$ 왼쪽에서 원소 하나를 제거하고 반환한다. 만약 원소가 없다면 `IndexError`를 발생시킨다.

- $\texttt{remove(value)}$<br>
    처음 찾은 $\texttt{value}$를 제거한다. 발견하지 못하면 `ValueError`를 발생시킨다.

- $\texttt{reverse}$<br>
    $\texttt{deque}$의 원소 순서를 제자리에서 뒤집고 `None`을 반환한다.<br>
    *버전 3.2에서 추가됨*

- $\texttt{rotate(n = 1)}$<br>
    $\texttt{deque}$를 *n*씩 오른쪽으로 회전한다. 만약 *n*이 음수이면 왼쪽으로 회전한다.<br>
    $\texttt{deque}$가 비어있지 않을 때, 오른쪽으로 1 회전하는 것은 `d.appendleft(d.pop())`와 동일하며, 왼쪽으로 1 회전하는 것은 `d.append(d.popleft())`와 동일하다.

$\texttt{deque}$ object는 하나의 읽기 전용 속성을 제공한다.

- $\texttt{maxlen}$<br>
    $\texttt{deque}$의 최대 크기 혹은 크기가 고정되지 않은 경우 `None`<br>
    *버전 3.1에서 추가됨*

위에 더해, $\texttt{deque}$는 iteration, pickling, `len(d)`, `reversed(d)`, `copy.copy(d)`, `copy.deepcopy(d)`, `in` 연산자를 활용한 membership 테스트, 그리고 첫번째 원소에 접근하기 위한 `d[0]`과 같은 인덱스 접근을 제공한다.

버전 3.5부터 $\texttt{deque}$는 `__add__()`, `__mul__()` 그리고 `__imul__()`을 지원한다.

예시:
```python
>>> from collections import deque
>>> d = deque('ghi')        # make a new deque with three items
>> for elem in d:           # iterate over the deque's elements
...    print(elem.upper())
G
H
I

>>> d.append('j')           # add a new entry to the right side
>>> d.appendleft('f')       # add a new entry to the left side
>>> d                       # show the representation of the deque
deque(['f', 'g', 'h', 'i', 'j'])

>>> d.pop()                 # return and remove the rightmost item
'j'
>>> d.popleft()             # return and remove the leftmost item
'f'
>>> list(d)                 # list the contents of the deque
['g', 'h', 'i']
>>> d[0]                    # peek at leftmost item
'g'
>>> d[-1]                   # peek at rightmost item
'i'

>>> list(reversed(d))       # list the contents of a deque in reverse
['i', 'h', 'g']
>>> 'h' in d                # search the deque
True
>>> d.extend('jkl')         # add multiple elements at once
>>> d
deque(['g', 'h', 'i', 'j', 'k', 'l'])
>>> d.rotate(1)             # right rotation
>>> d
deque(['l', 'g', 'h', 'i', 'j', 'k'])
deque.rotate(-1)            # left rotation
>>> d
deque(['g', 'h', 'i', 'j', 'k', 'l'])

>>> deque(reversed(d))      # make a new deque in reverse order
deque(['l', 'k', 'j', 'i', 'h', 'g'])
>>> d.clear()               # empty the deque
>>> d.pop()                 # cannot pop from an empty deque
Traceback (most recent call last):
    File "<pyshell#6>", line 1, in -toplevel-
        d.pop()
IndexError: pop from an empty deque

>>> d.extendleft('abc')     # extendleft() reverses the input order
>>> d
deque(['c', 'b', 'a'])
```
<br><br>

## Defaultdict objects
### $\texttt{class collections.defaultdict({\it default}}$ _ $\texttt{{\it factory=None}, /[, ...])}$
딕셔너리와 유사한 새 객체를 반환한다. $\texttt{defaultdict}$는 built-in `dict` 클래스의 subclass이다. 하나의 메서드를 덮어씌우고, 하나의 쓰기 가능한 instance 변수를 추가한다. 남은 기능은 `dict` 클래스의 그것과 같으므로 여기서는 기술하지 않는다.

첫 번째 인수는 `default_factory` 속성을 위한 초기값을 제공한다. 기본값은 `None`이다. 모든 남은 인수는 키워드 인수를 포함한 `dict` 생성자로 전달되는 것처럼 취급된다.

$\texttt{defaultdict}$ 객체는 표준 `dict` 연산에 더해 다음의 메서드를 지원한다.

- __ $\texttt{missing}$ __ $\texttt{(key)}$<br>
    만약 $\texttt{default}$ _ $\texttt{factory}$ 속성이 `None`이라면, 이 메서드는 *key*를 인수로 `KeyError` 예외를 발생시킨다.

    만약 $\texttt{default}$ _ $\texttt{factory}$가 `None`이 아니라면, 주어진 *key*를 위한 기본값을 제공하지 않고 호출된 후 딕셔너리에 이 값을 *key*를 위한 값으로 넣고 반환한다.

    $\texttt{default}$ _ $\texttt{factory}$를 호출하는 것이 예외를 발생시킨다면 이 예외는 바뀌지 않은 채 전파된다.

    이 메서드는 요청받은 키를 찾을 수 없을 때 `dict` 클래스의 `__getitem___()` 메서드에 의해 호출된다. 무엇을 반환하거나 발생시키거나, 그 다음에는 `__getitem__()`에 의해 반환되거나 발생한다.

    `__missing__()`은 `__getitem__()`뿐만 아니라 어느 연산을 위해서도 호출되지 *않는다*. 이는 다른 평범한 딕셔너리처럼 $\texttt{default}$ _ $\texttt{factory}$를 사용하는 대신 `get()`이 기본값으로 `None`을 반환한다는 의미이다.

$\texttt{defaultdict}$ 객체는 다음의 instance 변수를 지원한다.

- $\texttt{default}$ _ $\texttt{factory}$
    이 속성은 `__missing__()` 메서드에 의해 사용된다. 이것은 생성자의 첫 인수가 있다면 그것으로, 없다면 `None`으로 초기화된다.

*버전 3.9에서 변경됨*: `merge(|)`와 `update(|=)` 연산자 추가. [PEP 584](https://peps.python.org/pep-0584/) 참조.
<br><br>

## $\texttt{namedtuple()}$: Factory Function with Named Fields
Named tuple은 튜플의 각 위치에 의미를 할당해 더 가독성이 좋은 self-documenting 코드가 될 수 있게 한다. 일반적인 튜플이 사용되는 곳이라면 어디든지 사용될 수 있고, 인덱스 대신 이름으로 field에 접근할 수 있게 된다.

- $\texttt{collections.namedtuple({\it typename, field}}$ _ $\texttt{{\it names, *, rename=False, defaults=None, module=None})}$<br>
    *typename*으로 명명된 새로운 튜플 서브클래스를 반환한다. 새로운 서브클래스는 인덱싱과 순회가 가능할 뿐만 아니라 속성 색인으로 접근 가능한 field를 가진 튜플과 유사한 객체를 만드는데 사용된다. 서브클래스의 인스턴스는 또한 (`typename`과 `field_names`를 포함하는) 유용한 주석과 `name=value` 형식으로 튜플의 내용을 나열하는 `__repr__()` 메서드를 가진다.

    `field_names`는 `['x', 'y']`와 같이 문자열의 시퀀스이다. 또는, `'x y'`나 `'x, y'`와 같이 각 field명을 공백 또는 공백과 콤마로 구분한 하나의 하나의 문자가 될 수도 있다.

    유효한 파이썬 식별자라면 언더스코어로 시작하는 이름을 제외한 이름을 fieldname으로 사용할 수 있다. 유효한 식별자는 문자, 숫자, 그리고 언더스코어로 구성되나 숫자나 언더스코어로는 시작하지 않으며, *class*, *for*, *return*, *global*, *pass* 또는 *raise*와 같은 `keyword`는 사용할 수 없다.

    만약 *rename*이 `True`라면, 유효하지 않은 fieldname은 자동적으로 위치에 관한 이름들로 교체된다. 예를 들어 `['abc', 'def', 'ghi', 'abc']`는 키워드 `def`와 중복되는 fieldname `abc`를 제거해 `['abc', '_1', 'ghi', '_3']`으로 변환된다.

    *defaults*는 `None` 또는 기본값의 iterable이 될 수 있다. 기본값을 가진 field는 반드시 기본값이 없는 field 이후에 있어야 하기 때문에 `defaults`는 우측에 있는 파라미터에 적용되어야 한다. 예를 들어, 만약 fieldname이 `['x', 'y', 'z']`이고 기본값이 `(1, 2)`라면, `x`는 required argument가 되고, `y`의 기본값은 `1`, `z`의 기본값은 `2`가 된다.

    만약 *module*이 정의되었다면, named tuple의 `__module__` 속성은 그 값으로 설정된다.

    Named tuple 인스턴스는 per-instance 딕셔너리를 가지지 않기 때문에 가벼우며 일반적인 튜플보다 적은 메모리를 필요로 한다.

    pickling을 지원하기 위하여, named tuple 클래스는 *typename*과 매치되는 변수에 할당되어야 한다.

    *버전 3.1에서 변경됨*: `rename` 지원이 추가됨<br>
    *버전 3.6에서 변경됨*: `verbose`와 `rename` 파라미터가 keyword-only 인수가 됨<br>
    *버전 3.6에서 변경됨*: `module` 파라미터가 추가됨<br>
    *버전 3.7에서 변경됨*: `verbose` 파라미터와 `_source` 속성이 제거됨<br>
    *버전 3.7에서 변경됨*: `defaults` 파라미터와 `_field_defaults` 속성이 추가됨

```python
>>> # Basic example
>>> Point = namedtuple('Point', ['x', 'y'])
>>> p = Point(11, y=22)  # instantiate with positional or keyword arguments
>>> p[0] + p[1]          # indexable like the plain tuple (11, 22)
33
>>> x, y = p             # unpack like a regular tuple
>>> x, y
(11, 22)
>>> p.x + p.y            # fields also accessible by name
33
>>> p                    # readable __repr__ with a name=value style
Point(x=11, y=22)
```
Named tuple은 `csv`나 `sqlite3` 모듈에 의해 반환되는 결과 튜플의 field name을 할당하는 데에 특히 유용하다.
```python
EmployeeRecord = namedtuple('EmployeeRecord', 'name, age, title, department, paygrade')

import csv
for emp in map(EmployeeRecord._make, csv.reader(open("employees.csv", "rb"))):
    print(emp.name, emp.title)

import sqlite3
conn = sqlite3.connect('/companydata')
cursor = conn.cursor()
cursor.execute('SELECT name, age, title, department, paygrade FROM employees')
for emp in map(EmployeeRecord._make, cursor.fetchall()):
    print(emp.name, emp.title)
```

튜플로부터 상속받은 메서드에 추가해, named tuple은 세 개의 추가적인 메서드와 두 개의 속성을 지원한다. field name 충돌을 방지하기 위해, 메서드와 속성 이름은 언더스코어로 시작한다.

- $\texttt{classmethod somenamedtuple.}$ _ $\texttt{make(iterable)}$<br>
    존재하는 시퀀스나 iterable로부터 새 인스턴스를 만드는 클래스 메서드
    ```python
    >>> t = [11, 22]
    >>> Point._make(t)
    Point(x=11, y=22)
    ```

- $\texttt{somenamedtuple.}$ _ $\texttt{asdict()}$<br>
    field name을 해당하는 값에 매핑하는 새로운 딕셔너리를 반환한다.
    ```python
    >>> p = Point(x=11, y=22)
    >>> p._asdict()
    {'x': 11, 'y': 22}
    ```
    *버전 3.1에서 변경됨*: 일반적인 `dict` 대신 `OrdedredDict`를 반환함<br>
    *버전 3.8에서 변경됨*: `OrderedDict` 대신 일반적인 `dic`를 반환함. 파이썬 3.7에서 일반적인 딕셔너리는 정렬됨이 보장됨. 만약 `OrderedDict`의 다른 특징이 요구된다면, 형변환을 추천함: `OrderedDict(nt._asdict())`

- $\texttt{somenamedtuple.}$ _ $\texttt{replace(**kwargs)}$<br>
    특정된 field를 새로운 값으로 대체하는 새 named tuple 인스턴스를 반환한다.
    ```python
    >>> p = Point(x=11, y=22)
    >>> p._replace(x=33)
    Point(x=33, y=22)

    >>> for partnum, record in inventory.items():
    ...     inventory[partnum] = record._replace(price=newprices[partnum], timestamp=time.now())
    ```

- $\texttt{somenamedtuple.}$ _ $\texttt{fields}$<br>
    Field name을 나열하는 문자열의 튜플. Introspection과 이미 존재하는 named tuple로부터 새 named tuple을 만드는데 유용하다.
    ```python
    >>> p._fields    # view the field names
    ('x', 'y')

    >>> Color = namedtuple('Color', 'red green blue')
    >>> Pixel = namedtuple('Pixel', Point._fields + Color._fields)
    >>> Pixel(11, 22, 128, 255, 0)
    Pixel(x=11, y=22, red=128, green=255, blue=0)
    ```

- $\texttt{somenamedtuple.}$ _ $\texttt{field}$ _ $\texttt{defaults}$<br>
    기본값에 field name을 매핑하는 딕셔너리.
    ```python
    >>> Account = namedtuple('Account', ['type', 'balance'], defaults=[0])
    >>> Account._field_defaults
    {'balance': 0}
    >>> Account('premium')
    Account(type='preminum', balance=0)
    ```

문자열에 저장된 field name을 찾으려면 `getattr()` 함수를 사용한다.
```python
>>> getattr(p, 'x')
11
```

딕셔너리를 named tuple로 변환하려면 [unpacking argument lists](https://docs.python.org/3/tutorial/controlflow.html#tut-unpacking-arguments)에서 서술하는 것처럼 double-star 연산자를 사용한다.
```python
>>> d = {'x': 11, 'y': 22}
>>> Point(**d)
Point(x=11, y=22)
```

Named tuple은 정식 파이썬 클래스이기 때문에 서브클래스로 기능을 추가하거나 바꾸기 쉽다. 다음은 계산된 field와 고정폭 출력 포멧을 추가하는 예시이다.
```python
>>> class Point(namedtuple('Point', ['x', 'y'])):
...    __slots__ = ()
...    @property
...    def hypot(self):
...        return (self.x ** 2 + self.y ** 2) ** 0.5
...    def __str__(self):
...        return 'Point: x=%6.3f y=6.3f hypot=%6.3f' % (self.x, self.y, self.hypot)

>>> for p in Point(3, 4), Point(14, 5/7):
...    print(p)
Point: x= 3.000 y= 4.000 hypot= 5.000
Point: x=14.000 y= 0.714 hypot=14.018
```
위의 서브클래스는 `__slots__`를 빈 튜플로 설정한다. 이는 인스턴스 딕셔너리의 생성을 방지해 메모리 요구사항을 낮게 유지하는데 도움이 된다.

서브클래스를 만드는 것은 새로운, 저장된 field를 추가하는 데에는 유용하지 않다. 대신 `_fields` 속성으로 새로운 named tuple 타입을 만든다.
```python
>>> Point3D = namedtuple('Point3D', Point._fields + ('z',))
```

주석은 `__doc__` field에 직접 할당을 하는 것으로 customize 할 수 있다.
```python
>>> Book = namedtuple('Book', ['id', 'title', 'authors'])
>>> Book.__doc__ += ': Hardcover book in active collection'
>>> Book.id.__doc__ = '13-digit ISBN'
>>> Book.title.__doc__ = 'Title of first printing'
>>> Book.authors.__doc__ = 'List of authors sorted by last name'
```
*버전 3.5에서 변경됨*: Property 주석이 쓰기 가능해짐
<br>

## $\texttt{OrderedDict}$ Objects
Ordered dictionary는 일반적인 딕셔너리와 같지만 정렬 연산에 관한 몇 가지 추가적인 기능을 가진다. 빌트인 딕셔너리 클래스가 입력 순서를 기억할 수 있게 되며 덜 중요해졌다. (파이썬 3.7)

딕셔너리와의 차이점 몇 가지는 여전히 남아있다.
- 일반적인 딕셔너리는 우수하게 mapping 연산을 하도록 설계되었다. 입력 순서를 추적하는 것은 후순위이다.

- $\texttt{OrderedDict}$는 우수하게 재배열 연산을 하도록 설계되었다. 공간 효율, 순회 속도, 그리고 업데이트 연산의 성능은 후순위이다.

- $\texttt{OrderedDict}$ 알고리즘은 빈도가 높은 재배열 연산을 `dict`보다 잘 다룬다. 아래의 예시들에서 보듯이, 다양한 종류의 LRU 캐시를 구현하는데 적합하다.

- $\texttt{OrderedDict}$에서의 equality 연산은 matching 순서를 확인한다.<br>
`dict`는 순서까지 고려하는 equality 테스트를 `p == q and all(k1 == k2 for k1, k2 in zip[p, q])`로 구현할 수 있다.<br>

- $\texttt{OrderedDict}$의 `popitem()` 메서드는 다른 형태를 가진다. 어느 아이템이 나올지 특정하는 추가 인수를 받을 수 있다.<br>
`dict`는 $\texttt{OrderedDict}$의 가장 우측에 위치한(마지막) 원소를 pop하는 `od.popitem(last=True)`를 `d.popitem()`으로 구현할 수 있다.<br>
`dict`는 $\texttt{OrederedDict}$의 만약 존재한다면 가장 좌측에 위치한(첫번째) 원소를 반환하고 제거하는 `od.popitem(last=False)`를 `(k := next(iter(d)), d.pop(k))`로 구현할 수 있다.

- $\texttt{OrderedDict}$는 원소를 마지막 지점으로 효율적으로 재위치시키는 `move_to_end()` 메서드를 가진다.<br>
`dict`는 $\texttt{OrderedDict}$에서 키와 값을 가장 우측으로 이동시키는 `od.move_to_end(k, last=True)`를 `d[k] = d.pop(k)`으로 구현할 수 있다.<br>
`dict`는 $\texttt{OrderedDict}$에서 키와 값을 가장 좌측으로 이동시키는 `od.move_to_end(k, last=False)`와 동등한 효율적인 방법을 가지지 못한다.

- 파이썬 3.8전까지, `dict`에는 `__reversed__()` 메서드가 없었다.
<br><br><br>
- $\texttt{class collections.OrderedDict([{\it items}])}$<br>
    딕셔너리 순서를 재배열하는데 특화된 메서드를 가진 `dict` 서브클래서의 인스턴스를 반환한다.

    *버전 3.1에서 추가됨*

    - $\texttt{popitem(last=True)}$<br>
        Ordered dictionary의 `popitem()` 메서드는 (키, 값) 쌍을 반환하고 제거한다. 각각의 쌍은 *last*가 `True`이면 LIFO, `False`이면 FIFO 순서로 반환된다.

    - $\texttt{move}$ _ $\texttt{to}$ _ $\texttt{end(key, last=True)}$
        존재하는 키를 ordered dictionary의 어느 쪽 끝으로 이동시킨다. *last*가 `True`(기본값)일 때에는 오른쪽 끝, *last*가 `False`일 때에는 왼쪽 끝으로 옮긴다. 키가 존재하지 않으면 `KeyError`를 발생시킨다.

        ```python
        >>> d = OrderedDict.fromkeys('abcde')
        >>> d.move_to_end('b')
        >>> ''.join(d)
        'acdeb'
        >>> d.move_to_end('b', last=False)
        >>> ''.join(d)
        'bacde'
        ```

        *버전 3.2에서 추가됨*

일반적인 mapping 메서드에 더해, ordered dictionary는 `reversed()`를 사용한 반전 순회 또한 지원한다.

$\texttt{OrderedDict}$ 객체 사이의 equality 테스트는 순서를 고려하며, `list(od1.items())==list(od2.items())`로 구현된다. $\texttt{OrderedDict}$ 객체와 다른 `Mapping` 객체 사이의 equality 테스트는 일반적인 딕셔너리처럼 순서를 고려하지 않는다. 이 경우 일반적인 딕셔너리가 사용되는 곳이라면 어디든 $\texttt{OrderedDict}$로 대체될 수 있다.

*버전 3.5에서 변경됨*: $\texttt{OrderedDict}$의 아이템, 키, 값 view는 이제 `reversed()`를 사용한 반전순회를 지원함<br>
*버전 3.6에서 변경됨*: [PEP468](https://peps.python.org/pep-0468/)에서 보듯이, $\texttt{OrderedDict}$ 생성자와 `update()`메서드로 전달되는 키워드 인수의 순서가 유지됨<br>
*버전 3.9에서 변경됨*: [PEP584](https://peps.python.org/pep-0584/)에서 기술되었듯이, merge(`|`)와 update(`|=`) 연산자가 추가됨

## $\texttt{OrderedDict}$ 사용예시
키가 최종적으로 삽입된 순서를 기억하는 ordered dictionary를 만드는 것은 어렵지 않다. 만약 새로운 entry가 이미 존재하는 entry를 덮어쓴다면, 기존 삽입 위치는 변경되며 끝으로 이동한다.
```python
class LastUpdatedOrderedDict(OrderedDict):
    'Store items in the order the keys were last added'

    def __setitem__(self.key, value):
        super().__setitem__(key, value)
        self.move_to_end(key)
```

$\texttt{OrderedDict}$는 또한 `functools.lru_cache()`를 다르게 구현하는데에도 유용하다.
```python
from time import time

class TimeBoundedLRU:
    "LRU Cache that invalidates and refreshed old entries."

    def __init__(self, func, maxsize=128, maxage=30):
        self.cache = OrderedDict()     # {args : (timestamp, result)}
        self.func = func
        self.maxsize = maxsize
        self.maxage = maxage
    
    def __call__(self, *args):
        if args in self.cache:
            self.cache.move_to_end(args)
            timestamp, result = self.cache[args]
            if time() - timestamp <= self.maxage:
                return result
        result = self.func(*args)
        self.cache[args] = time(), result
        if len(self.cache) > self.maxsize:
            self.cache.popitem(0)
        return result
```

```python
class MultiHitLRUCache:
    """ LRU cache that defers caching a result until
        it has been requested multiple times.

        To avoid flushing the LRU cache with one-time requests,
        we don't cache until a request has been made more than once.
    """

    def __init__(self, func, maxsize=128, maxrequests=4096, cache_after=1):
        self.requests = OrderedDict()  # { uncached_key : request_count }
        self.cache = OrderedDict()     # { cached_key : function_result }
        self.func = func
        self.maxrequests = maxrequests # max number of uncached requests
        self.maxsize = maxsize         # max number of stored return values
        self.cache_after = cache_after
    
    def __call__(self, *args):
        if args in self.cache:
            self.cache.move_to_end(args)
            return self.cache[args]
        result = self.func(*args)
        self.requests[args] = self.requests.get(args, 0) + 1
        if self.requests[args] <= self.cache_after:
            self.requests.move_to_end(args)
            if len(self.requests.) > self.maxrequests:
                self.requests.popitem(0)
        else:
            self.requests.pop(args, None)
            self.cache[args] = result
            if len(self.cache) > self.maxsize:
                self.cache.popitem(0)
        return result
```
<br><br>

## $\texttt{UserDict}$ objects
$\texttt{UserDict}$는 딕셔너리 객체를 감싸는 wrapper처럼 동작한다. 이 클래스의 필요성은 `dict`로부터 직접 서브클래스를 만드는 기능으로 부분적으로 대체되었으나, 이 클래스는 underlying 딕셔너리에 속성으로 접근할 수 있기 때문에 좀 더 다루기 쉽다.

- $\texttt{class collections.UserDict([{\it initialdata}])}$<br>
    딕셔너리를 구현하는 클래스. 인스턴스의 내용은 $\texttt{UserDict}$ 인스턴스의 `data` 속성을 통해 접근할 수 있는 일반적인 딕셔너리에 저장된다. 만약 *initialdata*가 주어졌다면, `data`는 그 내용으로 초기화된다. *initialdata*의 레퍼런스는 저장되지 않아 다른 목적을 위해 사용될 수 있게 된다는 점을 참고하라.

    Mapping의 메서드와 연산을 지원하기 위해 $\texttt{UserDict}$ 인스턴스는 다음과 같은 속성을 제공한다.

    - $\texttt{data}$<br>
        $\texttt{UserDict}$ 클래스의 내용을 저장하기 위해 사용되는 일반적인 딕셔너리.
<br><br>

## $\texttt{UserList}$ objects
$\texttt{UserList}$는 리스트 객체를 감싸는 wrapper처럼 동작한다. 사용자가 정의한 상속을 받거나 존재하는 메서드를 덮어 씌우거나 새 메서드를 만들 수 있는 유사 리스트 클래스에 유용한  베이스 클래스이다. 이 방법으로 사용자는 리스트가 새로운 행위를 할 수 있게 한다.

이 클래스의 필요성은 `list`로부터 직접 서브클래스를 만드는 기능으로 부분적으로 대체되었으나, 이 클래스는 underlying 리스트에 속성으로 접근할 수 있기 때문에 좀 더 다루기 쉽다.

- $\texttt{class collection.UserList([{\it list}])}$
    리스트를 시뮬레이션하는 클래스. 인스턴스의 내용은 $\texttt{UserList}$ 인스턴스의 `data` 속성을 통해 접근할 수 있는 일반적인 리스트에 저장된다. 인스턴스의 내용은 초기에는 기본값이 빈 리스트인 *리스트*의 사본으로 설정된다. *리스트*는 일반적인 파이썬 리스트나 $\texttt{UserList}$ 객체 등 아무 iterable이나 가능하다.

    메서드와 mutable sequence의 연산을 지원하기 위해, $\texttt{UserList}$ 인스턴스는 다음의 속성을 제공한다.

    - $\texttt{data}$<br>
    $\texttt{UserList}$ 클래스의 내용을 저장하기 위해 사용되는 일반적인 리스트.

**서브클래스 생성 시 요구사항**: $\texttt{UserList}$의 서브클래스는 인수가 한 개 이하인 생성자를 통해 만들 수 있다. 새로운 sequence를 반환하는 리스트 연산은 실제로 구현된 클래스의 인스턴스를 생성하는 시도를 한다. 그렇게 하기 위해 데이터 소스로 사용되는 sequence 객체를 하나의 파라미터로 생성자와 함께 호출한다.

만약 유도된 클래스가 이 요구사항에 응하지 않는다면, 이 클래스가 지원하는 모든 특별한 메서드는 덮어 씌워져야 하기 때문에 이런 경우에 제공되어야 하는 메서드에 관한 정보의 출처에게 자문한다.
<br><br>

## $\texttt{UserString}$ objects
$\texttt{UserString}$는 문자열 객체를 감싸는 wrapper처럼 동작한다. 이 클래스의 필요성은 `str`에서 직접 서브클래스를 만드는 기능에 의해 대체되었으나, 속성으로 underlying 문자열에 접근할 수 있기 때문에 좀 더 다루기 쉽다.

- $\texttt{class collections.UserString({\it seq})}$<br>
    문자열 객체를 구현하는 클래스. 인스턴스의 내용은 $\texttt{UserString}$ 인스턴스의 `data` 속성을 통해 접근할 수 있는 일반적인 문자열 객체에 저장된다. 인스턴스의 내용은 초기에는 `seq`의 사본으로 정해진다. `seq` 인수는 빌트인 `str()` 함수를 통해 문자열로 변환될 수 있는 객체라면 모두 가능하다.

    문자열의 메서드와 연산을 지원하는 것에 더해, $\texttt{UserString}$ 인스턴스는 다음의 속성을 제공한다.

    - $\texttt{data}$<br>
    $\texttt{UserString}$ 클래스의 내용을 저장하기 위해 사용되는 일반 `str` 객체.

    *버전 3.5에서 변경됨*: 새로운 메서드 `__getnewargs__`, `__rmod__`, `casefold`, `format_map`, `isprintable` 그리고 `maketrans`.