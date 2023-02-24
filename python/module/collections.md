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