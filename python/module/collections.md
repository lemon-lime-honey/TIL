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