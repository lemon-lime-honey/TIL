# Collections
[Documentation](https://docs.python.org/3/library/collections.html#module-collections)

## ChainMap objects
*버전 3.3에서 추가*
- 클래스 $\texttt{ChainMap}$은 매핑 된 숫자를 빠르게 연결해 하나의 단위로 취급될 수 있게 해준다. 딕셔너리를 생성하거나 $\texttt{update()}$를 여러 번 호출할 때보다 훨씬 빠를 수 있다.
- 이 클래스는 nested scope를 시뮬레이션 할 때 사용할 수 있으며 templating에 유용하다.
<br></br>

### $\texttt{class collections.ChainMap({\it*maps})}$
- $\texttt{ChainMap}$은 여러 개의 딕셔너리나 다른 매핑된 객체들을 묶어 하나의 갱신 가능한 view로 만든다. 만약 $\texttt\it{maps}$가 특정되지 않는다면 새 chain이 언제나 최소 하나의 매핑을 가질 수 있도록 하나의 빈 딕셔너리가 주어진다.