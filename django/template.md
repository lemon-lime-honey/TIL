# Template System
데이터 표현을 제어하며 표현에 관한 로직을 담당한다.

## Django Template Language(DTL)
Template에서 조건, 반복, 변수, 필터 등의 프로그래밍적 기능을 제공하는 시스템

### DTL Syntax
#### Variable `{{ variable }}`
- $\texttt{view}$ 함수에서 $\texttt{render}$ 함수의 세 번째 인자를 통해 딕셔너리 타입으로 넘겨받을 수 있다.
- 딕셔너리 `key`에 해당하는 문자열이 template에서 사용 가능한 변수명이 된다.
- $\texttt{.}$을 사용하여 변수 속성에 접근할 수 있다.

#### Filters `{{ variable|filter }}`
- 표시할 변수를 수정할 때 사용한다.
- chained가 가능하며, 일부 필터는 인자를 받기도 한다.
  - 예: `{{ name|truncatewords:30 }}`
- 약 60개의 built-in template filter가 제공된다.

#### Tags `{% tag %}`
- 반복 또는 논리를 수행하여 제어 흐름을 만드는 등 변수보다 복잡한 일을 수행한다.
- 일부 태그는 시작과 종료 태그가 필요하다.
  - 예: `{% if %} {% endif %}`
- 약 24개의 built-in template tags가 제공된다.

#### Comments
```
{% comment %}
  {% if name == 'Anakin' %}
  {% endif %}
{% endcomment %}
```
<br><br>

# 템플릿 상속
페이지의 공통요소를 포함하고 하위 템플릿이 재정의할 수 있는 공간을 정의하는 기본 `skeleton` 템플릿을 작성하여 상속 구조를 구축한다.

## 예시
### skeleton
```html
<!-- skeleton.html -->

<!DOCTYPE html>
<html lang="en">
<head>
  ...
  {% block style %}
  {% endblock style %}
</head>
<body>
  {% block content %}
  {% endblock content %}
</body>
</html>
```

### page
```html
{% extends 'skeleton.html' %}

{% block style %}
  <style>
    * { color: #003153 }
  </style>
{% endblock style %}

{% block content %}
  <p>From a certain point of view?</p>
{% endblock content %}
```

## `extends` tag
`{% extends 'path' %}`<br>
- 하위 템플릿이 상위 템플릿을 확장한다는 것을 알린다.
- 반드시 템플릿 최상단에 작성되어야 하며, 2개 이상 사용할 수 없다.

## `block` tag
`{% block name %} {% endblock name %}`<br>
- 하위 템플릿에서 재정의(overriden) 할 수 있는 블록을 정의한다.
- 하위 템플릿이 작성할 수 있는 공간을 지정한다.

# 요청과 응답 w/ HTML form
## 데이터 수신과 송신
- HTML form은 HTTP 요청을 서버에 보내는 가장 편리한 방법이다.
- HTML form element를 통해 사용자와 애플리케이션 간의 상호작용을 이해할 수 있다.

## `form` element
- 사용자로부터 할당된 데이터를 서버로 전송한다.
- 웹에서 사용자 정보를 입력하는 여러 방식(text, password 등)을 제공한다.

## `action`과 `method`
- form의 핵심 속성 두 가지
- `action`: 데이터의 목적지
  - 입력 데이터가 전송될 URL을 지정한다.
  - 이 속성이 지정되지 않으면 데이터는 현재 form이 있는 페이지의 URL로 송신된다.
- `method`: 데이터 송신 방식
  - 데이터를 어떤 방식으로 보낼 것인지 정의한다.
  - 데이터의 HTTP request methods(GET, POST)를 지정한다.

## `input` element
- 사용자의 데이터를 입력받을 수 있는 요소
- type 속성 값에 따라 다양한 유형의 입력 데이터를 받는다.

### `name`
- `input`의 핵심 속성
- 데이터를 제출했을 때 서버는 `name`속성에 설정된 값을 통해 사용자가 입력한 데이터에 접근할 수 있다.

## Query String Parameters
- 사용자의 입력 데이터를 URL 주소에 파라미터를 통해 넘기는 방법
- 문자열은 앰퍼샌드(&)로 연결된 `key=value` 쌍으로 구성되며, 기본 URL과 물음표(?)로 구분된다.
- `http://host:port/path?key=value&key=value`

## form 데이터의 위치
모든 요청 데이터는 HTTP request(view 함수의 첫 번째 인자) 객체에 들어있다.