# heapq
[Documentation](https://docs.python.org/3/library/heapq.html)

이 모듈은 우선순위 큐 알고리즘으로도 알려진 힙 큐 알고리즘 구현을 제공한다.

힙은 모든 상위 노드의 값이 하위 노드의 값보다 작거나 같은 이진트리이다. 이 구현은 0부터 시작하는 모든 `k`에 대해 `heap[k] <= heap[2 * k + 1]`과 `heap[k] <= heap[2 * k + 2]`를 만족하는 배열을 사용한다. 비교를 위해, 존재하지 않는 원소는 무한으로 간주된다. 힙은 루트 `heap[0]`이 언제나 가장 작은 원소를 가지는 흥미로운 특징을 보인다.

아래에 있는 API는 두 가지 측면에서 교과서의 힙 알고리즘과 다르다. 1) 인덱스가 0부터 시작한다. 이는 노드의 인덱스와 하위 노드의 인덱스 사이의 관계가 약간 더 모호해보이게 하지만, 파이썬의 인덱스가 0부터 시작하므로 좀 더 안정적이다. 2) `pop` 메소드는 가장 큰 요소가 아닌 가장 작은 요소를 반환한다. 이는 교과서에서 `최소 힙`으로 불리는데, 문서에서는 in-place sorting의 안정성 때문에 `최대 힙`이 더 흔히 보인다.

이 두 특성은 문제없이 파이썬의 일반적인 리스트를 힙으로 볼 수 있게 만든다. `heap[0]`은 가장 작은 요소이고, `heap.sort()`는 힙의 불변성을 유지한다.

힙을 만드려면, `[]`으로 초기화된 리스트를 사용하거나 함수 `heapify()`를 이용하여 이미 존재하는 리스트를 힙으로 변환한다.

다음의 함수가 제공된다.

- $\texttt{heapq.heappush({\it heap, item})}$<br>
  힙 불변성을 유지하며 힙에 요소를 넣는다.

- $\texttt{heapq.heappop({\it heap})}$<br>
  힙에서 가장 작은 요소를 힙 불변성을 유지하며 pop하고 반환한다. 만약 힙이 비었다면 `IndexError`가 발생한다. 가장 작은 요소에 제거 없이 접근하려면 `heap[0]`을 사용한다.

- $\texttt{heapq.heappushpop({\it heap, item})}$<br>
  요소를 힙에 넣고, 힙에서 가장 작은 요소를 pop하고 반환한다. 이 복합적인 동작은 `heappush()` 다음에 `heappop()`을 호출하는 것보다 더 효율적으로 동작한다.

- $\texttt{heapq.heapifty({\it x})}$<br>
  리스트 `x`를 제자리에서 선형시간에 힙으로 변환한다.

- $\texttt{heapq.heapreplace({\it heap, item})}$<br>
  힙에서 가장 작은 요소를 pop하고 반환하고, 새 `item`을 넣는다. 힙의 크기가 변하지 않는다. 만약 힙이 비었다면, `IndexError`가 발생한다.

  이 동작은 `heappop()` 다음에 `heappush()`를 호출하는 것보다 더 효율적이며, 고정 크기 힙을 사용하는 경우에는 더 적절할 수 있다. 이 pop/push 조합은 언제나 힙에서 요소 하나를 반환하며 그것을 `item`으로 대체한다.

  반환된 값이 추가된 `item`보다 더 큰 값일 수 있다. 만약 그것을 원하지 않는다면, 대신 `heappushpop()`의 사용을 고려한다. 그것의 push/pop 조합은 두 개의 값 중 더 작은 것을 반환하고 더 큰 것을 힙에 남겨둔다.

또한 이 모듈은 힙에 기반한 세 개의 일반적인 목적의 함수를 제공한다.

- $\texttt{heapq.merge({\it *iterables, key=None, reverse=False})}$<br>
  여러 개의 정렬된 입력을 하나의 정렬된 입력으로 병합한다.(예를 들어, 복수의 로그 파일로부터 타임스탬프된 항목들을 병합한다.) 정렬된 값의 iterator를 반환한다.

  `sorted(itertools.chain(*iterables))`와 유사하나 iterable을 반환하고, 데이터를 한 번에 메모리로 가져오지 않으며, 각각의 입력 스트림이 이미 오름차순으로 정렬되었다고 가정한다.

  키워드 인자로 구체화해야 하는 두 개의 선택 인자를 가진다.

  `key`는 각각의 입력 요소에서 비교 키를 추출하는데 사용하는 단일 인자의 키 함수를 지정한다. 기본값은 `None`이다.(요소를 직접 비교한다.)

  `reverse`는 불리언 값이다. 만약 `True`라면 입력 요소는 마치 각 비교가 뒤집어진 것처럼 병합된다. `sorted(itertools.chain(*iterables), reverse=True)`와 유사한 동작을 구현하려면, 모든 iterable은 오름차순으로 정렬되어 있어야만 한다.

  *버전 3.5에서 변경됨*: 옵션 파라미터 `key`, `reverse` 추가

- $\texttt{heapq.nlargest({\it n, iterable, key=None})}$<br>
  `iterable`로 정의된 dataset으로부터 `n`개의 큰 요소들을 가져와 만든 리스트를 반환한다. `key`(예를 들어 `key=str.lower`)는`iterable`의 각 요소에서 비교 키를 추출하는데 사용하는 단일 인자의 함수를 구체화하는 선택 인자이다. `sorted(iterable, key=key)[:n]`과 동등하다.

- $\texttt{heapq.nlargest({\it n, iterable, key=None})}$<br>
  `iterable`로 정의된 dataset으로부터 `n`개의 작은 요소들을 가져와 만든 리스트를 반환한다. `key`(예를 들어 `key=str.lower`)는`iterable`의 각 요소에서 비교 키를 추출하는데 사용하는 단일 인자의 함수를 구체화하는 선택 인자이다. `sorted(iterable, key=key)[:n]`과 동등하다.

마지막 두 함수는 `n`이 작은 값을 가질 때 성능이 좋다. 더 큰 값에서는 `sorted()` 함수를 사용하는 것이 더 효율적이다. 또한 `n==1`일 때 빌트인 `min()`과 `max()`함수를 사용하는 것이 더 효율적이다. 만약 이 함수들이 반복적으로 사용되어야 한다면, iterable을 힙으로 변경하는 것을 고려한다.
<br><br>

# Basic Examples
모든 값을 힙에 넣은 후 가장 작은 값을 pop하는 것으로 병합 정렬을 구현할 수 있다.

```python
>>> def heapsort(iterable):
...    h = []
...    for value in iterable:
...        heappush(h, value)
...    return [heappop(h) for i in range(len(h))]
...
>>> heapsort([1, 3, 5, 7, 9, 2, 4, 6, 8, 0])
[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
```

이는 `sorted(iterable)`과 유사하나 `sorted()`와는 달리 안정적이지 않다.

힙 요소는 튜플이 될 수 있다. 이는 주 기록이 추적되는 동안 (가령 수행 우선순위와 같은) 비교값을 지정하는데 유용하다.

```python
>>> h = []
>>> heappush(h, (5, 'write code'))
>>> heappush(h, (7, 'release product'))
>>> heappush(h, (1, 'write spec'))
>>> heappush(h, (3, 'create tests'))
>>> heappop(h)
(1, 'write spec')
```
<br><br>

# Priority Queue Implementation Notes

우선순위 큐는 힙의 일반적인 사용법이며 여러 구현 상의 난제를 가진다.

- 정렬의 안정성: 동일한 우선순위를 가지는 두 개의 일을 어떻게 추가된 순서로 반환하게 할 수 있는가?
- (우선순위, 일)과 같은 튜플은 우선순위가 같고 일에 관한 기본적인 비교 순서가 없다면 정렬이 성립하지 않는다.
- 만약 우선순위나 일이 변경된다면 힙에서 어떻게 새로운 위치로 옮길 것인가?
- 또는 대기 중인 일이 삭제되어야 한다면 큐에서 어떻게 찾아서 삭제할 것인가?

처음 두 문제의 해결 방안은 엔트리를 우선순위, 엔트리 카운트, 일로 구성된 세 개의 요소를 가진 리스트로 저장하는 것이다. 엔트리 카운트는 같은 우선순위를 가진 두 일을 추가된 순서대로 반환하는 타이 브레이커 역할을 한다. 그리고 중복된 값을 갖는 엔트리 카운트가 없기 때문에 튜플 비교는 두 일을 직접적으로 비교하는 일이 없다.

비교 불가한 일 문제의 또다른 해결법은 일 아이템을 무시하고 오직 우선순위 필드만 비교하는 wrapper 클래스를 만드는 것이다.

```python
from dataclasses import dataclass, field
from typing impor Any

@dataclass(order=True)
class PrioritizedItem:
    priority: int
    item: Any=field(compare False)
```

남은 문제는 대기 중인 일을 찾고 그것의 우선순위를 변경하거나 완전히 삭제하는 것이다. 일을 찾는 것은 큐의 엔트리를 가리키는 딕셔너리로 해결할 수 있다.

엔트리를 제거하거나 그것의 우선순위를 변경하는 것은 힙 구조의 불변성을 깰 수 있기 때문에 더 어렵다. 그러므로 엔트리를 제거된 것으로 마크하고 개정된 우선순위를 가진 새 엔트리를 추가하는 것이 가능한 해결 방법이다.

```python
pq = []                      # list of entries arranged in  a heap
entry_finder = {}            # mapping of tasks to entries
REMOVED = '<removed-task>'   # placeholder for a removed task
coutner = itertools.count()  # unique sequence count

def add_task(task, priority=0):
    # Add a new task or update the priority of an existing task
    if task in entry_finder:
        remove_task(task)
    count = next(counter)
    entry = [priority, count, task]
    entry_finder[task] = entry
    heappush(pq, entry)

def remove_task(task):
    # Mark an existing task as REMOVED. Raise KeyError if not found
    entry = entry_finder.pop(task)
    entry[-1] = REMOVED

def pop_task():
    # Remove and return the lowest priority task. Raise KeyError if empty
    while pq:
      priority, count, task = heappop(pq)
      if task is not REMOVED:
          del entry_finder[task]
          return task
    raise KeyError('pop from an empty priority queue')
```