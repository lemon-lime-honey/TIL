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

- $\texttt{math.fmod({\it{x, y}})}$<br>
  C 라이브러리에서 정의된 것처럼 `fmod(x, y)`를 반환한다. 파이썬 표현식 `x % y`가 같은 결과를 반환하지 않을 수 있다는 점에 유의하라. C 표준의 목적은 `fmod(x, y)`가 정확히 (수학적으로, 무한히 정확한) 어떤 정수 *n*에 대해 *x*와 부호가 같고 크기는 `abs(y)`보다 작은 `x - n*y`와 같게 하는 것이다. 파이썬의 `x % y`는 *y*와 부호가 같은 결과를 반환하고, float 인수를 정확히 계산하지 못할 수 있다. 예를 들어 `fmod(-1e-100, 1e100)`은 `-1e-100`이지만 파이썬의 `-1e-100 % 1e100`은 float로 정확히 표현될 수 없으며, 놀랍게도 `1e100`으로 반올림이 되는 `1e100-1e100`이다. 이러한 이유로 
  정수를 다룰 때에는 파이썬의 `x % y`가 선호되는 반면 float를 다룰 때에는 보통 함수 `fmod()`가 선호된다.

- $\texttt{math.frexp({\it{x}})}$<br>
  가수부(mantissa)와 지수 x를 `(m, e)`와 같은 한 쌍으로 반환한다. *m*은 float이고 *e*는 정수이며, `x == m * 2**e`를 만족한다. 만약 *x*가 0이면 `(0.0, 0)`을 반환하고 그 외의 경우에는 `0.5 <= abs(m) < 1`을 반환한다. 이는 float의 내부 표현을 이식성 있는 방식으로 *분리*하는데 사용된다.

- $\texttt{math.fsum({\it{iterable}})}$<br>
  iterable 내의 값의 정확한 floating point 합을 반환한다. 복수의 중간 부분 합들을 추적하여 정밀도의 손실을 방지한다.
  ```python
  >>> sum([.1, .1, .1, .1, .1, .1, .1, .1, .1, .1])
  0.9999999999999
  >>> fsum([.1, .1, .1, .1, .1, .1, .1, .1, .1, .1])
  1.0
  ```
  알고리즘의 정확도는 IEEE-754 산술의 보증과 올림 모드가 짝수로 빈올림(half-even)인 일반적인 경우에 의존한다. 윈도우가 아닌 일부 빌드에서 하부 C 라이브러리는 확장된 정밀 덧셈을 사용하며 때로 중간 합을 이중 자리 올림(double-round)해 최하위 비트에서 분리할 수 있다.

  자세한 사항은 [ASPN cookbook recipes for accurate floating point summation](https://code.activestate.com/recipes/393090/)에서 확인할 수 있다.

- $\texttt{math.gcd({\it{*integers}})}$<br>
  지정된 정수 인자들의 최대공약수를 반환한다. 만약 인수 중 하나라도 0이 아니라면 반환값은 모든 인수의 약수인 가장 큰 양의 정수이다. 만약 모든 인수가 0이라면 반환값은 `0`이다. 인수가 없는 `gcd()`는 `0`을 반환한다.

  *버전 3.5에서 추가됨*

  *버전 3.9에서 변경됨*: 임의의 개수의 인수 지원이 추가됨. 이전에는 오직 두 개의 인수만을 지원함.