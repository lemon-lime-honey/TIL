# math
[Documentation](https://docs.python.org/3/library/math.html)

이 모듈은 C 표준에 의해 정의된 수학 함수에 접근할 수 있게 한다.

이 함수들은 복소수와 함께 사용할수 없다. 만약 복소수 지원이 필요하다면 `cmath` 모듈에 있는 동명의 함수들을 사용해야 한다. 복소수를 지원하는 함수와 지원하지 않는 함수의 차이는 대부분의 사용자들이 복소수를 이해하는데에 요구되는 정도의 수학을 공부하고 싶어하지 않는 것에 기인한다. 복소수 결과값 대신 예외가 발생하는 것은 원치 않는 복소수 숫자가 파라미터로 사용되는 것을 조기에 알게 해 프로그래머가 복소수가 생성된 이유와 방법을 찾을 수 있게 한다.

다음의 함수들은 이 모듈에 의해 제공된다. 직접적으로 다르게 기술된 것이 아니라면 모든 반환값은 `float`이다.

## Number-theoretic and representation functions
- $\texttt{math.ceil({\it{x}})}$<br>
  `x`의 올림, 즉 `x`보다 크거나 같은 정수 중 가장 작은 것을 반환한다. 만약 `x`가 `float`가 아니라면 `x.__ceil__`이 대신하여 [Integral](https://docs.python.org/3/library/numbers.html#numbers.Integral) 값을 반환한다.

- $\texttt{math.comb({\it{n, k}})}$<br>
  반복과 순서 없이 `n`개의 아이템 중 `k`개의 아이템을 고르는 경우의 수를 반환한다.

  $k <= n$일 때 $\frac{n!}{k! \times (n - k)!}$, $k > n$일 때 $0$으로 계산한다.

  $(1 + x)^n$의 다항식 전개의 `k`번째 항의 계수와 같기 때문에 이항계수로도 불린다.

  만약 두 인수 중 어느 하나라도 정수가 아니라면 `TypeError`를 발생시킨다. 두 인수 중 어느 하나라도 음수이면 `ValueError`를 발생시킨다.

  *버전 3.8에서 추가됨*

- $\texttt{math.copysign({\it{x, y}})}$<br>
  `x`의 크기(절대값)와 `y`의 부호를 가진 `float`를 반환한다. 부호가 있는 0을 지원하는 환경에서 `copysign(1.0, -0.0)`은 `-1.0`을 반환한다.

- $\texttt{math.fabs({\it{x}})}$<br>
  `x`의 절대값을 반환한다.

- $\texttt{math.factorial({\it{n}})}$<br>
  `n` 팩토리얼을 정수로 반환한다. 만약 `n`이 [Integral](https://docs.python.org/3/library/numbers.html#numbers.Integral)이 아니거나 음수라면 `ValueError`를 발생시킨다.

  *버전 3.9부터 사용되지 않음*: [Integral](https://docs.python.org/3/library/numbers.html#numbers.Integral)값을 가진 `float`(예: 5.0) 사용이 중단됨

- $\texttt{math.floor({\it{x}})}$<br>
  `x`의 내림, 즉 `x`보다 작거나 같은 가장 큰 정수를 반환한다. 만약 `x`가 `float`가 아니라면 만약 `x`가 `float`가 아니라면 `x.__floor__`가 대신하여 [Integral](https://docs.python.org/3/library/numbers.html#numbers.Integral) 값을 반환한다.