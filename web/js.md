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