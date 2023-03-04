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
*버전 3.3에서 추가됨*: Unary plus, unary minus, 그리고 in-place multiset 연산 지원 추가