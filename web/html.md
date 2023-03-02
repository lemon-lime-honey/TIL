# HTML
- **H**yper**T**ext **M**arkup **L**anguage
- 웹 페이지의 의미와 구조를 정의하는 단어

## Hypertext
- 웹 페이지를 다른 페이지로 연결하는 링크
- 참조를 통해 사용자가 한 문서에서 다른 문서로 즉시 접근할 수 있는 텍스트

## Markup Language
- 태그 등을 이용하여 문서나 데이터의 구조를 명시하는 언어
- HTML, Markdown 등이 있다.
<br><br>

# HTML Structure
## HTML Element
```HTML
<p>New Hope: Luke Skywalker</p>
```
- 하나의 *element*는 여는 태그, 닫는 태그, 그 안의 내용으로 구성된다.
- 닫는 태그는 태그 이름 앞에 슬래시가 포함된다.
- 닫는 태그가 없는 태그도 존재한다.

## HTML Attributes
```HTML
<p class="ani">The Chosen One: Anakin Skywalker</p>
```
- 규칙
    - 요소 이름 다음에 바로 오는 속성은 요소 이름과 속성 사이에 공백이 있어야 한다.
    - 하나 이상의 속성이 있는 경우 공백으로 구분한다.
    - 속성 값은 따옴표로 감싸야 한다.
- 목적
    - 나타내고 싶지 않지만 추가적인 기능이나 내용을 담고 싶을 때 사용한다.
    - CSS가 해당 요소를 선택하기 위한 값으로 활용된다.

## HTML 문서의 구조
```HTML
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>The Negotiator</title>
</head>
<body>
  <p>Obi-Wan Kenobi</p>
</body>
</html>
```
- `<!DOCTYPE html>`: 해당 문서가 html 문서라는 것을 나타낸다.
- `<html></html>`: 전체 페이지의 콘텐츠를 포함한다.
- `<title></title>`: 브라우저 탭 및 즐겨찾기 시 표시되는 제목
- `<head></head>`
    - html 문서에 관련된 설명, 설정 등을 포함한다.
    - 사용자에게는 보이지 않는다.
- `<body></body>`: 페이지에 표시되는 모든 콘텐츠

## HTML Text Structure
- HTML의 주요 목적 중 하나는 텍스트 구조와 의미를 제공하는 것이다.
- Heading, Parahraphs: `h1`, `h2`, `h3`, `h4`, `h5`, `h6`, `p`
- Lists: `ol`, `ul`, `li`
- Emphasis, Importance: `em`, `strong`

## HTML Semantic Element
기본적인 모양과 기능 이외의 의미를 가지는 HTML 요소<br>
검색엔진 및 개발자가 웹 페이지의 콘텐츠를 이해하기 쉽게 만들어준다.

### 페이지 구조화를 위한 대표적인 semantic element
$\texttt{header}$, $\texttt{nav}$, $\texttt{main}$, $\texttt{article}$, $\texttt{section}$, $\texttt{aside}$, $\texttt{footer}$