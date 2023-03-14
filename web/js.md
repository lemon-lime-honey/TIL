# Javascript
웹페이지의 동적인 기능을 구현한다.
<br><br>

# DOM
웹페이지를 구조화된 객체로 제공하여 프로그래밍 언어가 웹페이지를 사용할 수 있게 연결시킨다.

## $\texttt{document}$ object
- 웹페이지 객체
- DOM Tree의 진입점
- 페이지를 구성하는 모든 객체 요소를 포함한다.

## DOM Query
### $\texttt{document.querySelector()}$
- 제공한 선택자와 일치하는 element를 한 개 선택한다.
- 제공한 CSS selector를 만족하는 첫 번째 element 객체를 반환한다. (없다면 null 반환)

### $\texttt{document.querySelectorAll()}$
- 제공한 선택자와 일치하는 여러 element를 선택한다.
- 매칭할 하나 이상의 선택자를 포함하는 유효한 CSS selector를 인자(문자열)로 받는다.
- 제공한 CSS selector를 만족하는 NodeList를 반환한다.

## DOM Manipulation
### $\texttt{classList}$ property
- 요소의 클래스 목록을 DOMTokenList(유사 배열) 형태로 반환한다.
- $\texttt{add}$와 $\texttt{remove}$ 메서드를 사용해 지정한 클래스 값을 추가 혹은 제거한다.

#### $\texttt{element.classList.add()}$
- 지정한 클래스 값을 추가한다.

#### $\texttt{element.classList.remove()}$
- 지정한 클래스 값을 제거한다.

### Attribute Manipulation
#### $\texttt{element.getAttribute()}$
- 해당 요소에 지정된 값을 반환한다.

#### $\texttt{element.setAttribute()}$
- 지정된 요소의 속성 값을 설정한다.
- 속성이 이미 있으면 값을 업데이트 한다.
- 속성이 없으면 지정된 이름과 값으로 새 속성을 추가한다.

#### $\texttt{element.removeAttribute()}$
- 요소에서 지정된 이름을 가진 속성을 제거한다.

### $\texttt{textContent}$ property
요소의 텍스트 콘텐츠를 표현한다.

### DOM Element Manipulation
- $\texttt{.createElement()}$
- $\texttt{.appendChild()}$
- $\texttt{.removeChild()}$

### $\texttt{style}$ property
$\texttt{color}$, $\texttt{fontSize}$ 등으로 스타일을 변경할 수 있다.
<br>

# JavaScript 문법
## 변수
### 식별자 작성 규칙
- 반드시 문자, $, _로 시작한다.
- 대소문자를 구분하며, 클래스명 이외의 경우 모두 소문자로 시작한다.
- 예약어 사용 불가
- 카멜 케이스(camelCase): 변수, 객체, 함수에 사용한다.
- 파스칼 케이스(PascalCase): 클래스, 생성자에 사용한다.
- 대문자 스네이크 케이스(SNAKE_CASE): 상수에 사용한다.

### 변수 선언 키워드
- 기본적으로 $\texttt{const}$ 사용을 권장한다.
- 재할당해야 하는 경우에만 $\texttt{let}$을 사용한다.
- $\texttt{let}$
    - 블록 스코프를 가지는 지역 변수를 선언한다.
    - 재할당이 가능하지만 재선언은 불가능하다.
- $\texttt{const}$
    - 블록 스코프를 가지는 지역 변수를 선언한다.
    - 재할당과 재선언이 불가능하다.
- $\texttt{var}$
    - 재할당과 재선언이 가능하다.
    - ES6 이전에 변수를 선언할 때 사용했다.
    - 함수 스코프를 가진다.
    - 호이스팅되는 특성으로 예기치 못한 문제가 발생할 수 있다.
        - 변수를 선언 이전에 참조할 수 있는 현상. 변수 선언 이전의 위치에서 접근하면 `undefined`를 반환한다.
        - ES6부터 $\texttt{var}$ 대신 $\texttt{const}$와 $\texttt{let}$ 사용을 권장한다.
    - 변수 선언 시 $\texttt{var}$, $\texttt{const}$, $\texttt{let}$ 키워드 중 하나를 사용하지 않으면 자동으로 $\texttt{var}$로 선언된다.

#### 블록 스코프
- $\texttt{if}$, $\texttt{for}$, 함수 등의 중괄호 내부를 가리킨다.
- 블록 스코프를 가지는 변수는 블록 바깥에서 접근할 수 없다.
<br><br>

## 데이터 타입
### 원시 자료형(Primitive type)
- $\texttt{Number}$, $\texttt{String}$, $\texttt{Boolean}$, $\texttt{undefined}$, $\texttt{null}$
- 변수에 값이 직접 저장되는 자료형
- 불변, 값이 복사된다.

#### $\texttt{String}$
- 덧셈을 통해 문자열끼리 붙일 수 있다.
- `backtick`을 통한 `Template Literal`을 사용하여 문자열 사이에 변수를 삽입할 수 있다.

#### $\texttt{Boolean}$
- 조건문 또는 반복문에서 `boolean`이 아닌 데이터 타입은 자동 형변환 규칙에 의해 `true` 또는 `false`로 변환된다.

### 참조 자료형(Reference type)
- $\texttt{Object}$, $\texttt{Array}$, $\texttt{Function}$
- 객체의 주소가 저장되는 자료형
- 가변, 주소가 복사된다.

### ToBoolean conversions (자동 형변환)
| 데이터 타입 | false | true |
| --- | --- | --- |
| undefined | 항상 false | X |
| null | 항상 false | X |
| Number | 0, -0, NaN | 나머지 모든 경우 |
| String | 빈 문자열 | 나머지 모든 경우 |

<br><br>

## 연산자
### 할당 연산자
- 오른쪽에 있는 피연산자의 평가 결과를 왼쪽 피연산자에 할당하는 연산자
- 다양한 연산에 대한 단축 연산자를 지원한다.
- `++`, `--`, `+=`, `-=` 등

### 비교 연산자
- 피연산자(숫자, 문자, Boolean 등)를 비교하고 결과값을 boolean으로 반환하는 연산자

### 동등 연산자 `==`
- 두 피연산자가 같은 값으로 평가되는지 비교 후 boolean 값을 반환한다.
- 비교할 때 암묵적 타입 변환을 통해 타입을 일치시킨 후 같은 값인지 비교한다.
- 두 피연산자가 모두 객체일 경우 메모리의 같은 객체를 바라보는지 판별한다.
- 예상치 못한 결과가 발생할 수 있으므로 특별한 경우를 제외하면 사용하지 않는다.

### 일치 연산자 `===`
- 두 피연산자의 값과 타입이 모두 같은 경우 `true`를 반환한다.
- 같은 객체를 가리키거나 같은 타입이면서 같은 값인지 비교한다.
- 엄격한 비교가 이루어지며, 암묵적 타입 변환이 발생하지 않는다.

### 논리 연산자
| 역할 | 표기 |
| --- | --- |
| and | `&&` |
| or | `\|\|` |
| not | `!` |

<br><br>

## 조건문
### $\texttt{if}$
조건 표현식의 결과값을 boolean 타입으로 변환 후 참/거짓을 판단한다.
```javascript
if (조건문) {
  명령문
} else if (조건문) {
  명령문
} else {
  명령문
}
```
<br><br>

## 반복문
| 키워드 | 연관 키워드 | 스코프 |
| --- | --- | --- |
| $\texttt{while}$ | break, continue | 블록 스코프 |
| $\texttt{for}$ | break, continue | 블록 스코프 |
| $\texttt{for...in}$ | object 순회 | 블록 스코프 |
| $\texttt{for...of}$ | iterable 순회 | 블록 스코프 |

### $\texttt{while}$
조건문이 참이면 문장을 계속해서 수행한다.
```javascript
while (조건문) {
  // do something
}
```

### $\texttt{for}$
특정한 조건이 거짓으로 판별될 때까지 반복한다.
```javascript
for ([초기문]; [조건문]; [증감문]) {
  // do something
}
```

### $\texttt{for...in}$
객체의 속성을 순회할 때 사용한다.<br>
배열도 순회할 수 있으나 인덱스 순으로 순회한다는 보장이 없으므로 권장하지 않는다.
```javascript
for (variable in object) {
  statements
}
```

### $\texttt{for...of}$
반복 가능한 객체(배열, 문자열 등)를 순회할 때 사용한다.
```javascript
for (variable of object) {
  statements
}
```